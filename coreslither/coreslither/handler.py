import re
import json
import inspect
from .models.module import Document
from slither.slither import Slither
from tempfile import NamedTemporaryFile
from slither.detectors.abstract_detector import AbstractDetector
from slither.detectors import all_detectors
from solc_select.solc_select import switch_global_version
from .token_audit.contract_helper import find_real_contract, check_black_list
from .token_audit.contract_helper import check_selfdestruct, check_owner_privilege


pattern = r"\(.*?\)"


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

    version = re.search("pragma solidity ([\d.^]*)", data.contract)
    if version:
        version = version.group(1).replace("^", "")[:3]
        if version == "0.5":
            switch_global_version("0.5.16")
        if version == "0.6":
            switch_global_version("0.6.11")
        if version == "0.7":
            switch_global_version("0.7.6")
        if version == "0.8":
            switch_global_version("0.8.16")

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

    result = data.result
    result["core_slither"] = result_list

    token_result = {}
    real_contract = find_real_contract(slither)
    if type(real_contract) != tuple and real_contract.is_erc20():
        token_result['is_blacklist'] = check_black_list(real_contract)
        token_result['is_selfdestruct'] = check_selfdestruct(real_contract)[0]
        token_result['is_delegatecall'] = check_selfdestruct(real_contract)[1]
        token_result['is_owner_privilege'] = check_owner_privilege(real_contract)

    data.result['token_audit'] = token_result
    data.result = result
    data.save()
    return "Detection completed"
