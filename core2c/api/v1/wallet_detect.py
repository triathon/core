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


async def token_process_data(content):
    """
    token process data
    """
    content_result = content.get("result")
    if not content_result:
        return False, "not result"

    count_risk = 0
    token_res = []
    for v in content_result:
        chain_id = v.get("chain_id", 56)
        token_name = v.get("token_name")
        token_symbol = v.get("token_symbol")
        balance = v.get("balance")
        for item in v.get("approved_list"):
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
                "token_symbol": token_symbol,
                "balance": balance,
                "approved_amount": approved_amount,
                "advice": 0 if risk < 1 else 1,
                "risk": risk,
                "malicious_behavior": malicious_behavior
            }
            token_res.append(res_dict)

    result = {
        "count_risk": count_risk,
        "result": token_res
    }
    return True, result


async def token_detect_result(chain_id, user_address):
    content = await goplus_wallet_detect(chain_id, user_address)
    return await token_process_data(content)


async def nft721_process_data(content):
    """
    nft721 process data
    """
    content_result = content.get("result")
    if not content_result:
        return False, "not result"

    count_risk = 0
    token_res = []
    for v in content_result:
        chain_id = v.get("chain_id", 56)
        nft_name = v.get("nft_name")
        nft_symbol = v.get("nft_symbol")
        for item in v.get("approved_list"):
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
                "nft_name": nft_name,
                "nft_symbol": nft_symbol,
                "approved_amount": approved_amount,
                "advice": 0 if risk < 1 else 1,
                "risk": risk,
                "malicious_behavior": malicious_behavior
            }
            token_res.append(res_dict)

    result = {
        "count_risk": count_risk,
        "result": token_res
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

# -- api


@wallet_detect_router.get('/total')
async def total():
    """
    detection total
    """
    count = await models.UserDetection.filter(type__in=[2, 3]).all().count()
    return await success({"total": 2000 + int(count)})


# @wallet_detect_router.get("/status")
# async def status(
#         user_address: str
# ):
#     """
#     get detection status
#     """
#     data = {"status": "0"}
#     user_detection = await models.UserDetection.filter(user_address=user_address, status="0", type=2).first()
#     if user_detection:
#         data = {"status": "1", "address": user_detection.address, "chain": user_detection.chain}
#     return await success(data)


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

    user_detection, _ = await models.UserDetection.get_or_create(
        address=user_address,
        user_address=user_address,
        chain=chain,
        type=option,
        create_time=datetime.datetime.now()
    )

    status, result = await get_detect_result(chain_id, user_address, option)
    if not status:
        return await error_found("detection failure")
    if status:
        user_detection.status = "1"
        await user_detection.save()
        return await success(result)
    else:
        user_detection.status = "2"
        await user_detection.save()
        return await error_found(result)
