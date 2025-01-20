import os.path
from copy import deepcopy

from fameio.input.resolver import PathResolver
from fameio.input.scenario import StringSet

from famegui.config.config import DEFAULT_FAME_WORK_DIR
from famegui.models import ScenarioLoader, Scenario


def get_default_scenario_model():
    """ Helper function to retrieve base scenario
    model obj for prototyping and testing"""

    scenario_model = ScenarioLoader.load_yaml_file(
        os.path.join(DEFAULT_FAME_WORK_DIR, "scenario.yaml"),
        PathResolver(),
        DEFAULT_FAME_WORK_DIR
    )

    return scenario_model


def add_string_set_value(scenario: Scenario, string_set_group_name: str, string_set_value: str):
    item = scenario.string_sets[string_set_group_name]

    value_dict: dict = item.to_dict()

    value_dict_copy = deepcopy(value_dict["values"])
    value_dict_copy[string_set_value] = {}

    value_dict["values"].update(value_dict_copy)
    data = StringSet.from_dict(value_dict)

    scenario.string_sets[string_set_group_name] = data



if __name__ == "__main__":
    model = get_default_scenario_model()

    ScenarioLoader.save_to_yaml_file(model, os.path.join(DEFAULT_FAME_WORK_DIR, "scenario.yaml"))
