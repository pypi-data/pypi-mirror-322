import os

import pytest
import ujson
from fameio.input.resolver import PathResolver
from famegui import models
from famegui.config.config import DEFAULT_FAME_WORK_DIR
from famegui.data_manager.string_set_manager import get_pre_defined_string_set_values_from_scenario

@pytest.fixture
def scenario_file_path():
    """Fixture to ensure the scenario file exists and provide its path."""
    assert os.path.exists(DEFAULT_FAME_WORK_DIR), f"Path does not exist: {DEFAULT_FAME_WORK_DIR}"
    file_path = os.path.join(DEFAULT_FAME_WORK_DIR, "scenario.yaml")
    assert os.path.exists(file_path), f"Scenario file does not exist: {file_path}"
    return file_path


def test_load_scenario_model(scenario_file_path):
    """Test to load the scenario model and verify its integrity."""
    scenario_model = models.ScenarioLoader.load_yaml_file(
        scenario_file_path,
        PathResolver(),
        DEFAULT_FAME_WORK_DIR
    )
    assert scenario_model is not None, "Failed to load scenario model"

def test_pre_defined_string_set_values(scenario_file_path):
    """Test to retrieve pre-defined string set values from the scenario model."""
    scenario_model = models.ScenarioLoader.load_yaml_file(
        scenario_file_path,
        PathResolver(),
        DEFAULT_FAME_WORK_DIR
    )
    string_set_data_dict = get_pre_defined_string_set_values_from_scenario(scenario_model)
    assert string_set_data_dict is not None, "Failed to retrieve string set data"
    assert isinstance(string_set_data_dict, dict), "String set data should be a dictionary"
