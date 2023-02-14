# -*- coding: utf-8 -*-
"""
@File        : models.py
@Author      : Aug
@Time        : 2023/2/13 15:41
@Description :
"""

from tortoise import fields
from tortoise.models import Model


class UserDetection(Model):
    id = fields.IntField(pk=True)
    address = fields.CharField(max_length=255, description="检测地址")
    user_address = fields.CharField(max_length=255, description="用户钱包地址")
    chain = fields.CharField(max_length=30, description="链类型")
    type = fields.IntField(description="1 token检测")
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    status = fields.CharField(max_length=10, default="0")

    class Meta:
        table = "user_detection"
        table_description = "用户检测"


class TokenDetection(Model):
    id = fields.IntField(pk=True)
    user_detection = fields.ForeignKeyField("models.UserDetection", on_delete=fields.CASCADE)
    logo = fields.CharField(max_length=255, null=True)
    name = fields.CharField(max_length=255, null=True)

    # Summary
    creater_addr = fields.CharField(max_length=255, null=True)
    owner_addr = fields.CharField(max_length=255, null=True)

    # Token overview
    total_supply = fields.CharField(max_length=255, null=True)
    holder_count = fields.CharField(max_length=255, null=True)
    top10_holders = fields.JSONField(description="Top10 holders info", null=True)
    top10_lp_token = fields.JSONField(description="Top10 LP token holders info", null=True)
    # data change with time
    contract_security = fields.JSONField(null=True)
    trading_security = fields.JSONField(null=True)
    error = fields.TextField(null=True)

    class Meta:
        table = "token_detection"
        table_description = "token检测"
