import logging
import os
import random
from copy import deepcopy

from fameio.input.resolver import PathResolver

from famegui import models
from famegui.config.config import DEFAULT_FAME_WORK_DIR
from famegui.models import Contract
from famegui.undo_utils.contract_utils import swap_or_delete_contract
from famegui.undo_utils.undo_constants import UndoActions
from famegui_runtime_helper.dict_hash_helper import hash_dict
from famegui_runtime_helper.fame_session_cache import FameSessionCache


def test_contract_undo():
    assert os.path.exists(DEFAULT_FAME_WORK_DIR), f"Path does not exist: {DEFAULT_FAME_WORK_DIR}"

    file_path = os.path.join(DEFAULT_FAME_WORK_DIR, "scenario.yaml")

    scenario_model = models.ScenarioLoader.load_yaml_file(
        file_path, PathResolver(), DEFAULT_FAME_WORK_DIR)

    assert scenario_model is not None

    original_contracts = deepcopy(scenario_model.contracts)

    rdm_int = random.randint(0, len(scenario_model.contracts) - 1)

    process_random_contract_undo(original_contracts, rdm_int, scenario_model)


def process_random_contract_undo(original_contracts, rdm_int, scenario_model):
    # test if all contracts are serializable
    for idx, item in enumerate(scenario_model.contracts):
        contract_dict = item.to_dict()

        new_contract = Contract.from_dict(contract_dict)

        assert hash_dict(new_contract.to_dict()) == hash_dict(contract_dict)
    session_db = FameSessionCache()
    random_contract_pick = scenario_model.contracts[rdm_int]
    logger = logging.getLogger()
    logger.debug("random_contract_pick")

    logger.debug(random_contract_pick.to_dict())
    rdm_contract = random_contract_pick.to_dict()
    ref_contract = deepcopy(random_contract_pick.to_dict())
    rdm_contract = deepcopy(rdm_contract)

    rdm_contract["senderid"] = 62 if rdm_contract["senderid"] != 62 else 63
    contract_data = {"old_contract_data": ref_contract,
                     "current_contract_ref": rdm_contract}

    item_idx_to_del = None
    for idx, contract_item in enumerate(scenario_model.contracts):

        if hash_dict(contract_item.to_dict()) == hash_dict(ref_contract):
            item_idx_to_del = idx
            break
    assert item_idx_to_del is not None
    edited_contract = Contract.from_dict(rdm_contract)
    assert edited_contract is not None

    amount_of_contracts_pre_deletion = len(scenario_model.contracts)
    swap_or_delete_contract(scenario_model, ref_contract, None)
    amount_of_contracts_post_deletion = len(scenario_model.contracts)

    assert amount_of_contracts_pre_deletion != amount_of_contracts_post_deletion
    for contract_item in scenario_model.contracts:
        if hash_dict(contract_item.to_dict()) == hash_dict(ref_contract):
            assert ValueError("Removed Contract cannot be in Scenario")
    contract_undo_change_action = {
        "type": UndoActions.UNDO_CONTRACT_FIELDS_CHANGED.value,
        "data": contract_data
    }

    session_db.add_item(contract_undo_change_action)
    swap_or_delete_contract(scenario_model, None, ref_contract)
    current_contract_ref_idx = None
    for idx, contract_item in enumerate(scenario_model.contracts):
        if hash_dict(contract_item.to_dict()) == hash_dict(ref_contract):
            current_contract_ref_idx = idx
            break

    assert current_contract_ref_idx is not None
    contract_idx = None
    for idx, contract_item in enumerate(scenario_model.contracts):
        if hash_dict(contract_item.to_dict()) == hash_dict(ref_contract):
            contract_idx = idx
    assert contract_idx is not None

    for original_contract in original_contracts:
        matched = False
        for contract in scenario_model.contracts:
            if hash_dict(original_contract.to_dict()) == hash_dict(contract.to_dict()):
                matched = True
                break

        assert matched == True
    last_undo_item = session_db.get_last_item()
    last_contract_undo_change_action = last_undo_item["data"]

    logger.info("Checking....")
    logger.info(last_contract_undo_change_action["old_contract_data"])

    assert hash_dict(last_contract_undo_change_action["old_contract_data"]) != hash_dict(
        last_contract_undo_change_action["current_contract_ref"])
    current_contract_ref = last_contract_undo_change_action["current_contract_ref"]
    contracts_pre_undo = deepcopy(scenario_model.contracts)

    swap_or_delete_contract(scenario_model,
                            last_contract_undo_change_action["old_contract_data"],
                            current_contract_ref)
    swap_or_delete_contract(scenario_model,
                            current_contract_ref,
                            last_contract_undo_change_action["old_contract_data"])

    contracts_pre_undo_set = set([
        hash_dict(contract.to_dict()) for contract in contracts_pre_undo
    ])

    # check if contracts are same after performing an undo
    for item in scenario_model.contracts:
        assert hash_dict(item.to_dict()) in contracts_pre_undo_set
