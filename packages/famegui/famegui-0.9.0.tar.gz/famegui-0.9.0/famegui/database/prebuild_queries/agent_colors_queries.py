import typing

from sqlalchemy import MetaData, Table
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from famegui.database.db_loader.db_manager import get_row_count, bulk_insert, get_rows, get_single_row
from famegui.database.settings_db.init_db import init_db_session


def colors_for_agent_types_exit_in_db() -> bool:
    """
    Check if the db has specified colors for agent types
    """
    row_count = 0
    with init_db_session() as session:
        row_count = get_row_count(session, "agent_colors")

    return row_count > 0


def get_all_colors_for_agent_types() -> typing.Union[None, typing.List[typing.Dict]]:
    """
    Retrieve all colors related to agent all available agent types
    """
    res_list = []

    with init_db_session() as session:
        res_list = get_rows(session, "agent_colors",
                            ["agent_color_hex_code", "agent_type_name"])

    return res_list


def get_color_for_agent_type(agent_type: str) -> typing.Union[str, None]:
    """
    Retrieves hex color code for given agent type from database ( if available) else None.

    Args:
        agent_type (str): The type of agent to look up

    Returns:
            str | None: Hex color code if found, None if not found
        """
    res = None
    with init_db_session() as session:
        res = get_single_row(session, "agent_colors",
                             "agent_type_name",
                             agent_type,
                             ["agent_color_hex_code"])
    return res["agent_color_hex_code"] if res is not None else None


def bulk_insert_colors(type_to_color_dict: dict):
    """
    Bulk insert colors to populate the db with randomly picked colors for every agent type
    """
    map_fields = lambda key, color: {
        "agent_color_hex_code": color,
        "agent_type_name": key,
        "data_type": 0  # string
    }

    formatted_records = [map_fields(key, item) for key, item in type_to_color_dict.items()]

    with init_db_session() as session:
        bulk_insert(session, "agent_colors", formatted_records)
