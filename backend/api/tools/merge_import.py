# Fix imports path for all solidity files in the `--root` directory
# Use this script to make the source code compilable. Assuming all source code are in the root directory.

import re
import os

def build_import_graph(sol_dir):
    resolve_dict = {}
    sols =  [os.path.join(sol_dir, f) for f in os.listdir(sol_dir) if f.endswith('.sol')]
    for file_path in sols:
        with open(file_path, 'r') as f:
            import_file_list = []
            for line in f:
                match = re.search(r'''['"].*/(\w+\.sol)['"];''', line)
                if match:
                    import_file = match.group(1)
                    import_file_list.append(import_file)
        resolve_dict[file_path] = import_file_list

    file_list = list(resolve_dict.keys())
    with open("target.sol",'a+') as target:
        while len(file_list):
            write_file_list = [k for k,v in resolve_dict.items() if len(v) ==0]
            for file_path in write_file_list:
                with open(file_path, 'r') as sol_file:
                    for line in sol_file:
                        if not line.startswith('import'):
                            target.write(line)
                file_list.remove(file_path)
                resolve_dict.pop(file_path)
                for k, v in resolve_dict.items():
                    file_name = file_path.split('/')[-1]
                    if file_name in v:
                        v.remove(file_name)



if __name__ == '__main__':
    root = "./multi_file_contract"

    build_import_graph(root)
