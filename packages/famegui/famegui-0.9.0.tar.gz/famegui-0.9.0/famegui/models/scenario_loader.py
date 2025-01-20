import logging
import os
from pathlib import Path

import fameio.input.loader as fameio
import yaml
from fameio.input.scenario.fameiofactory import FameIOFactory

import famegui.models as models
from famegui.config.config import DEFAULT_FAME_WORK_DIR


def _check_all_agents_have_display_coords(scenario: models.Scenario):
    if len(scenario.agents) == 0:
        return True
    for a in scenario.agents:
        if a.display_xy is None:
            return False
        return True


def insert_work_dir_into_paths(data, fame_work_dir):
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = insert_work_dir_into_paths(value, fame_work_dir)  # Recurse for nested dictionaries
    elif isinstance(data, list):
        data = [insert_work_dir_into_paths(item, fame_work_dir) for item in data]  # Recurse for lists
    elif isinstance(data, str) and data.startswith("./"):
        data = data.replace("./", fame_work_dir + "/", 1)  # Replace only the first instance
    return data


class CustomFameIOFactory(FameIOFactory):
    @staticmethod
    def new_schema_from_dict(definitions: dict) -> models.Schema:
        return models.Schema.from_dict(definitions)

    @staticmethod
    def new_general_properties_from_dict(definitions: dict) -> models.GeneralProperties:
        return models.GeneralProperties.from_dict(definitions)

    @staticmethod
    def new_agent_from_dict(definitions: dict) -> models.Agent:
        return models.Agent.from_dict(definitions)

    @staticmethod
    def new_contract_from_dict(definitions: dict) -> models.Contract:
        return models.Contract.from_dict(definitions)


class ScenarioLoader:

    @staticmethod
    def load_predefined_options():

        example_schema_path = os.path.join(DEFAULT_FAME_WORK_DIR, "schemas", "schema-example.yaml")
        example_props_path = os.path.join(DEFAULT_FAME_WORK_DIR, "props", "properties-example.yaml")

        with open(example_schema_path, 'r') as file:
            example_schema = yaml.safe_load(file)

        with open(example_props_path, 'r') as file:
            example_props = yaml.safe_load(file)

        return {"schema": example_schema,
                "GeneralProperties": example_props}

    @staticmethod
    def load_yaml_file(file_path: str, path_resolver: fameio.PathResolver,
                       fame_work_dir: str) -> models.Scenario:
        """Load (read and parse) a YAML scenario file"""
        file_path = os.path.abspath(file_path)

        yaml_dict = fameio.load_yaml(Path(file_path), path_resolver)

        yaml_dict = yaml_dict if yaml_dict is not None else ScenarioLoader.load_predefined_options()

        scenario = models.Scenario.from_dict(definitions=yaml_dict,
                                             factory=CustomFameIOFactory())


        # check if layout generation is necessary
        if not _check_all_agents_have_display_coords(scenario):
            logging.info("at least one Agent does not have graph layout coords (X,Y): applying layouting to all agents")
            models.layout_agents(scenario)
            for agent in scenario.agents:

                if agent.display_xy is not None:
                    continue
                agent.set_display_xy(0, 0)

        assert _check_all_agents_have_display_coords(scenario)

        return scenario

    @staticmethod
    def save_to_yaml_file(scenario: models.Scenario, file_path: str):
        """Save the given scenario to a YAML file"""
        logging.info("saving scenario to file {}".format(file_path))

        assert os.path.isabs(file_path)

        try:
            with open(file_path, "w") as f:
                export_to_dict = scenario.to_export_to_yaml_dict()

                yaml.dump(export_to_dict, f)
        except Exception as e:
            raise RuntimeError("failed to save scenario to file '{}'".format(file_path)) from e
