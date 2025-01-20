import os

from famegui import models
import fameio.input.schema as fameio

_dir = os.path.dirname(__file__)
_schema_path = os.path.abspath(os.path.join(_dir, "../../../testing_resources/schemas/schema-example.yaml"))


def test_schema_loader():
    yaml_path = os.path.abspath(_schema_path)
    schema = models.Schema.load_yaml_file(yaml_path)

    assert len(schema.agent_types) == 25

    assert "Biogas" in schema.agent_types
    assert schema.agent_types["Biogas"].name == "Biogas"
    assert len(schema.agent_types["Biogas"].attributes) == 9

    assert "DemandTrader" in schema.agent_types
    assert "Loads" in schema.agent_types["DemandTrader"].attributes
    assert schema.agent_types["DemandTrader"].attributes["Loads"].is_mandatory is True
    assert schema.agent_types["DemandTrader"].attributes["Loads"].attr_type == fameio.AttributeType.BLOCK

    assert "VariableRenewableOperator" in schema.agent_types
    assert len(schema.agent_types["VariableRenewableOperator"].attributes) == 6

    assert (
        schema.agent_types["VariableRenewableOperator"].attributes["InstalledPowerInMW"].attr_type
        == fameio.AttributeType.TIME_SERIES
    )

    assert schema.agent_types["VariableRenewableOperator"].attributes["SupportInstrument"].values == [
        "FIT",
        "MPVAR",
        "MPFIX",
        "CFD",
        "CP",
        "FINANCIAL_CFD"
    ]
