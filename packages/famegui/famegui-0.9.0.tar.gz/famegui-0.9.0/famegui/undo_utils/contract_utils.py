from typing import Union

from famegui_runtime_helper.dict_hash_helper import hash_dict
from famegui.models import Scenario, Contract

MANIPULATED_CONTRACT_KEY = "current_contract"
ORIGINAL_CONTRACT_KEY = "original_contract"


# noinspection PyTypeChecker
def swap_or_delete_contract(scenario: Scenario, target_ref_contract: Union[dict, None],
                            contract_to_be_replaced: Union[dict, None]):
    if target_ref_contract is None:
        scenario.contracts.append(Contract.from_dict(contract_to_be_replaced))
        return

    item_idx_to_manipulate = None

    for idx, contract_item in enumerate(scenario.contracts):

        if hash_dict(contract_item.to_dict()) == hash_dict(target_ref_contract):
            item_idx_to_manipulate = idx
            break


    if contract_to_be_replaced is None:
        scenario.contracts.remove(scenario.contracts[item_idx_to_manipulate])
        return

    assert item_idx_to_manipulate is not None

    scenario.contracts[item_idx_to_manipulate] = Contract.from_dict(contract_to_be_replaced)
