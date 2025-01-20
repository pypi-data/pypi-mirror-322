import datetime
from functools import singledispatch

import ujson as json
import logging
import os.path
import time
import typing
from typing import List

import fameio.input.scenario as fameio
import fameio.input.schema as fameio_schema
from PySide6 import QtCore
from PySide6.QtCore import QObject
from fameio.input.scenario import Contract, Attribute
from icecream import ic

import famegui.models as models
from famegui.fame_tools.string_utils import get_last_substring
from famegui_runtime_helper.attribute_dict_formatting_helper import flatten_dict, build_simple_attr_dict
from famegui_runtime_helper.delta_dict_builder import DictDiffer
from famegui_runtime_helper.fame_session_cache import FameSessionCache
from famegui.config.config import BASE_DIR
from famegui.fame_tools.dict_tools import remove_none_values_and_empty_elements
from famegui.undo_utils.undo_constants import UndoActions


class Scenario(fameio.Scenario):
    class UndoManager(QObject):
        undo_signal = QtCore.Signal(int, str, str)  # agent_id, attr_name, new_value
        display_undo_dlg_signal = QtCore.Signal(str)  # serialized data

        def __init__(self):
            super().__init__()

    def connect_to_display_undo_dlg_signal(self, slot):
        self.undo_manager.display_undo_dlg_signal.connect(slot)

    def connect_to_undo_signal(self, slot):
        self.undo_signal.connect(slot)

    def trigger_undo(self):

        # get the last file in the cache

        cache_dir = os.path.join(BASE_DIR, "cache")

        youngest_file = None
        youngest_time = 0

        for filename in os.listdir(cache_dir):
            file_path = os.path.join(cache_dir, filename)
            if os.path.isfile(file_path):
                file_time = os.path.getmtime(file_path)
                if file_time > youngest_time:
                    youngest_time = file_time
                    youngest_file = file_path

        if youngest_file:
            time.ctime(youngest_time)

            with open(youngest_file, "r") as f:
                data = json.load(f)
                agent_id = data["agent_id"]
                attr_name = data["attr_name"]
                new_value = data["old_value"]

                self.undo_signal.emit(agent_id, attr_name, new_value)

    def compare_objects(self, obj1, obj2):

        attributes = ["delivery_interval", "product_name", "senderid", "receiverid", "expire_date", "first_delivery", ]

        changes = {}
        for attribute in dir(obj1):
            if not attribute.startswith('__'):

                if attribute not in attributes:
                    continue
                if attribute in changes:
                    continue
                value1 = getattr(obj1, attribute)
                value2 = getattr(obj2, attribute)
                if value1 != value2:
                    changes[attribute] = (value1, value2)
        return changes

    # Find changes between obj1 and obj2

    settings = {}

    def __init__(self, schema: fameio_schema.Schema, props: fameio.GeneralProperties):
        super().__init__(schema, props)

        self.undo_manager = self.UndoManager()
        self.undo_signal = self.undo_manager.undo_signal

    @property
    def contracts(self) -> List[Contract]:
        return super().contracts

    def del_all_related_contracts(self, agent_id: int) -> None:
        """Delete all contracts related to the given agent"""
        contracts_to_delete = []
        for idx, contract in enumerate(super().contracts[:]):
            if contract.sender_id == agent_id or contract.receiver_id == agent_id:
                contracts_to_delete.append(contract)
        for contract in contracts_to_delete:
            super().contracts.remove(contract)

    def set_agent_display_xy(self, agent_id: int, x: int, y: int) -> None:
        for a in self.agents:
            if a.id == agent_id:
                a.set_display_xy(x, y)
                return
        raise RuntimeError(f"Unknown agent with ID '{agent_id}'")

    def update_properties(self, props: models.GeneralProperties) -> bool:
        """Sync the scenario properties with the given ones, returns True if some changes"""
        if props.to_dict() != self.general_properties.to_dict():
            logging.info("Updating scenario general properties")
            self._general_props = props
            return True
        return False

    def to_export_to_yaml_dict(self):

        return self._to_dict()

    def _to_dict(self) -> dict:
        """Serializes the scenario content to a dict"""
        result = {
            Scenario.KEY_GENERAL: self.general_properties.to_dict(),
            Scenario.KEY_SCHEMA: self.schema.to_dict(),
        }
        if self.string_sets:
            result[Scenario.KEY_STRING_SETS] = {
                name: string_set.to_dict() for name, string_set in self.string_sets.items()
            }
        if self.agents:
            result[Scenario.KEY_AGENTS] = []
            for agent in self.agents:
                result[Scenario.KEY_AGENTS].append(agent.to_fame_gui_adjusted_dict())
        if self.contracts:
            result[Scenario.KEY_CONTRACTS] = []
            for contract in self.contracts:
                result[Scenario.KEY_CONTRACTS].append(contract.to_dict())

        return result

    def get_amount_of_related_contracts(self, agent_id) -> int:
        """Return the amount of directly connected agents to the given agent_id"""
        amount = 0
        for contract in self.contracts:
            if contract.sender_id == agent_id or contract.receiver_id == agent_id:
                amount += 1
        return amount

    def get_amount_connected_agents(self, agent_id: int) -> int:
        """Return the amount of directly connected agents to the given agent_id"""
        agent_id_set = set()

        for contract in self.contracts:
            if contract.sender_id == agent_id:
                agent_id_set.add(contract.receiver_id)
                continue
            if contract.receiver_id == agent_id:
                agent_id_set.add(contract.sender_id)

        return len(agent_id_set)

    def get_agents_by_type(self, type: str) -> typing.List[models.Agent]:

        return [agent for agent in self.agents if agent.type_name == type]

    def get_agent_by_id(self, agent_id: int) -> models.Agent:
        """Return the agent object model with the given agent_id"""
        for agent in self.agents:
            if agent.id == agent_id:
                return agent
        raise RuntimeError(f"Unknown agent with ID '{agent_id}'")

    def get_all_related_agents_ids(self, agent_id: int) -> List[int]:
        """Return a list of all agents related to the given agent_id"""
        agent_id_set = set()

        for contract in self.contracts:
            if contract.sender_id == agent_id:
                agent_id_set.add(contract.receiver_id)
                continue
            if contract.receiver_id == agent_id:
                agent_id_set.add(contract.sender_id)

        return list(agent_id_set)

    def add_contract(self, contract: models.Contract) -> None:
        # TODO: move here the logic located in MainController._create_contract_model
        super().add_contract(contract)

    @staticmethod
    def adjust_agent_attribute_keys(data_dict, agent_type):

        updated_data = {
            agent_type + "." + key: value
            for key, value in data_dict.items()
        }

        return updated_data

    def update_agent(self, updated_agent: models.Agent) -> None:
        """Update the agent with the given updated_agent."""

        for idx, agent in enumerate(super().agents[:]):
            if agent.id == updated_agent.id:

                updated_data = updated_agent.get_flat_agent_attributes_dict()

                flat_data = flatten_dict({}, updated_data)

                flat_data_old = agent.get_flat_agent_attributes_dict()

                attribute_diff = DictDiffer.diff_direct(flat_data_old, flat_data)

                changes_prefix = str(updated_agent.id) + "." + updated_agent.type_name

                attribute_diff = self.adjust_agent_attribute_keys(attribute_diff, changes_prefix)

                session_db = FameSessionCache()

                undo_item = {
                    "type": UndoActions.UNDO_AGENT_ATTRIBUTES_CHANGED.value,
                    "data": attribute_diff
                }

                session_db.add_item(undo_item)

                super().agents[idx].attributes.clear()

                for attr, value in updated_agent.attributes.items():

                    if isinstance(value, Attribute):
                        super().agents[idx].attributes[attr] = value
                        continue

                    if isinstance(value, dict):
                        value = {get_last_substring(key): value_sub for key, value_sub in value.items() if
                                 value_sub is not None}

                    super().agents[idx].attributes[attr] = Attribute(attr, value)

    def update_agent_from_dict(self, data_dict):
        non_full_name_values = {}

        attr_root_name_list = []

        agent_id, agent_type = None, None

        old_values = []

        for key in list(data_dict.keys()):
            splitted_attr_value_identifiers = key.split(".")
            agent_id = splitted_attr_value_identifiers[0]
            agent_type = splitted_attr_value_identifiers[1]
            root_attr_name = splitted_attr_value_identifiers[2]
            attr_root_name_list.append(root_attr_name)
            old_value = data_dict[key]["old_value"]
            old_values.append(old_value)

            sub_attr_key_list = splitted_attr_value_identifiers[2: (len(splitted_attr_value_identifiers))]

            values_from_store = {}

            if len(sub_attr_key_list) > 0:
                attr_name = ".".join(sub_attr_key_list)
                non_full_name_values[attr_name] = old_value
                attr_name = agent_type + "." + attr_name

                values_from_store[attr_name] = old_value

        for idx, agent in enumerate(super().agents[:]):
            if agent.id == int(agent_id):

                act = self.schema.agent_types[agent_type]

                for root_attr_name, old_value in zip(attr_root_name_list, old_values):
                    self.process_undo(act, agent, idx, non_full_name_values, old_value, root_attr_name)

    def process_undo(self, act, agent, idx, non_full_name_values, old_value, root_attr_name):
        root_attr = act.attributes.get(root_attr_name)
        if root_attr.has_nested_attributes:

            flat_full_name_labeled_values = agent.get_flat_agent_attributes_dict()

            non_full_name_values = remove_none_values_and_empty_elements(non_full_name_values)

            if root_attr.is_list:
                super().agents[idx].attributes[root_attr_name] = Attribute(root_attr_name,
                                                                           non_full_name_values[
                                                                               root_attr_name])
                return

            agent_type_name = agent.type_name

            flat_full_name_labeled_values.update(non_full_name_values)

            data_out = {}

            for attr_name, attr in act.attributes.items():
                iter_tmp_dict = build_simple_attr_dict(
                    attr, flat_full_name_labeled_values, agent_type_name)
                data_out[attr_name] = iter_tmp_dict[
                    attr_name] if attr_name in iter_tmp_dict else iter_tmp_dict

            data_out = remove_none_values_and_empty_elements(
                data_out
            )

            if not data_out:
                del super().agents[idx].attributes[root_attr_name]
                return

            data_out = data_out[root_attr_name]

            super().agents[idx].attributes[root_attr_name] = Attribute(root_attr_name, data_out)
            return
        if old_value is None:
            del super().agents[idx].attributes[root_attr_name]
            return
        super().agents[idx].attributes[root_attr_name] = Attribute(root_attr_name, old_value)
        return

    def agent_exists(self, agent_id: int) -> bool:
        """Check if an agent with the given id exists in the scenario."""
        return any([True for agent in self.agents if agent.id == agent_id])

    def update_contract(
            self, old_contract: models.Contract, updated_contract: Contract, is_in_testing_env=False
    ) -> None:
        """Update the contract with the given updated_contract."""
        """By searching the contract with the same product_name, sender_id 
        and receiver_id. to replace it with the updated_contract!!!"""

        undo_contract_change_item_data = {
            "original_contract": old_contract.to_dict(),
            "current_contract": updated_contract.to_dict(),
        }

        undo_contract_change_item = {
            "type": UndoActions.UNDO_CONTRACT_FIELDS_CHANGED.value,
            "data": undo_contract_change_item_data
        }

        if not is_in_testing_env:
            session_cache = FameSessionCache()
            session_cache.add_item(undo_contract_change_item)

        # TODO: Future Exception: if a contract has empty required attributes

        for idx, contract in enumerate(super().contracts[:]):
            if (
                    contract.product_name == old_contract.product_name
                    and contract.sender_id == old_contract.sender_id
                    and contract.receiver_id == old_contract.receiver_id
            ):
                # changes = self.compare_objects(old_contract, updated_contract)
                # keep for debugging

                super().contracts[idx] = updated_contract
                break  #

    @property
    def agents(self) -> typing.List[models.Agent]:
        """Return the list of agents in the scenario."""
        return super().agents
