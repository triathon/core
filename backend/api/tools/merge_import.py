import re
import os
from merge_contract import merger_contract


def search_sol_by_filename(name, sols):
    file_name = lambda p: p.split(os.path.sep)[-1]
    try:
        return next(file_name(f) for f in sols if file_name(f)[6:] == name)
    except StopIteration:
        return None


def fix_import_line(line, sols):
    match = re.search(r'''['"].*/(\w+\.sol)['"];''', line)
    if match:
        sol = match.group(1)
        replacement = search_sol_by_filename(sol, sols)
        if replacement:
            n_line = f'import "./{replacement}";\n'
            return n_line

    return line


def fix_import(sol, sols):
    with open(sol, 'r') as f:
        lines = list(f.readlines())
    updated_lines = [fix_import_line(line, sols) for line in lines]
    if lines != updated_lines:
        with open(sol, 'w') as f:
            f.write(''.join(updated_lines))


def handle_import(file_path, main_file):
    """
    :param file_path: contract path
    :param main_file: contract master file
    :return: merge contract
    """
    sols = [os.path.join(file_path, f) for f in os.listdir(file_path) if f.endswith('.sol')]
    for f in sols:
        fix_import(f, sols)
    return merger_contract(file_path, main_file)


if __name__ == '__main__':
    data = handle_import("/Users/luwei/Documents/luwei_code/BafenLiang/L4/etherscan-contract-crawler/bsc_contracts/0x00c49A0E9F793Eaa605bbE153fceBc031a605a2b_LockBurnBridge", "01_11_LockBurnBridge.sol")
    print(data)
