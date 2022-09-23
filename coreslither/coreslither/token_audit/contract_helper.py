from slither import Slither
from slither.core.solidity_types import MappingType
from slither.core.solidity_types import ArrayType
from slither.core.solidity_types import ElementaryType
from slither.core.solidity_types import UserDefinedType


from slither.slithir.operations import Return
# a = Slither('BACK.sol')
# contract.inheritance :superclass
# contract.derived_contracts ：subclass

def find_real_contract(file_slither):
    # get the real contract, whose constructor executed in contract creation
    contract_list = [one for one in file_slither.contracts if not (one.is_interface or one.is_library)]
    real_contract = None
    inherit_count = 0
    # rule 1 ,default rule
    if len(contract_list) == 1:
        return contract_list[0]
    # rule 2 , no subclass

    subclass_check_list = [one for one in contract_list if len(one.derived_contracts)==0]
    if len(subclass_check_list) == 1:
        return subclass_check_list[0]

    # rule 3 , superclass name contains 20

    superclass_checkou_list =  [one for one in subclass_check_list if "20" in ''.join([one.name for one in  one.inheritance])]
    if len(superclass_checkou_list) == 1:
        return superclass_checkou_list[0]
    return (False,"need more rule to handle such situation")


def find_only_owner_modifier(contract):
    # find The only owner modifier, which name can be only_admin,only_root
    target_list = []

    for modifier in contract.modifiers:
        #1 ,must check the caller ,ie msg.sender
        name_list = [one.name for one in  modifier.all_solidity_variables_read()]
        if "msg.sender" not in name_list:
            continue
        #2,compare with address state var
        for var in modifier.all_state_variables_read():
            if type(var.type)==ElementaryType and var.type.name == "address":
                target_list.append(modifier)
    if target_list:
        return target_list[0]


def find_balance_mapping(contract):
    # find balance var  from  balanceOf(address)
    balance_of = contract.get_function_from_full_name('balanceOf(address)')

    write_var = balance_of.all_state_variables_read()
    target_list = []
    for one in write_var:
        if type(one.type) == MappingType and one.signature[1]== ['address'] and one.signature[2] == ['uint256']:
            target_list.append(one)
    if len(target_list) >1:
        print("more than one candidate")
    return target_list[0]


def find_total_supply(contract):
    total_supply = contract.get_function_from_full_name('totalSupply()')
    return total_supply.all_state_variables_read()[0]


def check_black_list(contract):
    #1 store address list
    write_var = contract.all_state_variables_read
    target_list = []
    for one in write_var:
        if type(one.type) == MappingType and one.signature[1]== ['address'] and one.signature[2] == ['bool']:
            target_list.append(one)
            print("candinate address mapping", one.name)
    #2 only owner can change the state variable
    #3 which function is public
    
    only_owner_modifier =  find_only_owner_modifier(contract)
    for one in contract.functions:
        if only_owner_modifier not in one.modifiers:
            continue
        if set(target_list).intersection(set(one.all_state_variables_written())):
            print("candinate function:",one.name)
            return True




def mint_check(contract):
    ...

def owner_privilege(contract):
    only_owner = find_only_owner_modifier(contract)
    owner_function_list = [one for one in contract.functions if one.visibility in ['public','external']]

    owner_function_list = [one for one in owner_function_list if only_owner in one.modifiers]

    privilege_count = len(owner_function_list)

    if privilege_count < 20:
        # temp set to 20, need more data to confirm
        return True
