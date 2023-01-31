# -*- coding: utf-8 -*-
"""
@File        : deltaT.py
@Author      : Aug
@Time        : 2023/1/31 14:43
@Description :
"""

import datetime
import time


def cal_time(stamp1, stamp2):
    """
    :param stamp1: 历史时间
    :param stamp2: 现在时间
    """
    t1 = time.localtime(stamp1)
    t2 = time.localtime(stamp2)
    t1 = time.strftime("%Y-%m-%d %H:%M:%S", t1)
    t2 = time.strftime("%Y-%m-%d %H:%M:%S", t2)
    time1 = datetime.datetime.strptime(t1, "%Y-%m-%d %H:%M:%S")
    time2 = datetime.datetime.strptime(t2, "%Y-%m-%d %H:%M:%S")
    return (time2 - time1).seconds
