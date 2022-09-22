from pathlib import Path

from .contract_helper import find_real_contract


from slither import Slither
from slither.core.solidity_types import MappingType
from slither.core.solidity_types import ArrayType
from slither.core.solidity_types import ElementaryType
from slither.core.solidity_types import UserDefinedType


sol_file_dir = '/home/newlife/token'

solc_file_list = [str(one) for one in list(Path(sol_file_dir).glob("*.sol"))]

def test_find_real_contract(sol_dir):
    for file_path  in solc_file_list:
        file_slither = Slither('BACK.sol')
        print(find_real_contract(file_slither))
