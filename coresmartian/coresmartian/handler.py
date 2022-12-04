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
    version = version.group(1).replace("^", "")[:3]
    if version == "0.4":
        solcx.install_solc("0.4.19")
        solc_version = "0.4.19"
    if version == "0.5":
        switch_global_version("0.5.16")
        solc_version = "0.5.16"
    if version == "0.6":
        switch_global_version("0.6.11")
        solc_version = "0.6.11"
    if version == "0.7":
        switch_global_version("0.7.6")
        solc_version = "0.7.6"
    if version == "0.8":
        switch_global_version("0.8.16")
        solc_version = "0.8.16"
    return solc_version


def generate_sol_abi_bin(solc_version, contract, file_name):
    output = solcx.compile_source(
        contract,
        output_values=["abi", "bin"],
        solc_version=solc_version
    )

    contract_name = file_name.split(".")[0]
    output_ = [output[v] for v in output if v.split(":")[-1] == contract_name][0]

    abi = str(output_.get("abi"))
    abi = abi.replace("'", '"')
    abi = abi.replace("True", "true")
    abi = abi.replace("False", "false")

    prefix = f"{sys.path[0]}\{int(time.time())}{contract_name}"
    os.mkdir(prefix)

    abi_path = f"{prefix}\{contract_name}.abi"
    f = open(abi_path, "a")
    f.write(abi)
    f.close()

    bin_path = f"{prefix}\{contract_name}.bin"
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
    print(f"cmd run: {cmd_to_run}")
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

    timeout = 2

    version = re.search("pragma solidity ([\d.^]*)", contract)
    solc_version = update_sol_version(version)
    abi_path, bin_path, prefix = generate_sol_abi_bin(solc_version, contract, contract_name)

    order = f"dotnet D:/d/build/Smartian.dll fuzz -v 0 -p {bin_path} -a {abi_path} -t {timeout} -o {prefix}\/result"
    stderr, stdout = run_command(order)
    if stderr:
        raise Exception(f'Smartion error: {stderr}')

    result = stdout.split("Fuzzing timeout expired.")[-1]
    result = result.split("\r\n")
    result_list = [v.replace(" ", "").split("]")[-1] for v in result]
    results = {}
    for v in result_list:
        if ":" in v:
            key, value = v.split(":")
            results[key] = value

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
            result = handle(contract_id)
            print("db contract index {}, {}".format(contract_id, result))
            time.sleep(2)
        else:
            print("wait...")
            time.sleep(5)


if __name__ == '__main__':
    run()
