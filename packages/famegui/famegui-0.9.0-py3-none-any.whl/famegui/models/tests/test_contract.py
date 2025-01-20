import pytest

from famegui.models import Contract


def test_contract():
    c = Contract(
        sender_id=1,
        receiver_id=2,
        product_name="ProductName",
        delivery_interval=10,
        first_delivery_time=-20,
    )
    assert c.product_name == "ProductName"
    assert c.sender_id == 1
    assert c.display_sender_id == "#1"
    assert c.receiver_id == 2
    assert c.display_receiver_id == "#2"
    assert c.delivery_interval == 10
    assert c.first_delivery_time == -20
    assert c.expiration_time is None
    assert len(c.attributes) == 0


def test_contract_same_sender_receiver():
    # accept to build with same id for source and target
    c = Contract(
        sender_id=1,
        receiver_id=1,
        product_name="ProductName",
        delivery_interval=10,
        first_delivery_time=-20,
    )
    assert c.sender_id == c.receiver_id


def test_contract_bad_delivery_time():
    # negative delivery interval is not allowed
    with pytest.raises(ValueError):
        Contract(
            sender_id=1,
            receiver_id=1,
            product_name="ProductName",
            delivery_interval=-1,
            first_delivery_time=20,
        )
