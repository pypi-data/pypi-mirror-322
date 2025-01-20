import pytest

from famegui.models import Agent
import fameio.input.scenario.attribute as fameio


def test_agent():
    a = Agent(1, "FuelsMarket")
    assert a.id == 1
    assert a.display_id == "#1"
    assert a.type_name == "FuelsMarket"
    assert len(a.inputs) == 0
    assert len(a.outputs) == 0
    assert len(a.attributes) == 0

    a.add_attribute("NATURAL_GAS", fameio.Attribute("attr_name", "prices_gas.csv"))
    assert len(a.attributes) == 1
    assert a.attributes["NATURAL_GAS"].value == "prices_gas.csv"

    # try to add with same name
    with pytest.raises(ValueError):
        a.add_attribute("NATURAL_GAS", fameio.Attribute("attr_name", "other.csv"))

    # check it didn't change
    assert a.attributes["NATURAL_GAS"].value == "prices_gas.csv"
