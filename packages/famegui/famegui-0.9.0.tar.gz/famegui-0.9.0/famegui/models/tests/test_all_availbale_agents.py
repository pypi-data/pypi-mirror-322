import os
from copy import deepcopy

from fameio.input.resolver import PathResolver

from famegui_runtime_helper.attribute_dict_formatting_helper import build_simple_attr_dict
from famegui_runtime_helper.dict_hash_helper import hash_dict
from famegui import models
from famegui.config.config import DEFAULT_FAME_WORK_DIR
from famegui.models.tests.test_utils.test_utils import replace_first_number



def test_all_available_agents_for_update():
    assert os.path.exists(DEFAULT_FAME_WORK_DIR), f"Path does not exist: {DEFAULT_FAME_WORK_DIR}"

    file_path = os.path.join(DEFAULT_FAME_WORK_DIR, "scenario.yaml")

    scenario_model = models.ScenarioLoader.load_yaml_file(
        file_path, PathResolver(), DEFAULT_FAME_WORK_DIR)

    assert scenario_model is not None

    already_fetched_agent_types = set()

    first_agent_type_matches = []

    for agent in scenario_model.agents:

        if already_fetched_agent_types.__contains__(agent.type_name):
            continue

        first_agent_type_matches.append(agent)

        already_fetched_agent_types.add(agent.type_name)

    first_agent_type_matches = [agent for agent in first_agent_type_matches if
                                agent.attributes and scenario_model.schema.agent_types[
                                    agent.type_name
                                ].attributes]

    for item in first_agent_type_matches:
        flat_data = item.get_flat_agent_attributes_dict()

        original_data = deepcopy(flat_data)

        updated_flat_data = deepcopy(flat_data)

        agent_type_name = item.type_name

        data_out = {}

        updated_flat_data, _ = replace_first_number(updated_flat_data)

        assert hash_dict(updated_flat_data) != hash_dict(
            original_data)  # check if test is able to replace primitive value

        for attr_name, attr in scenario_model.schema.agent_types[agent_type_name].attributes.items():
            iter_tmp_dict = build_simple_attr_dict(
                attr, updated_flat_data, agent_type_name)
            data_out[attr_name] = iter_tmp_dict[attr_name] if attr_name in iter_tmp_dict else iter_tmp_dict

        # test undo

        for attr_name, attr in scenario_model.schema.agent_types[agent_type_name].attributes.items():
            iter_tmp_dict = build_simple_attr_dict(
                attr, original_data, agent_type_name)
            data_out[attr_name] = iter_tmp_dict[attr_name] if attr_name in iter_tmp_dict else iter_tmp_dict

        newest_attr_data = item.get_flat_agent_attributes_dict()

        assert hash_dict(newest_attr_data) == hash_dict(
            original_data)
