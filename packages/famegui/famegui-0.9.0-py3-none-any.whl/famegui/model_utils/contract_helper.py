from famegui.models import Scenario


def get_contract_from_fields(scenario: Scenario, product_name: str,
                             receiver_id: int, sender_id: int):


    result_list = [contract for contract in scenario.contracts if contract.sender_id == sender_id
                   and contract.receiver_id == receiver_id and contract.product_name == product_name]

    if len(result_list) == 0:
        raise ValueError(f"Specified Contract does not exists:: check the fields "
                         f" product_name: {str(product_name)}; receiver_id: {str(receiver_id)}; sender_id: {str(receiver_id)} ")

    return result_list[0]
