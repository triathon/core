# -*- coding: utf-8 -*-
"""
@File        : detection_result.py
@Author      : Aug
@Time        : 2023/1/16 18:31
@Description :
"""
from django_redis import get_redis_connection

from api.models import Document
from conf import config

rd = get_redis_connection()


def parseErrorResult(did) -> (bool, str):
    """
    处理检测异常数据
    did
    return:
        whether there is an anomaly：True/ False
    """
    query = Document.objects.filter(id=did).first()
    result = query.result
    count = 0
    error = ""

    # slither
    rd_slither_key = config.coreslither_queue+"Set"
    slither_status = rd.hget(rd_slither_key, f"{did}status")
    # error
    if not result.get("coreslither_error"):
        if slither_status == "2":
            slither_error = rd.hget(rd_slither_key, f"{did}error")
            result["coreslither_error"] = slither_error
            count += 1
            error = slither_error

    else:
        count += 1
        error = result.get("coreslither_error")

    # mythril
    rd_thril_key = config.corethril_queue+"Set"
    thril_status = rd.hget(rd_thril_key, f"{did}status")
    # error
    if not result.get("coremythril_error"):
        if thril_status == "2":
            mythril_error = rd.hget(rd_thril_key, f"{did}error")
            result["coremythril_error"] = mythril_error
            count += 1
            if error == "":
                error = mythril_error
    else:
        count += 1
        if error == "":
            error = result.get("coremythril_error")

    # smartian
    rd_smartian_key = config.coresmartian_queue+"Set"
    smartian_status = rd.hget(rd_smartian_key, f"{did}status")
    # error
    if not result.get("coresmartian_error"):
        if smartian_status == "2":
            smartian_error = rd.hget(rd_smartian_key, f"{did}error")
            result["coresmartian_error"] = smartian_error

    query.result = result
    query.save()

    if count > 0:
        return True, error
    return False, ""

