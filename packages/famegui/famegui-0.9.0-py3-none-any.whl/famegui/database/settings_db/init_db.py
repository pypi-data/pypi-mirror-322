import logging
import os.path
from contextlib import contextmanager

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from famegui.config.config import BASE_DIR
from typing import Union, List, overload

# Define the database URI
DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "database.sqlite3")}'

# Create the engine
engine = create_engine(DATABASE_URI)

# Define the base class
Base = declarative_base()

# Create a session factory
Session = sessionmaker(bind=engine)


class Setting(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    value = Column(String, nullable=False)
    setting_name = Column(String, nullable=False)
    data_type = Column(String, nullable=False)  # Adding the data_type column
    setting_label = Column(String, nullable=False)
    help_text = Column(String, nullable=True)

    def __repr__(self):
        return f"<Setting(id={self.id}, value='{self.setting_name}')>"


def get_db_engine():
    engine = create_engine(DATABASE_URI)
    return engine





@contextmanager
def init_db_session():
    # Create the table if it does not exist
    Base.metadata.create_all(engine)

    # Create a session
    session = Session()

    try:
        yield session
    finally:
        # Close the session after use
        session.close()







if __name__ == '__main__':
    logging.info("Running init_db.py")

