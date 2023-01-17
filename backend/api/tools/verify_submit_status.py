# -*- coding: utf-8 -*-
"""
@File        : verify_submit_status.py
@Author      : Aug
@Time        : 2023/1/16 12:27
@Description :
"""
from conf import config
from api.tools import detection_result

number_of_detection = config.number_of_detection


def checkstatus(doc, result):
    if check_whether_there_is_detect(doc, result):
        first = doc.first()
        return False, {"code": 200, "status": 1, "msg": "one is currently being detected", "id": first.id}

    if check_detection_numberOfTimes(doc.count()):
        return False, {"code": 200, "status": 2, "msg": f"{number_of_detection} have been detected"}
    return True, ""


def check_whether_there_is_detect(doc, result):
    """检查是否有正在检测中的
    :param doc:
    """
    corethril = result.get("corethril")
    core_slither = result.get("core_slither")

    if doc.filter(result={}).exists():
        return True
    status, _ = detection_result.parseErrorResult(doc.first().id)
    if status:
        return False
    if not corethril and corethril != []:
        return True
    if not core_slither and core_slither != []:
        return True
    return False


def check_detection_numberOfTimes(count):
    """
    检查检测次数是否超标
    """
    if count >= number_of_detection:
        return True
    return False