import os

from sqlalchemy import MetaData

from famegui.config.config import BASE_DIR
from famegui.database.settings_db.init_db import init_db_session, get_db_engine


def load_db_data():
    # Initialize MetaData
    metadata = MetaData()

    # Reflect all tables from the database
    metadata.reflect(bind=get_db_engine())

    # List all table names
    table_names = metadata.tables.keys()

    yaml_file_path = os.path.join(BASE_DIR, "config", 'settings_config.yaml')

    from famegui.database.db_loader.db_manager import load_yaml_to_db

    with init_db_session() as session:
        load_yaml_to_db(yaml_file_path, session)
