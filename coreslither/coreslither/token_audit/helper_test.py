from pathlib import Path

from contract_helper import find_real_contract
from contract_helper import find_only_owner_modifier


from slither import Slither
from slither.core.solidity_types import MappingType
from slither.core.solidity_types import ArrayType
from slither.core.solidity_types import ElementaryType
from slither.core.solidity_types import UserDefinedType


sol_file_dir = '/home/newlife/token'

solc_file_list = [str(one) for one in list(Path(sol_file_dir).glob("*.sol"))]
print(len(solc_file_list))
print(solc_file_list)
def test_find_real_contract():
    
    for file_path  in solc_file_list:
        file_slither = Slither(file_path)
        real_contract = find_real_contract(file_slither)
        print(file_path,real_contract)
        print("only owner modifier",find_only_owner_modifier(real_contract))

if __name__ == '__main__':
    test_find_real_contract()
