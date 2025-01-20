import os

from famegui.models import Agent, Contract, GeneralProperties, Scenario, Schema

_dir = os.path.dirname(__file__)
_schema_path = os.path.abspath(
    os.path.join(_dir, "../../../testing_resources/schemas/schema-example.yaml")
)


def test_scenario_creation_from_scratch():
    # create empty scenario
    schema = Schema.load_yaml_file(_schema_path)
    props = GeneralProperties.make_default()
    s = Scenario(schema, props)
    assert len(s.agents) == 0
    assert len(s.contracts) == 0

    s.add_agent(Agent(1, "type1"))
    s.add_agent(Agent(2, "type2"))
    s.add_agent(Agent(3, "type3"))

    # TODO: fameio should reject duplicated agent
    # with pytest.raises(ValueError):
    #    s.add_agent(Agent(1, "type1"))
    # assert len(s.agents) == 3
    # assert len(s.contracts) == 0
    # assert s.agents[1].inputs == []
    # assert s.agents[1].outputs == []
    # assert s.agents[2].inputs == []
    # assert s.agents[2].outputs == []

    s.add_contract(Contract(1, 2, "contract 1->2", 10, 20))
    assert len(s.agents) == 3
    assert s.agents[1].inputs == []
    # TODO: enable these tests once Scenario.add_contract() has been updated to link inputs/outputs
    # assert s.agents[1].outputs == [2]
    # assert s.agents[2].inputs == [1]
    # assert s.agents[2].outputs == []
    assert len(s.contracts) == 1
    assert s.contracts[0].sender_id == 1
    assert s.contracts[0]._receiver_id == 2
    assert s.contracts[0].product_name == "contract 1->2"
    assert s.contracts[0].delivery_interval == 10
    assert s.contracts[0].first_delivery_time == 20
    assert s.contracts[0].expiration_time is None

    # accept contract with same sender / receiver
    s.add_contract(Contract(1, 1, "contract 1->1", 11, 21))
    assert len(s.contracts) == 2
    assert s.contracts[1].sender_id == 1
    assert s.contracts[1]._receiver_id == 1
    assert s.contracts[1].product_name == "contract 1->1"

    # bad contracts
    # TODO: fameio should reject those bad contracts
    # with pytest.raises(ValueError):
    #    s.add_contract(Contract(0, 1, "bad contract", 11, 21))  # bad sender
    # with pytest.raises(ValueError):
    #    s.add_contract(Contract(1, 0, "bad contract", 11, 21))  # bad receiver
    # assert len(s.contracts) == 2
