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
    """基础返回值"""
    code: int  # 状态码
    msg: str  # 信息
    data: Any  # 返回数据


SUCCESS_RESPONSE = BaseResponse(code=http.HTTPStatus.OK, msg="success", data=None)  # 成功的http返回结构
NOTFOUND_RESPONSE = BaseResponse(code=http.HTTPStatus.NOT_FOUND, msg="%s")  # 404的http返回结构
ERROR_RESPONSE = BaseResponse(code=30001, msg="%s")  # 30001的http返回结构


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
