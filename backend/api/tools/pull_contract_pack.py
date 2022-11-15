# -*- coding: utf-8 -*-
"""
@File        : runnpm.py
@Author      : Aug
@Time        : 2022/11/4 9:10
@Description : Download the contract network package
"""
import os
import tempfile
import subprocess


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


def pull_pack(pack_name, prefix):
    """
    Pull the contract network package
    :param pack_name:
    :return:
    """
    npm_pack_path = prefix
    npm_prefix = '--prefix=' + npm_pack_path
    npm_install_cmd = "npm install {} " + npm_prefix

    # Install the dependencies in the same directory as the current python file
    if not os.path.exists(npm_pack_path + "/package.json") and not os.path.exists(npm_pack_path + "\package.json"):
        stderr, stdout = run_command("npm init -y", cwd=npm_pack_path)
        if stderr:
            return False, f"[npm init] error: {stderr}"

    # Install pack
    stderr, stdout = run_command(npm_install_cmd.format(pack_name), cwd=npm_pack_path)
    if stderr:
        return False, f'[npm install] error: {stderr}'
    else:
        return True, ''
