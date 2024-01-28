# -*- coding: utf-8 -*-
"""
@File        : base.py
@Author      : Aug
@Time        : 2023/2/14 10:28
@Description :
"""
import http
import copy
from typing import Any
from pydantic.main import BaseModel


class BaseResponse(BaseModel):
    """base return value"""
    code: int  # code
    msg: str  # message
    data: Any  # return data


SUCCESS_RESPONSE = BaseResponse(code=http.HTTPStatus.OK, msg="success", data=None)
NOTFOUND_RESPONSE = BaseResponse(code=http.HTTPStatus.NOT_FOUND, msg="%s")
ERROR_RESPONSE = BaseResponse(code=30001, msg="%s")


async def success(data=None):
    resp = copy.deepcopy(SUCCESS_RESPONSE)
    resp.data = data
    return resp


async def not_found(msg, code=None):
    resp = copy.deepcopy(NOTFOUND_RESPONSE)
    resp.msg = msg
    if code:
        resp.code = code
    return resp


async def error_found(msg, code=None):
    resp = copy.deepcopy(ERROR_RESPONSE)
    resp.msg = msg
    if code:
        resp.code = code
    return resp
