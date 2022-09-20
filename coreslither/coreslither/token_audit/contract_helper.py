from slither import Slither
from slither.core.solidity_types import MappingType
from slither.core.solidity_types import ArrayType
from slither.core.solidity_types import ElementaryType
from slither.core.solidity_types import UserDefinedType

# a = Slither('BACK.sol')

def find_real_contract(file_slither):
    # get the real contract, whose constructor executed in contract creation
    contract_list = [one for one in file_slither.contracts if not (one.is_interface or one.is_library)]
    real_contract = None
    inherit_count = 0
    if len(contract_list) == 1:
        return contract_list[0]
    else:
        #TODO build derived map for all contract in contract_list
        # find the contract which has no subclass
        for one in contract_list:
            if len(one.inheritance) > inherit_count:
                real_contract = one
        # find more specific method to determine the real contract
    return real_contract

def find_only_owner_modifier(contract):
    # find The only owner modifier, which name can be only_admin,only_root
    target_list = []

    for modifier in contract.modifiers:
        #1 ,must check the caller ,ie _MsgSender
        if '_msgSender' not in modifier.all_internal_calls():
            continue
        #2,compare with address state var
        for var in modifier._all_state_variables_read:
            if type(var.type)==ElementaryType and var.type.name == "address":
                target_list.append(modifier)
    if target_list:
        return target_list[0]


def find_balance_var(contract):
    # find balance var  from  balanceOf(address)
    balance_of = contract.get_function_from_full_name('balanceOf(address)')

    write_var = balance_of.all_state_variables_read
    target_list = []
    for one in write_var:
        if one.type == MappingType and one.signature[1]== ['address'] and one.signature[2] == ['uint256']:
            target_list.append(one)
    if len(target_list) >1:
        print("more than one candidate")
    return target_list[0]


def find_total_supply(contract):
    total_supply = contract.get_function_from_full_name('totalSupply()')
    return total_supply.all_state_variables_read()[0]


def collect_state_variable(contract):
    # collect all the variables which load on block
    write_var = contract.all_state_variables_written



def check_black_list(contract):
    #1 store address list
    write_var = contract.all_state_variables_read
    target_list = []
    for one in write_var:
        if one.type == MappingType and one.signature[1]== ['address'] and one.signature[2] == ['bool']:
            target_list.append(one)
    #2 only owner can change the state variable
    #3 which function is public
    only_owner_modifier =  contract.find_only_owner_modifier(contract)
    for one in contract.functions:
        if only_owner_modifier not in one.modifiers:
            continue
        if set(target_list).intersection(set(one.all_state_variables_written())):
            return True





def mint_check(contract):
    ...
