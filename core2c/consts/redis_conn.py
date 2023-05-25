# -*- coding: utf-8 -*-
"""
@File        : redis_conn.py
@Author      : JunL
@Time        : 2023/5/10 16:30
@Description :
"""
import redis
from conf import config as cf


def get_redis():
    """
    redis connect
    :return:
    """
    config = cf.get("test_mining")
    conn_pool = redis.ConnectionPool(
        host=config.get("redis_host"),
        port=config.get("redis_port"),
        password=config.get("redis_password"),
        decode_responses=True,
        db=config.get("redis_db"),
    )
    rds = redis.Redis(connection_pool=conn_pool)
    return rds
