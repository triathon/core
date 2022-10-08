import os
import re
import sys


def is_sol_valid(infile, s):
    if ".sol" != infile[-4:]:
        return True, "{} file is not a solidity file!!!".format(s)
    return False, None


def unfold_imports(imports, infile):
    buffer = []

    if infile not in imports:
        with open(infile, "r+") as f:

            for line in f:
                # Remove the pragma line in all imports
                if "pragma" in line[:6]:
                    continue
                if "SPDX-License-Identifier" in line:
                    continue

                # Read the imports
                if "import" in line[:6]:
                    match = re.search(r".*[\'|\"](.*)[\'|\"]", line)
                    if match:
                        dirname = os.path.dirname(infile)
                        file = os.path.join(dirname, match.group(1))
                        introduce_file = os.path.abspath(file)

                        buffer.append(unfold_imports(imports, introduce_file))
                        imports.append(introduce_file)
                    else:
                        print("There's syntax error of import in {}".format(infile))
                        sys.exit(-3)
                else:
                    buffer.append(line)
    return ''.join(buffer)


def merge_run(file_path, version):

    # Check if the solidity compiler version format is valid
    match = re.search(r"\d+\.\d+\.\d+", version)
    if not match:
        return "Compiler version is not a valid format"
    # Check if the input solidity filename is valid
    status, error = is_sol_valid(file_path, "Input")
    if status:
        return error

    infile = file_path

    imports = []
    data = "pragma solidity ^{};\n".format(version) + unfold_imports(imports, os.path.abspath(infile))

    return data


def merger_contract(file_path, main_file):
    master_file = file_path + "/" + main_file
    with open(master_file, 'r') as f:
        data = f.read()
    version = re.search("pragma solidity ([\d.^]*)", data)
    if version:
        version = version.group(1).replace("^", "")
        return merge_run(master_file, version)
    return "There is no version number in the contract"
