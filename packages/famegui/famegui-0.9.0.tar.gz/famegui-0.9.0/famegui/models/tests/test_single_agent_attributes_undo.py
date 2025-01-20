import os
from copy import deepcopy

from fameio.input.resolver import PathResolver

from famegui_runtime_helper.attribute_dict_formatting_helper import build_simple_attr_dict
from famegui_runtime_helper.dict_hash_helper import hash_dict
from famegui import models
from famegui.config.config import DEFAULT_FAME_WORK_DIR
from famegui.fame_tools.dict_tools import remove_none_values_and_empty_elements


def test_simple_attribute_update():
    assert os.path.exists(DEFAULT_FAME_WORK_DIR), f"Path does not exist: {DEFAULT_FAME_WORK_DIR}"

    file_path = os.path.join(DEFAULT_FAME_WORK_DIR, "scenario.yaml")

    scenario_model = models.ScenarioLoader.load_yaml_file(
        file_path, PathResolver(), DEFAULT_FAME_WORK_DIR)

    assert scenario_model is not None

    first_agent = deepcopy(scenario_model.agents[0])

    data_out = {}

    flat_full_name_labeled_values = first_agent.get_flat_agent_attributes_dict()

    flat_full_name_labeled_values_updated = deepcopy(flat_full_name_labeled_values)

    flat_full_name_labeled_values_updated["GateClosureInfoOffsetInSeconds"] = 29

    agent_type_name = first_agent.type_name

    for attr_name, attr in scenario_model.schema.agent_types[agent_type_name].attributes.items():
        iter_tmp_dict = build_simple_attr_dict(
            attr, flat_full_name_labeled_values_updated, agent_type_name)
        data_out[attr_name] = iter_tmp_dict[attr_name] if attr_name in iter_tmp_dict else iter_tmp_dict

    data_out = remove_none_values_and_empty_elements(data_out)

    for attr_name_sub, attr_sub in data_out.items():
        value = data_out[attr_name_sub]
        first_agent.attributes[attr_name_sub] = value

    scenario_model.update_agent(first_agent)

    new_flat_full_name_labeled_values = first_agent.get_flat_agent_attributes_dict()

    # agent attributes must be changed

    assert hash_dict(flat_full_name_labeled_values) != hash_dict(new_flat_full_name_labeled_values)
