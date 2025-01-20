import logging
import typing
from collections import defaultdict
from typing import Optional, Dict, Any, List, Tuple

import yaml
from sqlalchemy import Column, Integer, String, inspect, MetaData, Table, text, Text, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from famegui.database.settings_db.init_db import init_db_session

Base = declarative_base()
_model_registry = {}  # Global registry to store model classes


def get_existing_table_names(yaml_path, session):
    with open(yaml_path, 'r') as file:
        yaml_content = yaml.safe_load(file)

    tables = yaml_content.get('db', {}).get('tables', {})
    inspector = inspect(session.bind)
    existing_tables = inspector.get_table_names()

    return existing_tables


def read_all_data(session):
    all_data = {}
    # Use the inspector to get the metadata of the database
    inspector = inspect(session.bind)

    all_data = {}

    # Get all table names from the database
    tables = inspector.get_table_names()

    # Loop over each table and retrieve its data
    for table_name in tables:
        query = session.execute(text(f"SELECT * FROM {table_name}"))
        rows = query.fetchall()

        # Get the column names from the table
        columns = query.keys()

        # Convert rows to dictionaries with column names as keys
        records = [dict(zip(columns, row)) for row in rows]

        # Store the result in all_data dictionary
        all_data[table_name] = records
    return all_data


def get_or_create_model(table_name, columns):
    """Get existing model class or create new one"""
    if table_name in _model_registry:
        return _model_registry[table_name]

    class_attrs = columns.copy()
    class_attrs['__tablename__'] = table_name
    ModelClass = type(table_name.capitalize(), (Base,), class_attrs)
    _model_registry[table_name] = ModelClass
    return ModelClass


def load_yaml_to_db(yaml_path, session):
    with open(yaml_path, 'r') as file:
        yaml_content = yaml.safe_load(file)

    tables = yaml_content.get('db', {}).get('tables', {})
    inspector = inspect(session.bind)
    existing_tables = inspector.get_table_names()

    for table_name, table_info in tables.items():
        table_schema = table_info.get('table_schema', {})
        preset_values = table_info.get('preset_values', [])

        # Build columns dynamically
        columns = {}
        columns['id'] = Column(Integer, primary_key=True, autoincrement=True)
        for column_name in table_schema.keys():
            if column_name == 'data_type':
                columns[column_name] = Column(Integer)
            else:
                columns[column_name] = Column(String)

        # Get or create model class
        ModelClass = get_or_create_model(table_name, columns)

        if table_name not in existing_tables:
            # Create the table only if it doesn't exist
            Base.metadata.create_all(session.bind, tables=[ModelClass.__table__])

            logging.info(f"Table '{table_name}' created.")

            insert_preset_values(ModelClass, preset_values, session, table_name)
        else:
            logging.info(f"Table '{table_name}' already exists. Skipping creation.")

            # avoid loading shortcut presets in
            # order to not override by user defined preferences

            insert_preset_values(ModelClass, preset_values, session, table_name)

    # Insert preset values


def insert_preset_values(ModelClass, preset_values, session, table_name):
    try:
        for new_record in preset_values:
            # Create filter conditions for all columns except 'id'
            filter_conditions = []
            for key, value in new_record.items():
                if key != 'id' and key != "shortcut_key":  # Exclude id from comparison
                    filter_conditions.append(getattr(ModelClass, key) == value)

            # Check if a record with the same values (excluding id) already exists
            existing_record = session.query(ModelClass).filter(*filter_conditions).first()

            if not existing_record:
                # Only insert if no matching record exists
                obj = ModelClass(**new_record)
                session.add(obj)
                logging.info(f"New preset record added to '{table_name}': {new_record}")
            else:
                logging.info(f"Skipping duplicate record in '{table_name}': {new_record}")

        session.commit()
        logging.info(f"Finished processing preset values for '{table_name}'.")
    except Exception as e:
        session.rollback()
        logging.info(f"Error inserting preset values into '{table_name}': {str(e)}")


def update_db(session, table_name, row_id, field_name, value,
              return_updated_record=False) -> typing.Union[None, dict]:
    try:
        # Reflect the table
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=session.bind)

        # Check if the field exists in the table
        if field_name not in table.c:
            logging.warning(f"Field '{field_name}' does not exist in table '{table_name}'.")
            return

        # Build the update statement
        stmt = (
            table.update()
            .where(table.c.id == row_id)  # Assuming 'id' is the primary key column
            .values({field_name: value})
        )

        # Execute the update statement
        result = session.execute(stmt)

        # Check if any row was affected
        if result.rowcount == 0:
            logging.warning(f"No row with ID {row_id} found in table '{table_name}'.")
            return

        # Commit the transaction
        session.commit()
        logging.info(f"Updated field '{field_name}' to '{value}' in table '{table_name}', row ID {row_id}.")

        # Fetch the updated record if required
        if return_updated_record:
            select_stmt = select(table).where(table.c.id == row_id)
            result = session.execute(select_stmt)
            record = result.first()
            return dict(record._mapping) if record else None

        return None



    except SQLAlchemyError as e:
        # Rollback the transaction in case of any errors
        session.rollback()
        logging.error(f"Error updating field '{field_name}' in table '{table_name}': {str(e)}")


# Example usage:
# Assuming 'session' is your SQLAlchemy session object and 'yaml_path' is the path to your YAML file.
# load_yaml_to_db(yaml_path, session)


def get_rows(
        session: Session,
        table_name: str,
        fields_to_select: List[str],
        condition: Optional[Tuple[str, Any]] = None
) -> typing.Union[Optional[List[Dict[str, Any]]], None]:
    """
    Retrieve rows from a database table, with an optional filter condition, and return selected fields.

    Args:
        session (Session): The SQLAlchemy session object to interact with the database.
        table_name (str): The name of the table from which to retrieve the rows.
        fields_to_select (List[str]): A list of strings specifying which columns/fields to return from the table.
        condition (Optional[Tuple[str, Any]]): A tuple specifying the filter condition. The first element is the column
                                               name and the second element is the value to filter by. If no condition is
                                               provided, all rows will be retrieved.

    Returns:
        Optional[List[Dict[str, Any]]]: A list of dictionaries containing the selected fields and their values for
                                        each row. Returns None if no rows are found or if an error occurs.

    Raises:
        SQLAlchemyError: If any SQLAlchemy error occurs during the query execution.

    Example:
        # To get all rows
        results = get_rows(session, "users", ["id", "name", "email"])

        # To get rows with a condition
        results = get_rows(session, "users", ["id", "name", "email"], ("email", "example@example.com"))
    """
    try:
        # Reflect the table from the database
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=session.bind)

        # Check if all the requested fields exist in the table
        for field in fields_to_select:
            if field not in table.c:
                logging.warning(f"Field '{field}' does not exist in table '{table_name}'.")
                return []

        # Build the select statement
        query = session.query(*[table.c[field] for field in fields_to_select])

        # Apply condition if provided
        if condition:
            filter_column, filter_value = condition
            if filter_column not in table.c:
                logging.warning(f"Field '{filter_column}' does not exist in table '{table_name}'.")
                return []
            query = query.filter(table.c[filter_column] == filter_value)

        # Execute the query and fetch all rows
        results = query.all()

        # If no results are found, return a message
        if not results:
            logging.warning(f"No matching records found in table '{table_name}'.")
            return []

        # Convert the results to a list of dictionaries
        rows_data = [{field: getattr(row, field) for field in fields_to_select} for row in results]

        return rows_data

    except SQLAlchemyError as e:
        # Handle any SQLAlchemy exceptions
        logging.error(f"Error retrieving data from table '{table_name}': {str(e)}")
        return None


def check_entry_exists(
        session: Session,
        table_name: str,
        filter_query_name: str,
        expected_value: Any
) -> bool:
    """
    Check if a specific entry exists in the database table based on a filter query.

    Args:
        session (Session): The SQLAlchemy session object to interact with the database.
        table_name (str): The name of the table to check the entry.
        filter_query_name (str): The column name used to filter rows (e.g., 'email' or 'id').
        expected_value (Any): The value to match in the filter (e.g., the specific email or id value).

    Returns:
        bool: True if the entry exists, False otherwise.

    Raises:
        SQLAlchemyError: If any SQLAlchemy error occurs during the query execution.
    """
    try:
        # Reflect the table from the database
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=session.bind)

        # Build the select statement
        query = session.query(table).filter(table.c[filter_query_name] == expected_value)

        # Execute the query and check if any row exists
        result = query.first()

        # Return True if result is not None (entry exists), otherwise False
        return result is not None

    except SQLAlchemyError as e:
        # Handle any SQLAlchemy exceptions
        logging.error(f"Error checking if entry exists in table '{table_name}': {str(e)}")
        return False


def get_single_row(
        session: Session,
        table_name: str,
        filter_query_name: str,
        expected_value: Any,
        fields_to_select: List[str]
) -> Optional[Dict[str, Any]]:
    """
    Retrieve a single row from a database table based on a filter query and return selected fields.

    Args:
        session (Session): The SQLAlchemy session object to interact with the database.
        table_name (str): The name of the table from which to retrieve the row.
        filter_query_name (str): The column name used to filter rows (e.g., 'email' or 'id').
        expected_value (Any): The value to match in the filter (e.g., the specific email or id value).
        fields_to_select (List[str]): A list of strings specifying which columns/fields to return from the table.

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing the selected fields and their values for the matching row.
        Returns None if no matching row is found or if an error occurs.

    Raises:
        SQLAlchemyError: If any SQLAlchemy error occurs during the query execution.

    Example:
        result = get_single_row(session, "users", "email", "example@example.com", ["id", "name", "email"])
    """

    try:
        # Reflect the table from the database
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=session.bind)

        # Check if all the requested fields exist in the table
        for field in fields_to_select:
            if field not in table.c:
                logging.info(f"Field '{field}' does not exist in table '{table_name}'.")
                return None

        # Build the select statement
        query = session.query(*[table.c[field] for field in fields_to_select]) \
            .filter(table.c[filter_query_name] == expected_value)

        # Execute the query and fetch one row
        result = query.first()

        # If result is None, return a message
        if result is None:
            logging.warning(
                f"No matching record found in table '{table_name}' for {filter_query_name} = {expected_value}.")
            return None

        # Convert the result to a dictionary if the query succeeds
        row_data = {field: getattr(result, field) for field in fields_to_select}
        return row_data

    except SQLAlchemyError as e:
        # Handle any SQLAlchemy exceptions
        logging.error(f"Error retrieving data from table '{table_name}': {str(e)}")
        return None


def insert(session: Session, table_name: str, record: Dict[str, Any]) -> bool:
    """
    Insert a single row into a database table.

    Args:
        session (Session): The SQLAlchemy session object to interact with the database.
        table_name (str): The name of the table to insert the record into.
        record (Dict[str, Any]): A dictionary containing the column names and values to insert.

    Returns:
        bool: True if the insertion is successful, False otherwise.

    Raises:
        SQLAlchemyError: If any SQLAlchemy error occurs during the query execution.
    """

    try:
        # Reflect the table from the database
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=session.bind)

        # Insert the record
        stmt = table.insert().values(**record)
        session.execute(stmt)
        session.commit()
        logging.info(f"Successfully inserted record into '{table_name}': {record}")
        return True

    except SQLAlchemyError as e:
        # Rollback in case of an error
        session.rollback()
        logging.error(f"Error inserting record into '{table_name}': {str(e)}")
        return False


def bulk_insert(session: Session, table_name: str, records: List[Dict[str, Any]]) -> bool:
    """
    Insert multiple rows into a database table in a bulk operation.

    Args:
        session (Session): The SQLAlchemy session object to interact with the database.
        table_name (str): The name of the table to insert the records into.
        records (List[Dict[str, Any]]): A list of dictionaries where each dictionary represents a row to insert.

    Returns:
        bool: True if the insertion is successful, False otherwise.

    Raises:
        SQLAlchemyError: If any SQLAlchemy error occurs during the query execution.
    """
    try:
        # Reflect the table from the database
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=session.bind)

        # Insert the records in bulk
        stmt = table.insert().values(records)
        session.execute(stmt)
        session.commit()
        logging.info(f"Successfully inserted {len(records)} records into '{table_name}'")
        return True

    except SQLAlchemyError as e:
        # Rollback in case of an error
        session.rollback()
        logging.error(f"Error inserting records into '{table_name}': {str(e)}")
        return False


def get_row_count(session: Session, table_name: str) -> int:
    """
    Get the total number of rows in a database table.

    Args:
        session (Session): The SQLAlchemy session object to interact with the database.
        table_name (str): The name of the table to count rows from.

    Returns:
        int: The total number of rows in the table. Returns -1 if an error occurs.

    Raises:
        SQLAlchemyError: If any SQLAlchemy error occurs during the query execution.
    """
    try:
        # Reflect the table from the database
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=session.bind)

        # Get the row count
        count = session.query(table).count()
        logging.info(f"Table '{table_name}' has {count} rows.")
        return count

    except SQLAlchemyError as e:
        # Handle errors
        logging.error(f"Error getting row count from '{table_name}': {str(e)}")
        return -1


def get_string_set_values_from_db():
    """Fetch all String Set Groups with Values from project DB"""
    results = None

    with init_db_session() as session:
        results = get_rows(session, "db_string_item",
                           ["string_set_item_value", "parent_string_set_group_name"])

    results = results if results is not None else []

    # Group by `parent_string_set_group_name`
    grouped_data = defaultdict(list)

    for item in results:
        group_key = item["parent_string_set_group_name"]
        grouped_data[group_key].append(item["string_set_item_value"])

    # Convert defaultdict to a regular dict
    result = dict(grouped_data)


    return result


def get_string_set_values_for_group(group_name: str):
    results = None

    with init_db_session() as session:
        results = get_rows(session, "db_string_item",
                           ["string_set_item_value", "parent_string_set_group_name"])

    results = results if results is not None else []

    results = [
        item["string_set_item_value"] for item in results if
        item["parent_string_set_group_name"] == group_name
    ]

    return results


if __name__ == "__main__":
    pass
