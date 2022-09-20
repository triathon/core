from slither import Slither
from slither.core.solidity_types import MappingType
from slither.core.solidity_types import ArrayType
from slither.core.solidity_types import ElementaryType
from slither.core.solidity_types import UserDefinedType
a = Slither('BACK.sol')

def find_real_contract(file_slither):
    # get the real contract, whose constructor executed in contract creation
    contract_list = [one for one in file_slither.contracts if not (one.is_interface or one.is_library)]
    real_contract = None
    inherit_count = 0
    if len(contract_list) > 1:
        for one in contract_list:
            if len(one.inheritance) > inherit_count:
                real_contract = one
    else:
        real_contract = contract_list[0]
    return real_contract

def find_only_owner_modifier(contract):
    # find The only owner modifier
    target_list = []
    for modifier in contract.modifiers:
        for var in modifier._all_state_variables_read:
            if type(var.type)==ElementaryType and var.type.name == "address":
                target_list.append(modifier)
    return target_list
                
def collect_state_variable(contract):
    # collect all the variables which load on block
    write_var = contract.all_state_variables_read
    
def find_balance_var(contract):
    write_var = contract.all_state_variables_read
    target_list = []
    for one in write_var:
        if one.type == MappingType and one.signature[1]== ['address'] and one.signature[2] == ['uint256']:
            target_list.append(one)
    if len(target_list) == 1:
        return target_list[0]
    
def check_black_list(contract):
    write_var = contract.all_state_variables_read
    target_list = []
    for one in write_var:
        if one.type == MappingType and one.signature[1]== ['address'] and one.signature[2] == ['bool']:
            target_list.append(one)
    if not target_list:
        return False
    

    
    
    
def mint_check(contract):
    ...
    