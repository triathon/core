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
from django.http import FileResponse
from django_redis import get_redis_connection
from eth_account.messages import encode_defunct
from hexbytes import HexBytes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from web3.auto import w3

from api.models import Document, User
from api.serializers import WriteDocumentSerializer, ReadDocumentSerializer
from api.tools.contract_helper import fetch_contract_meta, write_contract
from conf import config
from api.tools.merge_contract import Merge

rd = get_redis_connection()


def set_queue(d_id):
    rd.lpush(config.coreslither_queue, d_id)
    rd.lpush(config.corethril_queue, d_id)
    rd.lpush(config.coresmartian_queue, d_id)


class SubmitContractAddress(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request: Request):
        network, address = request.data['network'], request.data['address']
        contract_meta = fetch_contract_meta(network, address)
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
            doc = serializer.save()
            set_queue(doc.id)
            return Response({"id": doc.id})
        else:
            print(serializer.errors, 'error')
            return Response({"id": None}, status=403)


class UploadContractFile(APIView):
    """
    Uploading contract files Api
    """
    def post(self, request: Request):
        upload_file = request.data.get("file")
        upload_file_name = upload_file.name
        main_file = request.data.get("main_file")
        format_zip = upload_file_name.endswith(".zip")
        format_sol = upload_file_name.endswith(".sol")
        if not format_zip and not format_sol:
            return Response({"code": 301, "msg": "The file is not in zip/sol format"})

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
                    return Response({"code": 302, "msg": "Empty folder"})
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
                doc = serializer.save()
                set_queue(doc.id)
                return Response({"id": doc.id})
            else:
                return Response({"id": None}, status=403)
        except:
            print(traceback.print_exc())
            return Response({"code": 500, "msg": "Server error, please try again"}, status=500)


class DownloadContractFile(APIView):
    """
    Download the contract file api
    """

    def get(self, request: Request):
        doc = Document.objects.get(pk=request.query_params['id'])
        if doc.user == request.user:
            file = File(doc.file_name, doc.file, content_type='application/octet-stream')
            return FileResponse(file, as_attachment=True)
        return Response({"msg": "you don't own this file"}, status=403)


class MyFiles(ListAPIView):
    queryset = Document.objects.defer("file")
    serializer_class = ReadDocumentSerializer
    ordering = ['-id']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


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
