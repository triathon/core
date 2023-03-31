# -*- coding: utf-8 -*-
"""
@File        : wallet_detect.py
@Author      : Aug
@Time        : 2023/3/14 16:26
@Description : Approval Security
"""
import datetime

import requests
from fastapi import APIRouter, Body
from typing import Optional

from db.models import models
from conf import logger, config
from consts import success, error_found

wallet_detect_router = APIRouter(prefix='/wallet_detect')

chain_type = {
    "ETH": "1",
    "BSC": "56"
}

risk_msg = {
    "is_contract": "Attention,this is not a contract address.",
    "is_open_source": "This contract is not open source."
}


async def goplus_wallet_detect(chain, addresses, option=2):
    """
    goplus wallet detection
    :param chain: chain id
    :param addresses: addresses
    :param option: 2 token 3 erc721
    """
    try:
        if option == 2:
            url = config['goplus_api'].get("token_approval_security").format(chain=chain, addresses=addresses)
        elif option == 3:
            url = config['goplus_api'].get("nft721_approval_security").format(chain=chain, addresses=addresses)
        content = requests.get(url).json()
        return content
    except Exception:
        logger.exception('extract_goplus_info error')
        return None

# Approval security risk data process


async def token_process_data(content):
    """
    token process data
    """
    if not content:
        return False, "not result"
    content_result = content.get("result")
    if not content_result:
        return False, "not result"

    count_risk = 0
    token_res = []
    asset_count_risk = 0
    token_asset_res = []
    for v in content_result:
        # approval
        chain_id = v.get("chain_id", 56)
        token_name = ''.join(v.get("token_name").split('\b'))
        token_address = v.get("token_address")
        token_symbol = v.get("token_symbol")
        balance = v.get("balance")
        # asset
        malicious_address = v.get("malicious_address")
        is_open_source = v.get("is_open_source")
        for item in v.get("approved_list"):
            # approval
            contract = item.get("approved_contract")
            approved_amount = item.get("approved_amount")
            address_info = item.get("address_info")

            malicious_behavior = address_info.get("malicious_behavior")
            # increased risk item
            for risk_key, msg in risk_msg.items():
                if address_info.get(risk_key) == 0:
                    malicious_behavior.append(msg)

            risk = len(malicious_behavior)
            count_risk += risk
            res_dict = {
                "project": address_info.get("contract_name"),
                "contract": contract,
                "chain": chain_id,
                "token": token_name,
                "token_address": token_address,
                "token_symbol": token_symbol,
                "balance": balance,
                "approved_amount": approved_amount,
                "advice": 0 if risk < 1 else 1,
                "risk": risk,
                "malicious_behavior": malicious_behavior
            }
            token_res.append(res_dict)

            # asset
            deployed_time = address_info.get("deployed_time")
            safety_tips = []
            if is_open_source == 0:
                asset_count_risk += 1
                safety_tips.append("This contract is not open source.")
            elif malicious_address == 1:
                safety_tips = malicious_behavior
            asset_count_risk += risk
            asset_res_dict = {
                "asset_name": token_name,
                "symbol": token_name,
                "safety_tips": safety_tips,
                "chain_id": chain_id,
                "type": "ERC-20",
                "contract_address": token_address,
                "balance": balance,
                "advice": "Safe" if asset_count_risk < 1 else "Caution" if asset_count_risk == 1 else "Do not trade",
                "deployed_time": deployed_time
            }
            token_asset_res.append(asset_res_dict)

    result = {
        # approval
        "count_risk": count_risk,
        "result": token_res,
        # asset
        "asset_count_risk": asset_count_risk,
        "asset_result": token_asset_res
    }
    return True, result


async def token_detect_result(chain_id, user_address):
    content = await goplus_wallet_detect(chain_id, user_address)
    return await token_process_data(content)


async def nft721_process_data(content):
    """
    nft721 process data
    """
    if not content:
        return False, "not result"
    content_result = content.get("result")
    if not content_result:
        return False, "not result"

    count_risk = 0
    token_res = []
    asset_count_risk = 0
    asset_res = []
    for v in content_result:
        # approval
        chain_id = v.get("chain_id", 56)
        nft_name = v.get("nft_name")
        nft_address = v.get("nft_address")
        nft_symbol = v.get("nft_symbol")
        # asset
        malicious_address = v.get("malicious_address")
        is_open_source = v.get("is_open_source")
        for item in v.get("approved_list"):
            # approval
            contract = item.get("approved_contract")
            approved_amount = item.get("approved_for_all")
            address_info = item.get("address_info")

            malicious_behavior = address_info.get("malicious_behavior")
            # increased risk item
            for risk_key, msg in risk_msg.items():
                if address_info.get(risk_key) == 0:
                    malicious_behavior.append(msg)

            risk = len(malicious_behavior)
            count_risk += risk
            res_dict = {
                "project": address_info.get("contract_name"),
                "contract": contract,
                "chain": chain_id,
                "nft_name": nft_name,
                "nft_address": nft_address,
                "nft_symbol": nft_symbol,
                "approved_amount": "approval all" if approved_amount == 1 else "single",
                "advice": 0 if risk < 1 else 1,
                "risk": risk,
                "malicious_behavior": malicious_behavior
            }
            token_res.append(res_dict)

            # asset
            deployed_time = address_info.get("deployed_time")
            asset_risk = 0
            safety_tips = []
            if is_open_source == 0:
                asset_risk += 1
                safety_tips.append("This contract is not open source.")
            elif malicious_address == 1:
                safety_tips = malicious_behavior
            asset_risk += risk
            asset_count_risk += asset_risk
            asset_res_dict = {
                "asset_name": nft_symbol,
                "symbol": nft_symbol,
                "safety_tips": safety_tips,
                "chain_id": chain_id,
                "type": "ERC-721",
                "contract_address": nft_address,
                "balance": "1",
                "advice": "Safe" if asset_risk < 1 else "Caution" if asset_risk == 1 else "Do not trade",
                "deployed_time": deployed_time
            }
            asset_res.append(asset_res_dict)

    result = {
        "count_risk": count_risk,
        "result": token_res,
        "asset_count_risk": asset_count_risk,
        "asset_result": asset_res
    }
    return True, result


async def nft721_detect_result(chain_id, user_address):
    content = await goplus_wallet_detect(chain_id, user_address, 3)
    return await nft721_process_data(content)


async def get_detect_result(chain_id, user_address, option):
    if option == 2:
        status, result = await token_detect_result(chain_id, user_address)
    else:
        status, result = await nft721_detect_result(chain_id, user_address)
    return status, result


async def detect_create_table_and_to_result(user_address, chain, chain_id, option=2):
    """
    detect save db
    """
    user_detection, _ = await models.UserDetection.get_or_create(
        address=user_address,
        user_address=user_address,
        chain=chain,
        type=option,
        create_time=datetime.datetime.now()
    )

    status, result = await get_detect_result(chain_id, user_address, option)
    if status:
        user_detection.status = "1"
    else:
        user_detection.status = "2"
    await user_detection.save()
    return result


async def merge_erc20_nft721_detect(user_address, chain, chain_id):
    erc20 = await detect_create_table_and_to_result(user_address, chain, chain_id, option=2)
    nft721 = await detect_create_table_and_to_result(user_address, chain, chain_id, option=3)

    asset_erc20 = erc20.pop("asset_count_risk")
    asset_erc20_result = erc20.pop("asset_result")
    asset_nft721 = nft721.pop("asset_count_risk")
    asset_nft721_result = nft721.pop("asset_result")

    asset_result = asset_erc20_result + asset_nft721_result
    sort_result = sorted(asset_result, key=lambda x: x.get("deployed_time"), reverse=True)
    data = {
        "erc20": erc20,
        "nft721": nft721,
        "asset_security": {
            "count_risk": asset_erc20 + asset_nft721,
            "result": sort_result
        }
    }
    return data

# -- api


@wallet_detect_router.get('/total')
async def total():
    """
    detection total
    """
    count = await models.UserDetection.filter(type=2).all().count()
    return await success({"total": 3000 + int(count)})


@wallet_detect_router.post('/detect')
async def token_detection(
        user_address: str = Body(None),
        chain: Optional[str] = Body("BSC"),
        option: Optional[int] = Body(2),
):
    """
    home search
    :param user_address:用户钱包地址
    :param chain: 链(ETH,BSC)
    :param option: 2token授权检测 3nft721授权检测
    :return:
    """
    if not user_address:
        return await error_found("no user address")
    chain_id = chain_type.get(chain)
    if not chain_id or chain_id is None:
        return await error_found("This chain is not supported yet/ chain error")
    if option not in [2, 3]:
        return await error_found("Please enter the correct selection")

    result = await detect_create_table_and_to_result(user_address, chain, chain_id, option)

    return await success(result)


@wallet_detect_router.post('/merge_detect')
async def merge_detection(
        user_address: str = Body(None),
        chain: Optional[str] = Body("BSC"),
):
    """
    home search
    :param user_address:用户钱包地址
    :param chain: 链(ETH,BSC)
    :return:
    """
    if not user_address:
        return await error_found("no user address")
    chain_id = chain_type.get(chain)
    if not chain_id or chain_id is None:
        return await error_found("This chain is not supported yet/ chain error")

    data = await merge_erc20_nft721_detect(user_address, chain, chain_id)
    return await success(data)
