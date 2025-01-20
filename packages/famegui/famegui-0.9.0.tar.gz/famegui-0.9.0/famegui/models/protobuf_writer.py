import logging
import os

from fameio.input.resolver import PathResolver
from fameio.input.validator import SchemaValidator
from fameio.input.writer import ProtoWriter

import famegui.models as models


def write_protobuf_output(scenario: models.Scenario, output_path: str, path_resolver: PathResolver) -> None:
    logging.debug("generating protobuf output to '{}'".format(output_path))
    assert os.path.isabs(output_path)

    timeseries_manager = SchemaValidator.validate_scenario_and_timeseries(scenario, path_resolver)

    writer = ProtoWriter(output_path, timeseries_manager)
    writer.write_validated_scenario(scenario)
    logging.info("protobuf output was generated to '{}'".format(output_path))
