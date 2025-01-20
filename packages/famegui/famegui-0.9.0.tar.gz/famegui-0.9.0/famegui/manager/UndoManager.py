import logging

import ujson as json
import os
from pathlib import Path

from PySide6.QtCore import QObject

from famegui_runtime_helper.dict_hash_helper import hash_dict
from famegui_runtime_helper.fame_session_cache import FameSessionCache
from famegui.config.config import BASE_DIR
from famegui.path_config import CACHE_TRACKING_DB_PATH, CACHE_TRACKING_DB_DIR
from famegui.undo_utils.contract_utils import ORIGINAL_CONTRACT_KEY, MANIPULATED_CONTRACT_KEY
from famegui.undo_utils.undo_constants import UndoActions


def bulk_save_old_agent_coords(agent_ctrl_dict: dict,
                               agent_ctrl_dict_post_transformational_coords: dict):
    with open(CACHE_TRACKING_DB_PATH, "r", encoding="utf-8") as file:
        json_db_data = json.loads(file.read())

    data_list = json_db_data["data_list"]

    if hash_dict(agent_ctrl_dict_post_transformational_coords) == hash_dict(agent_ctrl_dict):
        raise ValueError("Pre and Post-Transformational Coords cannot be the same !")

    if len(data_list) >= 2:
        first_item = data_list[0]
        last_item = data_list[len(data_list) - 1]
        item_idx = first_item["index"]
        item_idx_last = last_item["index"]

        if item_idx > item_idx_last:
            last_item_in_list_by_idx = first_item
        else:
            last_item_in_list_by_idx = last_item
        last_item_idx = last_item_in_list_by_idx["index"]

        new_idx = last_item_idx + 1

    else:
        new_idx = len(data_list) + 1

    undo_step = {
        "type": "agent_re_arrange",
        "data": {
            "agent_coords": agent_ctrl_dict,
            "agent_ctrl_dict_post_transformational_coords": agent_ctrl_dict_post_transformational_coords
        },
        "index": new_idx
    }

    session_db = FameSessionCache()

    session_db.add_item(undo_step)

    data_list.append(undo_step)

    with open(CACHE_TRACKING_DB_PATH, "w", encoding="utf-8") as file:
        file.write(json.dumps(json_db_data))


class UndoManager(QObject):

    def __init__(self, controller):
        super().__init__()
        self.check_or_create_cache_db()

        self.session_db = FameSessionCache()

        self.controller = controller

    @staticmethod
    def check_or_create_cache_db():
        json_db_data = {"data_list": [], "current_index": 0}

        os.makedirs(CACHE_TRACKING_DB_DIR, exist_ok=True)

        file_path = Path(CACHE_TRACKING_DB_PATH)

        if not file_path.is_file():
            with open(CACHE_TRACKING_DB_PATH, "w+", encoding="utf-8") as file:
                file.write(json.dumps(json_db_data))

    def get_current_cache_index(self):
        cache_db = os.path.join(BASE_DIR, "cache", "db", "db.json")

        data_dict = {}

        with open(cache_db, "r", encoding="utf-8") as db_file:
            data_dict = json.loads(db_file.read())

        return data_dict["current_index"]

    def add_new_undo_step(self, data_dict):
        cache_db = os.path.join(BASE_DIR, "cache", "db", "db.json")

        current_db = {}

        with open(cache_db, "r", encoding="utf-8") as read_db:
            current_db = json.loads(read_db.read())

        data_list = current_db["data_list"]
        data_list.append(data_dict)

        self.session_db.add_item(data_dict)

        with open(cache_db, "w+", encoding="utf-8") as db_file:
            db_file.write(json.dumps(current_db))

    def save_project_properties_manipulation(self, original_props: dict, updated_props: dict):

        data = {
            "type": UndoActions.UNDO_SCENARIO_PROPERTIES.value,
            "data": {
                "original_props": original_props,  # use for undo
                "updated_props": updated_props,  # use for redo
            },
            "index": self.get_current_cache_index() + 1
        }

        self.add_new_undo_step(data)

    def save_moved_agent(self, agent_x, agent_y, agent_id, old_x, old_y):
        data = {
            "type": "agent_moved",
            "data": {
                "agent": {
                    "agent_x": agent_x,
                    "agent_y": agent_y,
                    "agent_id": agent_id
                },
                "original_agent": {
                    "agent_x": old_x,
                    "agent_y": old_y,
                    "agent_id": agent_id

                }
            },
            "index": self.get_current_cache_index() + 1
        }

        self.add_new_undo_step(data)

    def peek_last_cache_file(self):
        # List all files in the directory
        result = None
        cache_db = os.path.join(BASE_DIR, "cache", "db", "db.json")

        with open(cache_db, "r", encoding="utf-8") as f:
            data = json.load(f)
            current_index = int(data["current_index"])
            data_list = data["data_list"]
            for item in data_list:
                if item["index"] == len(data_list) - current_index:
                    result = item
                    break

        return result["file_name"]

    def perform_last_queued_redo(self):
        """Performing redo by inverting the undo actions the """
        result = self.session_db.redo_last_item()
        logging.info("Redo inside ....")
        logging.info(result)

        if result is None:
            return

        if result["type"] == UndoActions.UNDO_CONTRACT_FIELDS_CHANGED.value:
            contract_data = result["data"]

            original_contract = contract_data[MANIPULATED_CONTRACT_KEY]
            current_contract = contract_data[ORIGINAL_CONTRACT_KEY]

            self.controller.perform_contract_fields_undo(current_contract, original_contract)

        if result["type"] == UndoActions.UNDO_AGENT_ATTRIBUTES_CHANGED.value:
            self.controller.perform_agent_attributes_undo(result["data"])

        if result["type"] == "agent_re_arrange":
            agent_coords_data = result["data"]["agent_ctrl_dict_post_transformational_coords"]

            self.controller.re_render_scene(agent_coords_data)

        if result["type"] == UndoActions.UNDO_SCENARIO_PROPERTIES.value:
            self.controller.apply_properties(result["data"]["updated_props"])

        if result["type"] == "agent_moved":
            agent_data = result["data"]["original_agent"]

            self.controller.set_agent_display_xy(agent_data["agent_id"], agent_data["agent_x"],
                                                 agent_data["agent_y"])

    def perform_last_queued_undo(self):
        result = self.session_db.get_last_item()

        if result is None:
            return

        if result["type"] == UndoActions.UNDO_CONTRACT_FIELDS_CHANGED.value:
            contract_data = result["data"]

            original_contract = contract_data[ORIGINAL_CONTRACT_KEY]
            current_contract = contract_data[MANIPULATED_CONTRACT_KEY]

            self.controller.perform_contract_fields_undo(current_contract, original_contract)

        if result["type"] == UndoActions.UNDO_AGENT_ATTRIBUTES_CHANGED.value:
            self.controller.perform_agent_attributes_undo(result["data"])

        if result["type"] == UndoActions.UNDO_SCENARIO_PROPERTIES.value:
            self.controller.apply_properties(result["data"]["original_props"])

        if result["type"] == "agent_re_arrange":
            agent_coords_data = result["data"]["agent_coords"]

            self.controller.re_render_scene(agent_coords_data)

        if result["type"] == "agent_moved":
            agent_data = result["data"]["agent"]

            self.controller.set_agent_display_xy(agent_data["agent_id"], agent_data["agent_x"],
                                                 agent_data["agent_y"])

    def perform_undo(self):

        self.perform_last_queued_undo()

    def perform_redo(self):

        self.perform_last_queued_redo()
