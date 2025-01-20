from famegui.database.db_loader.db_manager import get_single_row, check_entry_exists
from famegui.database.settings_db.init_db import init_db_session


def check_if_agent_type_has_color(agent_type_name: str):
    exist = False
    with init_db_session() as session:
        exist = check_entry_exists(session, "agent_colors_second_table", "agent_type_name", agent_type_name)

    return exist




