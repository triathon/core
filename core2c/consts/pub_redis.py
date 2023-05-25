# -*- coding: utf-8 -*-
"""
@File        : pub_redis.py
@Author      : JunL
@Time        : 2023/5/25 21:51
@Description :
"""
import json
from consts.redis_conn import get_redis


async def send_pub_redis(detect_id, medium_risk, high_risk, address):
    res = {
        "detect_id": detect_id,
        "medium_risk": medium_risk,
        "high_risk": high_risk,
        "address": address,
        "detect_type": 1,
    }
    rds = get_redis()
    rds.publish(f"token_nft:{address}", json.dumps(res))
