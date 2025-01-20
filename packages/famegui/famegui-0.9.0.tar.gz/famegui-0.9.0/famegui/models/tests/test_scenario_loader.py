import logging
import os
import pytest
import typing

import yaml

from famegui.models import ScenarioLoader
import fameio.input.loader as fameio

_dir = os.path.dirname(__file__)


class CustomPathResolver(fameio.PathResolver):
    def resolve_yaml_imported_file_pattern(
            self, root_path: str, file_pattern: str
    ) -> typing.List[str]:
        # adjust root path to where the schema is stored
        root_path = os.path.abspath(_dir + "../../../../testing_resources")
        result = super().resolve_yaml_imported_file_pattern(root_path, file_pattern)
        assert len(result) > 0
        return result


def test_load_valid_yaml_file():
    path_resolver = CustomPathResolver()
    fame_work_dir = os.path.abspath(_dir + "../../../../testing_resources")

    s = ScenarioLoader.load_yaml_file(_dir + "/files/scenario.yaml", path_resolver, fame_work_dir)

    assert len(s.agents) == 50
    assert s.agents[0].type_name == "DayAheadMarketSingleZone"
    assert s.agents[0].display_id == "#1"
    assert s.agents[1].type_name == "CarbonMarket"
    assert s.agents[1].display_id == "#3"
    assert s.agents[2].type_name == "FuelsMarket"
    assert s.agents[2].display_id == "#4"
    assert s.agents[3].type_name == "DemandTrader"
    assert s.agents[3].display_id == "#100"

    assert len(s.contracts) == 294
    assert s.contracts[0].sender_id == 2000
    assert s.contracts[0].display_receiver_id == "#500"
    assert s.contracts[0].product_name == "PowerPlantPortfolio"
    # TODO: enable these tests once Scenario.add_contract() has been updated to link inputs/outputs
    # assert s.agents[3].outputs == [3]
    # assert s.agents[2].inputs == [4]

    assert s.contracts[1].display_sender_id == "#2001"
    assert s.contracts[1].receiver_id == 501
    assert s.contracts[1].product_name == "PowerPlantPortfolio"
    # assert s.agents[5].outputs == [4]
    # assert s.agents[4].inputs == [5]

    assert s.contracts[2].sender_id == 2002
    assert s.contracts[2].receiver_id == 502
    assert s.contracts[2].product_name == "PowerPlantPortfolio"
    # assert s.agents[2].outputs == [1]
    # assert s.agents[1].inputs == [2]


def is_yaml_empty(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read().strip()  # Remove any leading/trailing whitespace
            if not content:
                return True  # File is empty or only whitespace

            # Attempt to parse the YAML content
            yaml_data = yaml.safe_load(content)
            if yaml_data is None:  # YAML content is valid but empty
                return True
    except Exception as e:
        logging.info(f"Error reading YAML file: {e}")
    return False


def test_load_empty_yaml_file():
    # we accept empty scenario files (to not block the user in the GUI)
    path_resolver = CustomPathResolver()
    fame_work_dir = os.path.abspath(_dir + "../../../../testing_resources")

    empty_scenario_path = _dir + "/files/empty.yaml"

    assert is_yaml_empty(empty_scenario_path) == True

    # todo: talk to DLR:: empty scenario is not loading due to lower_keys function

    ScenarioLoader.load_yaml_file(_dir + "/files/empty.yaml", path_resolver, fame_work_dir)


def test_load_single_agent_yaml_file():
    path_resolver = CustomPathResolver()
    fame_work_dir = os.path.abspath(_dir + "../../../../testing_resources")

    s = ScenarioLoader.load_yaml_file(_dir + "/files/single_agent.yaml", path_resolver, fame_work_dir)
    assert len(s.agents) == 1
    assert len(s.contracts) == 0


def test_load_single_contract_yaml_file():
    path_resolver = CustomPathResolver()
    fame_work_dir = os.path.abspath(_dir + "../../../../testing_resources")
    # TODO: this scenario file should be rejected (contract references missing agents)
    s = ScenarioLoader.load_yaml_file(
        _dir + "/files/single_contract.yaml", path_resolver, fame_work_dir
    )
    assert len(s.agents) == 0
    assert len(s.contracts) == 1


def test_load_invalid_path():
    path_resolver = CustomPathResolver()
    fame_work_dir = os.path.abspath(_dir + "../../../../testing_resources")
    with pytest.raises(FileNotFoundError):
        ScenarioLoader.load_yaml_file(_dir + "/invalid_path", path_resolver, fame_work_dir)
