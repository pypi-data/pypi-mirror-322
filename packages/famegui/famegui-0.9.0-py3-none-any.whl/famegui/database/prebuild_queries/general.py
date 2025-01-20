from famegui.database.db_loader.db_manager import get_rows
from famegui.database.settings_db.init_db import init_db_session


def get_stored_shortcuts() -> list:
    with init_db_session() as session:
        res_list = get_rows(session, "shortcuts",
                            ["shortcut_name", "shortcut_key"])

    return res_list#
