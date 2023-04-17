import re
import json
import inspect
import time

import redis
import solcx

from models.module import Document, DATA
from slither.slither import Slither
from tempfile import NamedTemporaryFile
from slither.detectors.abstract_detector import AbstractDetector
from slither.detectors import all_detectors
from solc_select.solc_select import switch_global_version, installed_versions, install_artifacts
from token_audit.contract_helper import find_real_contract, check_black_list
from token_audit.contract_helper import check_selfdestruct, check_owner_privilege


pattern = r"\(.*?\)"


def version_vif(version):
    """
    版本
    """
    version_group = version.group(1)
    if "^" in version_group:
        version = version_group.replace("^", "")
    elif "=" in version_group:
        version = version_group.replace("=", "")
    elif ">=" in version_group:
        version = version_group.replace(">=", "")
    elif ">" in version_group:
        version = version_group.replace(">", "")
    else:
        version = version_group

    if version not in installed_versions():
        install_artifacts("all")

    switch_global_version(version)
    return True, version


def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    s_id = int(req)
    result_list = []
    data = Document.select().where(Document.id == s_id).first()
    if not data:
        return "Invalid resource"

    version = re.search("pragma solidity ([\d.^|\d.=|\d.>=|\d.>]*)", data.contract)
    if version:
        status, msg = version_vif(version)
        if not status:
            return msg
    with NamedTemporaryFile('w+t', suffix=".sol") as f:
        f.write(data.contract)
        f.seek(0)
        print("filename:", f.name)
        try:
            slither = Slither(f.name)
        except Exception as err:
            err_str = err.__str__()
            if "Source file requires different compiler version" in err_str:
                return "Compiler version mismatch"
            if "not found: File not found" in err_str:
                return "Missing dependent file"
            return err_str

    if not data.functions:
        function_list = []
        for contract in slither.contracts:
            contract_list = []
            for function in contract.functions:
                contract_list.append({
                    "function_name": function.name,
                    "read": [v.name for v in function.variables_read if v],
                    "written": [v.name for v in function.variables_written if v]
                })
            function_list.append({
                "contract": contract.name,
                "function": contract_list
            })
        data.functions = json.dumps(function_list)

    detectors = [getattr(all_detectors, name) for name in dir(all_detectors)]
    detectors = [d for d in detectors if inspect.isclass(d) and issubclass(d, AbstractDetector)]
    for detector_cls in detectors:
        slither.register_detector(detector_cls)
    result = slither.run_detectors()
    for values in result:
        for value in values:
            description = value["description"]
            matching = re.findall(pattern, description)
            for match in matching:
                if len(match) > 20:
                    description = description.replace(match, "")
            result_list.append({
                "check": value["check"],
                "impact": value["impact"],
                "confidence": value["confidence"],
                "description": description
            })


    token_result = {}
    real_contract = find_real_contract(slither)
    if type(real_contract) != tuple and real_contract.is_erc20():
        token_result['is_blacklist'] = check_black_list(real_contract)
        token_result['is_selfdestruct'] = check_selfdestruct(real_contract)[0]
        token_result['is_delegatecall'] = check_selfdestruct(real_contract)[1]
        token_result['is_owner_privilege'] = check_owner_privilege(real_contract)

    data = Document.select().where(Document.id == s_id).first()
    result = data.result
    result["core_slither"] = result_list
    data.result['token_audit'] = token_result
    data.result = result
    data.save()
    return "Detection completed"


def save_error(error, did):
    data_db = Document.select().where(Document.id == did).first()
    if data_db:
        db_result = data_db.result
        db_result["coreslither_error"] = error
        data_db.result = db_result
        data_db.save()


def run():
    print("slither start of testing...")
    conn_pool = redis.ConnectionPool(
        host=DATA.redis_host,
        port=DATA.redis_port,
        password=DATA.redis_password,
        decode_responses=True,
        db=DATA.redis_db,
    )
    rc = redis.Redis(connection_pool=conn_pool)
    rcSetKey = DATA.task_queue+"Set"
    while True:
        id_list = rc.lrange(DATA.task_queue, 0, 4)
        if id_list:
            contract_id = rc.rpop(DATA.task_queue)
            try:
                print("db contract index {} :".format(contract_id))
                result = handle(contract_id)
                print("result: {}".format(result))
                if result != "Detection completed":
                    save_error(str(result), contract_id)
                    rc.hset(rcSetKey, f"{contract_id}error", str(result))
                    rc.hset(rcSetKey, f"{contract_id}status", "2")
                else:
                    rc.hset(rcSetKey, f"{contract_id}status", "1")
                time.sleep(2)
            except Exception as e:
                print("error:", e)
                count = rc.hget(rcSetKey, f"{contract_id}count")
                if not count:
                    count = 0
                if count >= 1:
                    continue
                # tautology
                save_error(str(e), contract_id)
                rc.hset(rcSetKey, f"{contract_id}count", str(int(count)+1))
                rc.hset(rcSetKey, f"{contract_id}error", str(e))
                rc.hset(rcSetKey, f"{contract_id}status", "2")

                rc.lpush(DATA.task_queue, contract_id)
                print("tautology:", contract_id)
        else:
            print("wait...")
            time.sleep(5)


if __name__ == '__main__':
    run()
