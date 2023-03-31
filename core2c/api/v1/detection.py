# -*- coding: utf-8 -*-
"""
@File        : detection.py
@Author      : Aug
@Time        : 2023/2/13 15:53
@Description :
"""
import datetime
import json
import time
from pathlib import Path

import requests
from fastapi import APIRouter, Body
from typing import Optional

from db.models import models
from conf import logger, config
from consts import success, error_found

detection_router = APIRouter(prefix='')

chain_type = {
    "ETH": "1",
    "BSC": "56",
    "Tron": "tron",
    "Polygon": "137",
    "Avalanche": "43114",
    "Optimism": "10",
}

nft_security = config['goplus_api'].get("nft_security")

# token detection key
contract_security_key = (
    "is_proxy", "is_mintable", "can_take_back_ownership", "owner_change_balance",
    "hidden_owner", "selfdestruct", "external_call",
)
contract_high_stake = ("is_proxy", "owner_change_balance", "selfdestruct",)
contract_medium_risk = ("is_mintable", "can_take_back_ownership", "hidden_owner", "external_call",)

trading_security_key = (
    "is_honeypot", "transfer_pausable", "cannot_sell_all", "cannot_buy",
    "trading_cooldown", "is_anti_whale", "anti_whale_modifiable", "slippage_modifiable",
    "is_blacklisted", "is_whitelisted", "personal_slippage_modifiable",
)
trading_high_stake = ("is_honeypot", "transfer_pausable", "cannot_sell_all", "slippage_modifiable", "personal_slippage_modifiable")
trading_medium_risk = ("cannot_buy", "trading_cooldown", "is_anti_whale", "anti_whale_modifiable", "is_blacklisted", "is_whitelisted")

# nft detection key


async def goplus_detection(url):
    """
    goplus toen detection
    :param url: url
    """
    try:
        print(url)
        content = requests.get(url).json()
        return content
    except Exception:
        logger.exception('extract_goplus_info error')
        return None


async def get_dict(dict_keys, data):
    result = {}
    for k in dict_keys:
        if data.get(k):
            result[k] = data.get(k)
    return result


async def get_risk_count(dict_keys, data):
    count = 0
    for k in dict_keys:
        if data.get(k) == "1":
            count += 1
    return count


async def save_token_detection_result(content, token_address, user_detection_id):
    """
    save token detection result
    :param content: detection result
    :param token_address: token address
    :param user_detection_id: token address
    """
    token, _ = await models.TokenDetection.get_or_create(user_detection_id=user_detection_id)
    try:
        result = content.get("result").get(token_address.lower())
        if not result:
            msg = "Something wrong, please check（There may be the following reasons: wrong chain, wrong address, the contract is not open source）"
            token.error = msg
            await token.save()
            return False, _, msg
        is_open_source = result.get("is_open_source")
        if is_open_source == "0":
            msg = "Something wrong, please check（There may be the following reasons: wrong chain, wrong address, the contract is not open source）"
            token.error = msg
            await token.save()
            return False, _, msg

        contract_security = {'is_open_source': "0"}
        cs_result = await get_dict(contract_security_key, result)
        contract_security = dict(contract_security, **cs_result)
        contract_security["high_stake"] = await get_risk_count(contract_high_stake, result)
        contract_security["medium_risk"] = await get_risk_count(contract_medium_risk, result)

        tax_risk_type = 0
        if result.get("is_in_dex") == 0:
            trading_security = {}
        else:
            buy_tax = result.get("buy_tax", '0')
            sell_tax = result.get("sell_tax", '0')
            trading_security = {"buy_tax": buy_tax, "sell_tax": sell_tax}
            if float(buy_tax)*100 > 1 or float(sell_tax)*100 > 1:
                tax_risk_type = 2
            elif float(buy_tax)*100 > 0 or float(sell_tax)*100 > 0:
                tax_risk_type = 1
        ts_result = await get_dict(trading_security_key, result)
        trading_security = dict(trading_security, **ts_result)
        trading_high_stake_count = await get_risk_count(trading_high_stake, result)
        trading_medium_risk_count = await get_risk_count(trading_medium_risk, result)
        trading_security["high_stake"] = trading_high_stake_count+1 if tax_risk_type == 2 else trading_high_stake_count
        trading_security["medium_risk"] = trading_medium_risk_count+1 if tax_risk_type == 1 else trading_medium_risk_count

        token.logo = result.get("token_symbol")
        token.name = result.get("token_name")

        token.creater_addr = result.get("creator_address")
        token.owner_addr = result.get("owner_address")

        token.total_supply = result.get("total_supply")
        token.holder_count = result.get("holder_count")
        token.top10_holders = json.dumps({"result": result.get("holders")})
        token.top10_lp_token = json.dumps({"result": result.get("lp_holders")})

        token.contract_security = json.dumps(contract_security)
        token.trading_security = json.dumps(trading_security)

        await token.save()
        return True, token, "ok"
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error("save_token_detection_result error: %s" % str(e))
        return False, _, _


async def token_detection_details(query):
    """
    get token detection details
    """
    token_query = await models.TokenDetection.filter(user_detection_id=query.id).first()

    # percent +
    top10_holders = token_query.top10_holders.get("result")
    top10_lp_token = token_query.top10_lp_token.get("result")
    top10_holders_percent = 0
    if top10_holders:
        for i in top10_holders:
            top10_holders_percent += float(i.get("percent"))
    top10_lp_token_percent = 0
    if top10_lp_token:
        for i in top10_lp_token:
            top10_lp_token_percent += float(i.get("percent"))

    # time utc
    time_struct = int(time.mktime(query.create_time.timetuple()))
    utc_time = datetime.datetime.utcfromtimestamp(time_struct-28800).strftime("UTC %d/%m/%Y %H:%M:%S")

    # risk
    if token_query.contract_security:
        high_risk = token_query.contract_security.get("high_stake", 0)
        medium_risk = token_query.contract_security.get("medium_risk", 0)
        if token_query.trading_security:
            high_risk += token_query.trading_security.get("high_stake", 0)
            medium_risk += token_query.trading_security.get("medium_risk", 0)
    else:
        high_risk = 0
        medium_risk = 0

    if high_risk == 0 and medium_risk > 0:
        risk_outcome = "1"  # medium risk
    elif high_risk > 0:
        risk_outcome = "2"  # high risk
    else:
        risk_outcome = "0"  # low risk

    # result
    result = {
        "id": token_query.id,
        "detection_user": query.user_address,
        "detection_time": utc_time,
        "logo": token_query.logo,
        "token_name": token_query.name,
        "summary": {
            "chain": query.chain,
            "address": query.address,
            "creater_addr": token_query.creater_addr,
            "owner_addr": token_query.owner_addr,
        },
        "token_overview": {
            "total_supply": token_query.total_supply,
            "holder_count": token_query.holder_count,
            "top10_holders": top10_holders,
            "top10_holders_percent": top10_holders_percent,
            "top10_lp_token": top10_lp_token,
            "top10_lp_token_percent": top10_lp_token_percent
        },
        "contract_security": token_query.contract_security,
        "trading_security": token_query.trading_security,
        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "risk_outcome": risk_outcome
    }
    return result


async def check_risk_value(key, num, correct_value=0):
    """
    check risk update value/risk num
    """
    if key == correct_value:
        value = 0
    else:
        num += 1
        value = 1
    return value, num


async def save_nft_detection_result(content, user_detection_id):
    """
    save nft detection result
    :param content: detection result
    :param user_detection_id: token address
    """
    error_msg = "Something wrong, please check（There may be the following reasons: wrong chain," \
                " wrong address, the contract is not open source）"
    detect, _ = await models.NftDetection.get_or_create(user_detection_id=user_detection_id)
    try:
        result = content.get("result")
        if not result:
            return False, _, error_msg
        is_open_source = result.get("is_open_source")
        if not result or is_open_source == "0":
            detect.error = error_msg
            await detect.save()
            return False, _, error_msg

        trading_holding = {
            "nft_items": result.get("nft_items"),
            "nft_owner_number": result.get("nft_owner_number"),
            "average_price_24h": result.get("average_price_24h"),
            "lowest_price_24h": result.get("lowest_price_24h"),
            "sales_24h": result.get("sales_24h"),
            "traded_volume_24h": result.get("traded_volume_24h"),
            "total_volume": result.get("total_volume"),
            "highest_price": result.get("highest_price")
        }

        # risk
        medium_risk, high_risk = 0, 0

        nft_verified = result.get("nft_verified")
        same_nfts = result.get("same_nfts")

        nft_verified, medium_risk = await check_risk_value(nft_verified, medium_risk, 1)
        same_nfts, high_risk = await check_risk_value(same_nfts, high_risk, "null")
        authenticity = {
            "nft_verified": nft_verified,
            "same_nfts": same_nfts
        }

        nft_open_source = result.get("nft_open_source")
        nft_proxy = result.get("nft_proxy")
        malicious_nft_contract = result.get("malicious_nft_contract")
        privileged_burn = result.get("privileged_burn")
        transfer_without_approval = result.get("transfer_without_approval")
        privileged_minting = result.get("privileged_minting")
        self_destruct = result.get("self_destruct")
        restricted_approval = result.get("restricted_approval")

        nft_open_source, high_risk = await check_risk_value(nft_open_source, high_risk, 1)
        nft_proxy, medium_risk = await check_risk_value(nft_proxy, medium_risk)
        malicious_nft_contract, high_risk = await check_risk_value(malicious_nft_contract, high_risk)

        privileged_burn, high_risk = await check_risk_value(privileged_burn.get('value'), high_risk)
        transfer_without_approval, high_risk = await check_risk_value(transfer_without_approval.get('value'), high_risk)
        privileged_minting, medium_risk = await check_risk_value(privileged_minting.get('value'), medium_risk)
        self_destruct, high_risk = await check_risk_value(self_destruct.get('value'), high_risk)

        restricted_approval, high_risk = await check_risk_value(restricted_approval, high_risk)

        trading_security = {
            "nft_open_source": nft_open_source,
            "nft_proxy": nft_proxy,
            "malicious_nft_contract": malicious_nft_contract,
            "privileged_burn": privileged_burn,
            "transfer_without_approval": transfer_without_approval,
            "privileged_minting": privileged_minting,
            "self_destruct": self_destruct,
            "restricted_approval": restricted_approval
        }

        risk_result = "low risk"
        if high_risk == 0 and medium_risk > 0:
            risk_result = "medium risk"
        elif high_risk > 0:
            risk_result = "high risk"
        risks = {
            "high_risk": high_risk,
            "medium_risk": medium_risk,
            "risk_result": risk_result
        }
        # -- update data
        detect.logo = result.get("nft_symbol")
        detect.name = result.get("nft_name")

        detect.nft_erc = result.get("nft_erc")
        detect.owner_addr = result.get("owner_address")

        detect.trading_holding = json.dumps(trading_holding)
        detect.authenticity = json.dumps(authenticity)
        detect.trading_security = json.dumps(trading_security)
        detect.risks = json.dumps(risks)

        await detect.save()
        return True, detect, "ok"
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error("save_nft_detection_result error: %s" % str(e))
        return False, _, _


async def nft_detection_details(query):
    """
    get nft detection details
    """
    detect_query = await models.NftDetection.filter(user_detection_id=query.id).first()

    # time utc
    time_struct = int(time.mktime(query.create_time.timetuple()))
    utc_time = datetime.datetime.utcfromtimestamp(time_struct-28800).strftime("UTC %d/%m/%Y %H:%M:%S")

    # result
    result = {
        "id": detect_query.id,
        "detection_user": query.user_address,
        "detection_time": utc_time,
        "logo": detect_query.logo,
        "token_name": detect_query.name,

        "detect_chain": query.chain,
        "detect_address": query.address,
        "nft_stand": detect_query.nft_erc,
        "owner_addr": detect_query.owner_addr,

        "trading_holding": detect_query.trading_holding,
        "authenticity": detect_query.authenticity,
        "trading_security": detect_query.trading_security,

        "risk": detect_query.risks
    }
    return result
# --- api


@detection_router.get('/detection_total')
async def total():
    """
    detection total
    """
    count = await models.TokenDetection.all().count()
    return await success({"total": 3000 + int(count)})


@detection_router.get("/detection_status")
async def status(
        user_address: str
):
    """
    get detection status
    """
    data = {"status": "0"}
    user_detection = await models.UserDetection.filter(user_address=user_address, status="0", type=1).first()
    if user_detection:
        data = {"status": "1", "address": user_detection.address, "chain": user_detection.chain}
    return await success(data)


@detection_router.post('/token_detection')
async def token_detection(
        user_address: str = Body(None),
        token_address: str = Body(None),
        chain: Optional[str] = Body("BSC"),
):
    """
    home search
    :param user_address:用户钱包地址
    :param token_address:token地址
    :param chain:
    :return:
    """
    if not user_address:
        return await error_found("no user address")
    if not token_address:
        return await error_found("no token address")
    chain_id = chain_type.get(chain)
    if not chain_id or chain_id is None:
        return await error_found("This chain is not supported yet/ chain error")

    user_detection, _ = await models.UserDetection.get_or_create(
        address=token_address,
        user_address=user_address,
        chain=chain,
        type=1
    )

    content = await goplus_detection(
        config['goplus_api'].get("token_security").format(chain=chain, token_address=token_address))
    if not content:
        return await error_found("detection failure")
    status, _, msg = await save_token_detection_result(content, token_address, user_detection.id)
    user_detection.create_time = datetime.datetime.now()
    if status:
        user_detection.status = "1"
        await user_detection.save()
        result = await token_detection_details(user_detection)
        return await success(result)
    else:
        user_detection.status = "2"
        await user_detection.save()
        return await error_found(msg)


@detection_router.get("/token_detection/{pk}")
async def get_token_detection(
        pk: str
):
    token_query = await models.TokenDetection.filter(id=pk).order_by("-id").first()
    if not token_query:
        return await error_found("not token address")
    query = await models.UserDetection.filter(id=token_query.user_detection_id, type=1).order_by("-id").first()
    if query.status == "0":
        return await error_found("be testing")
    elif query.status == "2":
        return await error_found(token_query.error)
    result = await token_detection_details(query)
    return await success(result)


@detection_router.post('/nft_detection')
async def nft_detection(
        user_address: str = Body(None),
        detect_address: str = Body(None),
        chain: Optional[str] = Body("BSC"),
):
    """
    home search
    :param user_address:用户钱包地址
    :param detect_address:检测地址
    :param chain:
    :return:
    """
    if not user_address:
        return await error_found("no user address")
    if not detect_address:
        return await error_found("no detect address")
    if chain not in ["ETH", "BSC", "Polygon"]:
        return await error_found("This chain is not supported yet/ chain error")

    chain_id = chain_type.get(chain)
    if not chain_id or chain_id is None:
        return await error_found("This chain is not supported yet/ chain error")

    user_detection, _ = await models.UserDetection.get_or_create(
        address=detect_address,
        user_address=user_address,
        chain=chain,
        type=4
    )

    content = await goplus_detection(
        config['goplus_api'].get("nft_security").format(chain=chain_id, addresses=detect_address))
    if not content:
        return await error_found("detection failure")
    status, _, msg = await save_nft_detection_result(content, user_detection.id)
    user_detection.create_time = datetime.datetime.now()
    if status:
        user_detection.status = "1"
        await user_detection.save()
        result = await nft_detection_details(user_detection)
        return await success(result)
    else:
        user_detection.status = "2"
        await user_detection.save()
        return await error_found(msg)


@detection_router.get("/nft_detection/{pk}")
async def get_nft_detection(
        pk: str
):
    token_query = await models.NftDetection.filter(id=pk).order_by("-id").first()
    if not token_query:
        return await error_found("not nft address")
    query = await models.UserDetection.filter(id=token_query.user_detection_id, type=4).order_by("-id").first()
    if query.status == "0":
        return await error_found("be testing")
    elif query.status == "2":
        return await error_found(token_query.error)
    result = await nft_detection_details(query)
    return await success(result)
