import json
import time
from copy import deepcopy
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
from api.tools.contract_helper import fetch_contract_meta
from conf import config

rd = get_redis_connection()


def set_queue(d_id):
    rd.lpush(config.coreslither_queue, d_id)
    rd.lpush(config.corethril_queue, d_id)


class SubmitContractAddress(APIView):
    
    def post(self, request: Request):
        network, address = request.data['network'], request.data['address']
        contract_meta = fetch_contract_meta(network, address)
        file_name, src_code = contract_meta['ContractName'], contract_meta['SourceCode']
        if src_code[:4] == '{{\r\n':
            # todo: merge sol files
            src_txt = src_code
            src_bin = json.dumps(json.loads(src_code[1:-1])['sources'], ensure_ascii=False).encode()
        else:
            src_txt = src_code
            src_bin = src_code.encode()
        hash = sha1(src_code).hexdigest()
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
            return Response({"id": None}, status=403)


class UploadContractFile(APIView):
    
    def post(self, request: Request):
        file = request.data['file']
        hash = sha1(deepcopy(file).read()).hexdigest()
        data = {"user": request.user.pk, 'file_name': file.name, "date": int(time.time()),
                "sha1": hash, "file": deepcopy(file).read(), 'file_type': file.name.split('.')[-1],
                "contract": bytes(file.read()).decode()
                }
        serializer = WriteDocumentSerializer(data=data)
        if serializer.is_valid():
            doc = serializer.save()
            set_queue(doc.id)
            return Response({"id": doc.id})
        else:
            return Response({"id": None}, status=403)


class DownloadContractFile(APIView):
    
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
        user, created = User.objects.get_or_create(wallet_address=address)
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
