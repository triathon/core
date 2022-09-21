import re
import json
import inspect
from .models.module import Testing, Functional
from slither.slither import Slither
from tempfile import NamedTemporaryFile
from slither.detectors.abstract_detector import AbstractDetector
from slither.detectors import all_detectors
from solc_select.solc_select import switch_global_version


pattern = r"\(.*?\)"


def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    s_id = int(req)
    result_list = []
    data = Testing.select().where(Testing.id == s_id).first()
    if not data:
        return "Invalid resource"

    version = re.search("pragma solidity ([\d.^]*)", data.content).group(1)
    if not version:
        return "Whether the contract contains the correct version"
    version = version.replace("^", "")[:3]
    if version == "0.5":
        switch_global_version("0.5.16")
    if version == "0.6":
        switch_global_version("0.6.11")
    if version == "0.7":
        switch_global_version("0.7.6")
    if version == "0.8":
        switch_global_version("0.8.16")

    with NamedTemporaryFile('w+t', suffix=".sol") as f:
        f.write(data.content)
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

    data = Functional.select().where(Functional.test_id == s_id).first()
    if not data:
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

        Functional.create(
            test_id=s_id,
            function=json.dumps(function_list)
        )

    detectors = [getattr(all_detectors, name) for name in dir(all_detectors)]
    detectors = [d for d in detectors if inspect.isclass(d) and issubclass(d, AbstractDetector)]
    for detector_cls in detectors:
        slither.register_detector(detector_cls)
    result = slither.run_detectors()
    for values in result:
        if values:
            for value in values:
                val_dict = dict(value)
                description = val_dict["description"]
                matching = re.findall(pattern, description)
                for match in matching:
                    if len(match) > 20:
                        description = description.replace(match, "")
                result_list.append(description)
    testing = Testing.select().where(Testing.id == s_id).first()
    if testing:
        t_result = json.loads(testing.result)
        t_result["core_slither"] = result_list
        testing.result = json.dumps(t_result)
        testing.save()

    return "Detection completed"
