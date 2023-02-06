# -*- coding: utf-8 -*-
"""
@File        : verify_submit_status.py
@Author      : Aug
@Time        : 2023/1/16 12:27
@Description :
"""
import datetime
import time

from conf import config
from api.tools import detection_result

# 每日检测次数
number_of_detection = config.number_of_detection


def checkstatus(doc, result):
    """
    :return :
        0没问题1正在检测2检测超次数
    """
    if check_whether_there_is_detect(doc, result):
        first = doc.first()
        return False, {"code": 200, "status": 1, "msg": "one is currently being detected", "id": first.id}

    zero = int(time.mktime(time.strptime(str(datetime.date.today()), '%Y-%m-%d')))
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    last = int(time.mktime(time.strptime(str(tomorrow), '%Y-%m-%d'))) - 1
    count = doc.filter(date__gte=zero, date__lte=last).count()
    print("几次", count)
    if check_detection_numberOfTimes(count):
        return False, {"code": 200, "status": 2,
                       "msg": f"This version is limited to three times a day, please try again tomorrow"}
    return True, ""


def check_whether_there_is_detect(doc, result):
    """检查是否有正在检测中的
    :param doc:
    """
    core_slither = result.get("core_slither")

    if doc.filter(result={}).exists():
        return True
    status, _ = detection_result.parseErrorResult(doc.first().id)
    if status:
        return False
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