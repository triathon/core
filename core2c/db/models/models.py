# -*- coding: utf-8 -*-
"""
@File        : models.py
@Author      : Aug
@Time        : 2023/2/13 15:41
@Description :
"""
import math
import random
from tortoise import fields
from tortoise.models import Model


class UserDetection(Model):
    id = fields.IntField(pk=True)
    address = fields.CharField(max_length=255, description="检测地址")
    user_address = fields.CharField(max_length=255, description="用户钱包地址")
    chain = fields.CharField(max_length=30, description="链类型")
    type = fields.IntField(description="1 token检测 2token授权检测 3erc721授权检测 4nft检测")
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_time = fields.DatetimeField(auto_now=True, null=True, description="修改时间")
    status = fields.CharField(max_length=10, default="0", description="0检测中1检测成功2检测失败")
    medium_risk = fields.IntField(null=True)
    high_stake = fields.IntField(null=True)

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
    cs_medium_risk = fields.IntField(null=True)
    cs_high_stake = fields.IntField(null=True)
    ts_medium_risk = fields.IntField(null=True)
    ts_high_stake = fields.IntField(null=True)
    ts_sell_tax = fields.TextField(null=True)
    ts_is_honeypot = fields.IntField(null=True)
    ts_slippage_modifiable = fields.IntField(null=True)
    honeypot = fields.IntField(null=True)

    class Meta:
        table = "token_detection"
        table_description = "token检测"


class NftDetection(Model):
    id = fields.IntField(pk=True)
    user_detection = fields.ForeignKeyField("models.UserDetection", on_delete=fields.CASCADE)
    logo = fields.CharField(max_length=255, null=True)
    name = fields.CharField(max_length=255, null=True)

    # Basic info
    nft_erc = fields.CharField(max_length=255, null=True)
    owner_addr = fields.CharField(max_length=255, null=True)

    # data change with time
    # Trading and Holding
    trading_holding = fields.JSONField(null=True)
    # Security (0 not risk,1 risk)
    authenticity = fields.JSONField(null=True)
    trading_security = fields.JSONField(null=True)

    risks = fields.JSONField(null=True)
    error = fields.TextField(null=True)

    class Meta:
        table = "nft_detection"
        table_description = "nft检测结果"


def discretize(x):
    discrete_value = math.floor(8 / (1 + math.exp(-x))) + 1
    return discrete_value


def random_num():
    x = random.randint(1, 5)
    return x


class DetectionTotalCount(Model):
    id = fields.IntField(pk=True)
    user_detection = fields.ForeignKeyField("models.UserDetection", on_delete=fields.CASCADE)
    type = fields.IntField(default=1, description="1 钱包检测 2token/nft检测")
    num = fields.IntField(default=random_num)

    class Meta:
        table = "detect_total_count"
        table_description = "检测总数"
