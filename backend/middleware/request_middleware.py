# -*- coding: utf-8 -*-
"""
@File        : request_middleware.py
@Author      : Aug
@Time        : 2023/1/12 19:10
@Description :
"""
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from conf import logger


class RequestMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        """
        override return logic
        @param request:
        @param response:
        @return:
        """
        resp = {}
        if isinstance(response, Response):
            if str(response.status_code)[:1] == "2":
                data = response.data
                if data is None:
                    data = {}
                if isinstance(data, list):
                    resp["code"] = status.HTTP_200_OK
                    resp["msg"] = "ok"
                    resp["data"] = data
                    response.data = resp
                    response._is_rendered = False
                    response.render()
                    return response
                code = response.status_code
                if response.status_code == 204:
                    code = 200
                msg = "ok"
                if "code" in data:
                    code = data.pop("code")
                if "msg" in data:
                    msg = data.pop("msg")
                resp["code"] = code
                resp["msg"] = msg
                if "data" in data.keys() and len(data.keys()) == 1:
                    resp["data"] = data.pop("data")
                else:
                    resp["data"] = data
                response.data = resp
            elif response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
                resp["code"] = response.data.get("code", status.HTTP_500_INTERNAL_SERVER_ERROR)
                resp["msg"] = response.data.get("msg", "")
                resp["data"] = None
                response.data = resp
            elif response.status_code == status.HTTP_400_BAD_REQUEST:
                resp["code"] = response.status_code
                resp["msg"] = f"Parameter is missing or does not meet specifications, please check {response.data}"
                # k = [k for k in response.data][0]
                # resp["msg"] = f"{k}{response.data.get(k)[0]}"
                if response.data[0]:
                    resp["msg"] = response.data[0]
                resp["data"] = None
                response.data = resp
            elif response.status_code == status.HTTP_401_UNAUTHORIZED:
                resp["code"] = response.status_code
                resp["msg"] = "Please login"
                resp["data"] = None
                response.data = resp
            elif response.status_code == status.HTTP_403_FORBIDDEN:
                resp["code"] = response.status_code
                resp["msg"] = "The service is busy, please try again"
                resp["data"] = None
                response.data = resp
            else:
                resp["code"] = response.status_code
                resp["msg"] = "The service is busy, please try again"
                resp["data"] = None
                response.data = resp
            print(f'code:{response.status_code}')
            response.status_code = status.HTTP_200_OK
            response._is_rendered = False
            response.render()
        return response

    def process_exception(self, request, exception):
        """
        catch exception
        @param request:
        @param exception:
        @return:
        """
        resp = {}
        if isinstance(exception, AuthenticationFailed):
            resp["code"] = status.HTTP_403_FORBIDDEN
            resp["msg"] = "Login Failed"
        else:
            resp["code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            resp["msg"] = f"The service is busy, please try again."
        resp["data"] = None
        logger.error(f"错误信息:{str(exception)}")
        response = JsonResponse(data=resp, status=status.HTTP_200_OK)
        import traceback
        traceback.print_exc()
        return response
