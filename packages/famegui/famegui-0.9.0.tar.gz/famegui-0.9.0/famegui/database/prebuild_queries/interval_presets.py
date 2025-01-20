import typing

from famegui.database.db_loader.db_manager import get_rows
from famegui.database.settings_db.init_db import init_db_session


def get_delivery_interval_presets() -> typing.List[typing.Dict]:
    """
        Retrieve all delivery interval presets from the 'delivery_interval_presets' table.

        This function uses an active database session to query the 'delivery_interval_presets'
        table and returns a list of dictionaries containing the 'preset_duration_in_seconds'
        and 'preset_label' fields for each row.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries with 'preset_duration_in_seconds'
                                  and 'preset_label' for each delivery interval preset.
        """
    with init_db_session() as session:
        res_list = get_rows(session, "delivery_interval_presets", ["preset_duration_in_seconds", "preset_label"])



    return res_list
