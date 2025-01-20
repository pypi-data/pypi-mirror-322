import typing
from enum import Enum

from famegui.database.db_loader.db_manager import get_single_row
from famegui.database.settings_db.init_db import init_db_session

DB_SETTING_TABLE_NAME = "settings"
DB_SETTING_NAME_FIELD = "setting_name"


class FameContractGraphItemSettings(object):
    CONTRACT_LINE_ANGLE = "contract_line_angle"
    CONTRACT_LINE_WIDTH = "contract_line_width"


class FameGeneralRuntimeSetting:
    AMOUNT_OF_UNDO_STEPS = "amount_of_undo_steps"


def get_setting_value(setting_name_entry: str, fallback_value: typing.Union[str, int]) -> str:
    """
    Retrieve the value of a setting by its name from the settings table.
    If no setting is found, the fallback value is returned.

    Args:
        setting_name_entry (str): The name of the setting to search for.
        fallback_value (str): The value to return if the setting is not found.

    Returns:
        str: The value of the setting if found, otherwise the fallback value.
    """
    with init_db_session() as session:
        result = get_single_row(session, DB_SETTING_TABLE_NAME, DB_SETTING_NAME_FIELD, setting_name_entry, ["value"])

    # Return the result if found, otherwise return the fallback value
    if result and "value" in result:
        return result["value"]


    else:
        return fallback_value


if __name__ == "__main__":

    value = int(get_setting_value(FameContractGraphItemSettings.CONTRACT_LINE_ANGLE,
                                  20))
