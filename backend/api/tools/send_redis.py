# -*- coding: utf-8 -*-
"""
@File        : send_redis.py
@Author      : JunL
@Time        : 2023/5/25 21:18
@Description :
"""
import json

from api.tools.redis_conn import get_redis


def send_pub_redis(detect_id, medium_risk, high_risk, address):
    res = {
        "detect_id": detect_id,
        "medium_risk": medium_risk,
        "high_risk": high_risk,
        "address": address,
        "detect_type": 3,
    }
    rds = get_redis()
    rds.publish(f"static:{address}", json.dumps(res))
    print(f"publish: {address}")
