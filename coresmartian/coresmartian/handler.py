# -*- coding: utf-8 -*-
"""
@File        : smartion.py
@Author      : Aug
@Time        : 2022/11/28 9:32
@Description :
"""
import os
import re
import shutil
import sys
import tempfile
import subprocess
import time
import redis

import solcx
from models.module import Document, DATA
from solc_select.solc_select import switch_global_version


def update_sol_version(version):
    """
    update sol version
    :param version:
    :return:
    """
    if not version:
        raise Exception("Not version")

    version_group = version.group(1)
    if "^" in version_group:
        version = version_group.replace("^", "")[:3]
    elif "=" in version_group:
        version = version_group.replace("=", "")[:3]
    elif ">=" in version_group:
        version = version_group.replace(">=", "")[:3]
    elif ">" in version_group:
        version = version_group.replace(">", "")[:3]
    else:
        version = version_group[:3]
    solc_version = "0.8.16"
    if version == "0.4":
        solcx.install_solc("0.4.26")
        solc_version = "0.4.26"
    elif version == "0.5":
        switch_global_version("0.5.16")
        solc_version = "0.5.16"
    elif version == "0.6":
        switch_global_version("0.6.11")
        solc_version = "0.6.11"
    elif version == "0.7":
        switch_global_version("0.7.6")
        solc_version = "0.7.6"
    elif version == "0.8":
        switch_global_version("0.8.16")
    solcx.install_solc(solc_version)
    return solc_version


def generate_sol_abi_bin(solc_version, contract, file_name):
    output = solcx.compile_source(
        contract,
        output_values=["abi", "bin"],
        solc_version=solc_version
    )

    contract_name = file_name.split(".")[0]
    output_ = [output[v] for v in output if v.split(":")[-1] == contract_name]
    if not output_:
        output_ = []
        for v in output:
            if v.split(":")[-1]:
                output_.append(output[v])
                break
    output_ = output_[0]

    abi = str(output_.get("abi"))
    abi = abi.replace("'", '"')
    abi = abi.replace("True", "true")
    abi = abi.replace("False", "false")

    prefix = f"{sys.path[0]}{os.path.sep}{int(time.time())}{contract_name}"
    os.mkdir(prefix)

    abi_path = f"{prefix}{os.path.sep}{contract_name}.abi"
    f = open(abi_path, "a")
    f.write(abi)
    f.close()

    bin_path = f"{prefix}{os.path.sep}{contract_name}.bin"
    f1 = open(bin_path, "a")
    f1.write(output_.get("bin"))
    f1.close()
    return abi_path, bin_path, prefix


def run_command(cmd_to_run, cwd=None):
    """
    Wrapper around subprocess that pipes the stderr and stdout from `cmd_to_run`
    to temporary files. Using the temporary files gets around subprocess.PIPE's
    issues with handling large buffers.

    Note: this command will block the python process until `cmd_to_run` has completed.

    Returns a tuple, containing the stderr and stdout as strings.
    """
    with tempfile.TemporaryFile() as stdout_file, tempfile.TemporaryFile() as stderr_file:
        # Run the command
        popen = subprocess.Popen(cmd_to_run, stdout=stdout_file, stderr=stderr_file, shell=True, cwd=cwd)
        popen.wait()

        stderr_file.seek(0)
        stdout_file.seek(0)

        stderr = stderr_file.read().decode()
        stdout = stdout_file.read().decode()

        return stderr, stdout


def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    data = Document.select().where(Document.id == int(req)).first()
    if not data:
        return "Invalid resource"
    contract = data.contract
    contract_name = data.file_name

    timeout = DATA.test_timeout

    version = re.search("pragma solidity ([\d.^|\d.=|\d.>=|\d.>]*)", contract)
    solc_version = update_sol_version(version)
    abi_path, bin_path, prefix = generate_sol_abi_bin(solc_version, contract, contract_name)

    smartian_dll_path = "/home/Smartian/build/Smartian.dll"  # {sys.path[0]}{os.path.sep}build{os.path.sep}Smartian.dll
    order = f"dotnet {smartian_dll_path} fuzz -v 0 -p {bin_path} -a {abi_path} -t {timeout} -o {prefix}{os.path.sep}result"
    stderr, stdout = run_command(order)
    if stderr:
        raise Exception(f'Smartian error: {stderr}')
    if "Statistics" not in stdout:
        raise Exception(f'Smartian error out: stdount')
    result = stdout.split("Statistics")[-1]

    res, found_bug = result.split("Found Bugs:")

    res_list = [v.replace(" ", "").split("]")[-1] for v in res.split("\n")]
    results = {v.split(":")[0]: v.split(":")[1] for v in res_list if ":" in v}

    found_bug_list = [v.replace(" ", "").split("]")[-1] for v in found_bug.split("\n")]
    results["FoundBugs"] = {v.split(":")[0]: v.split(":")[1] for v in found_bug_list if ":" in v}

    # rm file
    shutil.rmtree(prefix)

    data_result = data.result
    data_result["core_smartian"] = [results]
    data.result = data_result
    data.save()
    return "Done, clean up and exit..."


def run():
    print("smartian start of testing...")
    conn_pool = redis.ConnectionPool(
        host=DATA.redis_host,
        port=DATA.redis_port,
        password=DATA.redis_password,
        decode_responses=True,
        db=DATA.redis_db,
    )
    rc = redis.Redis(connection_pool=conn_pool)
    while True:
        id_list = rc.lrange(DATA.task_queue, 0, 4)
        if id_list:
            contract_id = rc.rpop(DATA.task_queue)
            try:
                print("db contract index {} :".format(contract_id))
                result = handle(contract_id)
                print("result: {}".format(result))
                time.sleep(2)
            except Exception as e:
                rc.lpush(DATA.task_queue, contract_id)
                print("tautology", e)
        else:
            print("wait...")
            time.sleep(5)


if __name__ == '__main__':
    run()
