import os
import re
import time
import shutil

from api.tools.pull_contract_pack import pull_pack


class Merge(object):
    """
    Merge Files

    path: Folder path
    main_file: Primary file path
    """
    def __init__(self, path, main_file):
        if not path.endswith(os.path.sep):
            path += os.path.sep
        self.path = path
        self.main_file = main_file
        self.version = None
        self.verify()
        date = int(time.time())
        self.prefix = f"/opt/project/backend/upload_contracts/{str(date)}npm"
        os.mkdir(self.prefix)
        self.node_modules_path = f"{self.prefix}/node_modules"

    def start(self):
        """
        start of program
        :return:
        """
        spdx_text = "// SPDX-License-Identifier: MIT \n"
        pragma_text = f"pragma solidity ^{self.version};\n"

        _, code = self.merger_code(os.path.abspath(self.path+self.main_file), [], [])
        result = spdx_text + pragma_text + code

        # del node_modules
        shutil.rmtree(self.prefix)

        return result

    def verify(self):
        """
        Some check
        :return:
        """
        self.verify_is_sol(self.main_file)
        self.verify_path()
        self.verify_sol_version()

    def verify_is_sol(self, file_name):
        """
        verify whether it is an sol file
        :param file_name:
        :return:
        """
        if not file_name.endswith(".sol"):
            raise Exception(f"{file_name} not a sol file")

    def verify_path(self):
        """
        verification path
        :return:
        """
        if not os.path.exists(self.path):
            raise Exception("There is no path")

    def verify_sol_version(self):
        """
        Verify the contract version
        assign the value self.version
        :return:
        """
        main_file = os.path.abspath(self.path + self.main_file)
        f = open(main_file, 'r').read()
        version = re.search("pragma solidity ([\d.^]*)", f)
        if not version:
            raise Exception("The main file has no version number")
        version = version.group(1).replace("^", "")
        match = re.search(r"\d+\.\d+\.\d+", version)
        if not match:
            raise Exception("Compiler version is not a valid format")
        self.version = version

    def merger_code(self, current_file, processed, npm_packs, a=1):
        """

        :param current_file:
        :param processed:
        :param npm_packs:
        :return:
        """
        buffer = []
        if current_file.split('/')[-1] in processed:
            return processed, ''

        # if len(processed) == 16:
        #     a += 1
        #     if a == 5:
        #         raise
        #     print(f"-------------- \n processed: {len(processed)}")
        #     print(f"current_file: {current_file}")

        with open(current_file, "r+") as f:
            for line in f:
                # Remove the pragma line in all imports
                if "pragma" in line[:6] or "SPDX-License-Identifier" in line:
                    continue
                # Add additional code
                if "import" in line[:6]:
                    # if len(processed) == 16:
                    #     print(f"line: {line}")
                    introduce_file, npm_packs = self.get_import_path(line, current_file, npm_packs)
                    processed, code = self.merger_code(introduce_file, processed, npm_packs, a)
                    if code:
                        buffer.append(code)
                        processed.append(introduce_file.split('/')[-1])
                else:
                    buffer.append(line)
        return processed, ''.join(buffer)

    def get_import_path(self, line, current_file, npm_packs):
        # Import network package processing
        network_match = re.search('import +["\']@(.*)["\'];', line)
        # Local packet guide processing
        lock_match = re.search(r".*[\'|\"](.*)[\'|\"]", line)

        if network_match:
            introduce_file = os.path.abspath(
                f"{self.node_modules_path}/@{network_match.group(1)}")

            lis = network_match.group(1).split('/')
            npm_pack_name = f"@{lis[0]}/{lis[1]}"
            # whether a package has been downloaded
            if npm_pack_name not in npm_packs and not os.path.exists(introduce_file):
                # Download the pack
                pull_pack(npm_pack_name, self.prefix)
                npm_packs.append(npm_pack_name)
        elif lock_match:
            current_files = current_file.split('/')
            file_prefix = "/".join(current_files[:-1])
            introduce_file = os.path.abspath(os.path.join(file_prefix, lock_match.group(1)))
        else:
            raise Exception("There's syntax error of import in {}".format(line))
        return introduce_file, npm_packs


def merge_test():
    path = "/opt/project/sol/"
    file_name = "0x3d24C45565834377b59fCeAA6864D6C25144aD6c.sol"
    merge = Merge(path, file_name)
    res = merge.start()

    # save to file
    file = open('/opt/project/sol/0xxx.sol', 'w')
    file.write(res)
    file.close()
    print('ok')

