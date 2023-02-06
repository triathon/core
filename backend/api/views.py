import json
import os
import sys
import time
import traceback
import zipfile
import shutil
from hashlib import sha1

from Crypto.Random import random
from django.core.files.uploadedfile import SimpleUploadedFile as File
from django.db.models import Count
from django.http import FileResponse
from django_redis import get_redis_connection
from eth_account.messages import encode_defunct
from hexbytes import HexBytes
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from web3.auto import w3

from api.models import Document, User, DocumentResult
from api.serializers import WriteDocumentSerializer, ReadDocumentSerializer, DetectionLogSerializer, \
    DocumentResultSerializer
from api.tools.contract_helper import fetch_contract_meta, write_contract
from conf import config
from api.tools.merge_contract import Merge
from api.tools.rsc_func import rsaEncrypt, rsaDecrypt
from api.tools.verify_submit_status import checkstatus
from api.tools.detection_result import parseErrorResult
from api.tools.deltaT import cal_time

rd = get_redis_connection()


def set_queue(d_id):
    rd.lpush(config.coreslither_queue, d_id)
    rd.lpush(config.corethril_queue, d_id)
    rd.lpush(config.coresmartian_queue, d_id)


# auth

class AuthView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        address = request.query_params.get('address')
        if not address:
            return Response({'code': 403, 'message': 'wallet address is needed'}, status=403)
        user = User.objects.filter(wallet_address=address).first()
        if not user:
            user = User.objects.create(wallet_address=address, username=address)
        return Response({'nonce': user.nonce})

    def post(self, request):
        signature = request.data['signature']
        address = request.data['address']

        user, created = User.objects.get_or_create(wallet_address=address)
        msg = encode_defunct(text=f'Welcome login with nonce={user.nonce}')
        rec_address = w3.eth.account.recover_message(msg, signature=HexBytes(signature))

        user.nonce = random.randint(100000, 1000000)
        user.save()
        if address == rec_address:
            return Response({"token": str(AccessToken.for_user(user))})
        else:
            return Response({"token": None}, status=403)


class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        address = request.query_params.get('address')
        if not address:
            return Response({'code': 403, 'message': 'wallet address is needed'}, status=403)
        user = User.objects.filter(wallet_address=address).first()
        if not user:
            user = User.objects.create(wallet_address=address, username=address)
        nonceEncrypt, privateKey = rsaEncrypt(str(user.nonce))
        user.rsa_privateKey = privateKey
        user.save()
        return Response({'nonce': nonceEncrypt})

    def post(self, request):
        nonce = request.data['nonce']
        address = request.data['address']

        user, created = User.objects.get_or_create(wallet_address=address)
        nonceDecrypt = rsaDecrypt(nonce, eval(user.rsa_privateKey))
        user_noce = str(user.nonce)
        user.nonce = random.randint(100000, 1000000)
        user.save()
        if nonceDecrypt == user_noce:
            return Response({"token": str(AccessToken.for_user(user))})
        else:
            return Response({"token": None}, status=403)


# upload


class SubmitContractAddress(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request):
        doc = Document.objects.filter(user=self.request.user).defer("file").order_by("-id")
        first = doc.first()
        if first:
            status, resp = checkstatus(doc, first.result)
            if not status:
                return Response(resp)

        network, address = request.data['network'], request.data['address']
        if network not in ["eth", "bsc"]:
            return Response({"code": 30001, "msg": "please enter the correct network"})
        try:
            contract_meta = fetch_contract_meta(network, address)
        except Exception as e:
            return Response({"code": 30001, "msg": "The service is busy, please try again"})
        if contract_meta.get("ABI") == "Contract source code not verified":
            return Response({"code": 30001, "msg": "Something wrong Please Check contract address or chain network"})
        file_name, src_code = contract_meta['ContractName'], contract_meta['SourceCode']
        if src_code[:4] == '{{\r\n':
            src_txt = write_contract(file_name, src_code)
            src_bin = json.dumps(json.loads(src_code[1:-1])['sources'], ensure_ascii=False).encode()
        else:
            src_txt = src_code
            src_bin = src_code.encode()
        hash = sha1(src_bin).hexdigest()
        data = {"user": request.user.pk, 'file_name': file_name + ".sol", "date": int(time.time()),
                "sha1": hash, "file": src_bin, 'file_type': 'sol', "contract_address": address,
                "network": network, "contract": src_txt
                }
        serializer = WriteDocumentSerializer(data=data)
        if serializer.is_valid():
            save_doc = serializer.save()
            set_queue(save_doc.id)
            return Response({"id": save_doc.id})
        else:
            print(serializer.errors, 'error')
            return Response({"id": None}, status=403)


class UploadContractFile(APIView):
    """
    Uploading contract files Api
    """

    def post(self, request: Request):
        doc = Document.objects.filter(user=self.request.user).defer("file").order_by("-id")
        first = doc.first()
        if first:
            status, resp = checkstatus(doc, first.result)
            if not status:
                return Response(resp)

        upload_file = request.data.get("file")
        upload_file_name = upload_file.name
        main_file = request.data.get("main_file")
        format_zip = upload_file_name.endswith(".zip")
        format_sol = upload_file_name.endswith(".sol")
        if not format_zip and not format_sol:
            return Response({"code": 30001, "msg": "The file is not in zip/sol format"})

        curPath = sys.path[0]
        date = int(time.time())
        save_path = curPath + os.path.sep + "upload_contracts" + os.path.sep + str(date)
        try:
            # save file
            if format_sol:
                contract_path = save_path
                if not main_file:
                    main_file = upload_file_name
                try:
                    os.mkdir(save_path)
                except FileNotFoundError:
                    os.mkdir(curPath + os.path.sep + "upload_contracts")
                    os.mkdir(save_path)
                with open(save_path + os.path.sep + upload_file_name, 'x', encoding='utf-8') as f:
                    f.write(str(upload_file.read(), encoding="utf-8"))
                    f.close()
            else:
                contract_path = save_path + os.path.sep + upload_file_name.split(".")[0]

                # save zip file
                f = zipfile.ZipFile(upload_file, "r")
                if len(f.namelist()) < 2:
                    return Response({"code": 30001, "msg": "Empty folder"})
                for file in f.namelist():
                    f.extract(file, save_path)
                f.close()

            # merge file
            merge = Merge(contract_path, main_file)
            contract = merge.start()
            contract = contract.encode("utf-8")

            # del zip file
            shutil.rmtree(save_path)

            # save to db
            data = {
                "user": request.user.pk,
                "file_name": main_file,
                "date": date,
                "sha1": sha1(contract).hexdigest(),
                "file": contract,
                "file_type": main_file.split('.')[-1],
                "contract": bytes(contract).decode()
            }
            serializer = WriteDocumentSerializer(data=data)
            if serializer.is_valid():
                save_doc = serializer.save()
                set_queue(save_doc.id)
                return Response({"id": save_doc.id})
            else:
                return Response({"id": None}, status=403)
        except Exception as e:
            if "No such file or directory" in str(e):
                return Response({"code": 30001, "msg": "Please upload right file (.sol)"}, status=500)
            return Response({"code": 30001, "msg": "Server error, please try again"}, status=500)


# manage


class DownloadContractFile(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    """
    Download the contract file api
    """

    def get(self, request: Request):
        doc = Document.objects.get(pk=request.query_params['id'])
        file = File(doc.file_name, doc.file, content_type='application/octet-stream')
        return FileResponse(file, as_attachment=True)


class MyFiles(ListAPIView):
    queryset = Document.objects.defer("file")
    serializer_class = ReadDocumentSerializer
    ordering = ['-id']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class QueryResult(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        doc_id = request.query_params.get('id', "")
        document = Document.objects.filter(id=doc_id).first()
        if document:
            results = document.result
            return Response(results)
        return Response({"msg": "No corresponding data"}, status=403)


class CheckStatus(APIView):
    permission_classes = []
    authentication_classes = []
    """
    check the user detection status
    """

    def get(self, request: Request):
        addr = request.GET.get("addr")
        if not addr:
            return Response({"code": "30001", "msg": "Not addr"})
        user = User.objects.filter(wallet_address=addr).first()
        if not user:
            return Response({"code": "30001", "msg": "Not account"})

        doc = Document.objects.filter(user=user).defer("file").order_by("-id")

        first = doc.first()
        if not first:
            return Response({"code": 200, "status": 0})
        # 检查
        status, resp = checkstatus(doc, first.result)
        if not status:
            return Response(resp)
        return Response({"code": 200, "status": 0})


class TotalDetection(APIView):
    permission_classes = []
    authentication_classes = []
    """
    返回检测总数
    """

    def get(self, request: Request):
        count = Document.objects.exclude(contract_address=None).count()
        return Response({"code": 200, "data": 2000 + count})


class MyPageNumberPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100


class DetectionLog(ListAPIView):
    """
    检测log
    """
    permission_classes = []
    authentication_classes = []
    deWeight = """
    select max(id) 
        from api_document 
    WHERE contract_address is NOT null and score is not null 
    group by contract_address having count(*)>=1
    """
    queryset = Document.objects.extra(where=[
        'api_document.id in (%s)' % deWeight
    ])
    serializer_class = DetectionLogSerializer
    pagination_class = MyPageNumberPagination
    ordering = ['-id']

    def get(self, request, *args, **kwargs):
        name = request.GET.get("name")
        queryset = self.queryset
        if name:
            queryset = self.queryset.filter(file_name=name)
            if not queryset.all():
                queryset = self.queryset.filter(contract_address=name)
        self.queryset = queryset
        return self.list(request, *args, **kwargs)


class DetectionDetails(APIView):
    """
    检测详情
    """
    permission_classes = []
    authentication_classes = []

    def get(self, request):
        did = request.GET.get("id")
        if not did:
            return Response({"code": 30001, "msg": "not id"})
        query = Document.objects.filter(id=did).first()
        if not query:
            return Response({"code": 30001, "msg": "not contract"})

        result = query.result
        # corethril = result.get("corethril")
        core_slither = result.get("core_slither")
        # core_smartian = result.get("core_smartian")
        # if (not corethril and corethril != []) or (not core_slither and core_slither != []):
        if not core_slither and core_slither != []:
            status, err = parseErrorResult(did)
            if status:
                return Response({"code": 30001, "msg": err})
            deltaT = cal_time(int(query.date), int(time.time()))
            if deltaT >= (60 * 15):
                result["coreslither_error"] = "Sorry, detection failed, please try again"
                query.result = result
                query.save()
                return Response({"code": 30001, "msg": "Sorry, detection failed, please try again"})
            if deltaT >= config.detectionTimeout:
                return Response({"code": 201, "msg": "under detecting"})
            return Response({"code": 200, "msg": "under detecting"})

        if not query.score:
            # 处理检测数据

            for i in core_slither:
                res_data = {
                    "document_id": did,
                    "title": i.get("check"),
                    "level": i.get("confidence"),
                    "description": i.get("description"),
                    "details": i
                }
                DocumentResult.objects.get_or_create(**res_data)

            # query
            dr_query = DocumentResult.objects.filter(document=query)
            high_count = dr_query.filter(level="High").count()
            medium_count = dr_query.filter(level="Medium").count()
            low_count = dr_query.filter(level="Low").count()
            # title classify
            total_type_detection = 100
            high_type_count = dr_query.filter(level="High").values("title").annotate(Count("title")).count()
            medium_type_count = dr_query.filter(level="Medium").values("title").annotate(Count("title")).count()
            low_type_count = dr_query.filter(level="Low").values("title").annotate(Count("title")).count()
            pass_type_count = total_type_detection - high_type_count - medium_type_count - low_type_count

            high_type_ratio = "%.2f" % (high_type_count / total_type_detection)
            medium_type_ratio = "%.2f" % (medium_type_count / total_type_detection)
            low_type_ratio = "%.2f" % (low_type_count / total_type_detection)
            pass_type_ratio = "%.2f" % (pass_type_count / total_type_detection)
            score_ratio = {
                "result": [
                    {"type": "high", "count": high_count, "ratio": high_type_ratio},
                    {"type": "medium", "count": medium_count, "ratio": medium_type_ratio},
                    {"type": "low", "count": low_count, "ratio": low_type_ratio},
                    {"type": "pass", "count": pass_type_count, "ratio": pass_type_ratio},
                ],
                "time": int(time.time())
            }

            # score = (100/total_detection*low_count) + (50/total_detection*medium_count) - 5
            # if score < 0:
            #     score = 0
            score = float(high_type_ratio) + float(medium_type_ratio)
            query.score = "%.2f" % score
            query.score_ratio = score_ratio
            query.save()
        else:
            dr_query = DocumentResult.objects.filter(document=query)

        query_data = DocumentResultSerializer(dr_query, many=True)

        data = {
            "user": query.user.wallet_address,
            "time": query.score_ratio.get("time", query.date),
            "contract_address": query.contract_address,
            "chain": query.network,
            "score": query.score,
            "score_ratio": query.score_ratio,
            "list": query_data.data
        }
        return Response(data)
