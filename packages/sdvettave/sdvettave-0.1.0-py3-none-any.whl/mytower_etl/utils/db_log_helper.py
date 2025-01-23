import logging
from typing import Dict
from airflow.hooks.base import BaseHook
from sqlalchemy import create_engine, Table, Column, MetaData, String, Integer, exc, inspect, Text
from sqlalchemy.exc import NoSuchModuleError
from sqlalchemy import inspect, insert, exc, text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import Date

 
from typing import Dict, List, Any
from sqlalchemy.sql import text


class DBLogHelper:
    def __init__(self, connection_id: str, table_name: str, schema: str = None, extra_columns: Dict[str, str] = None):
        """
        Initializes the DBLogHelper.

        Args:
            connection_id (str): Airflow connection ID for the database.
            table_name (str): Name of the table to log to.
            schema (str): Schema name for the table.
            extra_columns (Dict[str, str]): Additional columns to add to the table (column_name: column_type).
        """
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(self.__class__.__name__)

        # Store table name, schema, and additional columns
        self.table_name = table_name
        self.schema = schema
        self.extra_columns = extra_columns or {}

        # Get database connection from Airflow
        connection = BaseHook.get_connection(connection_id)
        connection_uri = 'postgresql://{}:{}@{}:{}/{}'.format(
            connection.login,
            connection.password,
            connection.host,
            connection.port,
            connection.schema
        )

        # Ensure SQLAlchemy can understand the URI
        try:
            executation_options = {}
            if schema:
                executation_options = {"schema_translate_map": {None: schema}}
            self.engine = create_engine(connection_uri, execution_options=executation_options)
            self.logger.info(f"Successfully created database engine for URI '{connection_uri}'.")
        except NoSuchModuleError as e:
            self.logger.error(f"Failed to create engine with the provided URI '{connection_uri}': {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error while creating engine with the URI '{connection_uri}': {e}")
            raise

        # Ensure the schema exists
        if self.schema:
            self._ensure_schema_exists()

        # Create or update the table
        self.metadata = MetaData(schema=self.schema)
        self.table = self._get_or_create_table()


    def _ensure_schema_exists(self):
        """
        Ensures that the schema exists in the database.
        """
        try:
            schema_create_stmt = f"CREATE SCHEMA IF NOT EXISTS {self.schema}"
            self.engine.execute(text(schema_create_stmt))
            self.logger.info(f"Schema '{self.schema}' ensured to exist.")
        except exc.SQLAlchemyError as e:
            self.logger.error(f"Failed to ensure schema '{self.schema}' exists: {e}")
            raise

    def _get_or_create_table(self):
        """
        Creates or updates the logging table.
        """
        # Base table definition
        columns = [
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('log_key', String, nullable=True),
        ]

        # Define SQL type mappings
        sql_type_mappings = {
            "string": "VARCHAR(255)",  # Example default length
            "integer": "INTEGER",
            "date": "DATE",
            "text": "TEXT"
        }

        # Add extra columns dynamically
        for column_name, column_type in self.extra_columns.items():
            column_type = column_type.lower()
            if column_type in sql_type_mappings:
                columns.append(Column(column_name, eval(column_type.capitalize())))
            else:
                self.logger.warning(f"Unsupported column type '{column_type}' for '{column_name}'. Skipping.")

        table = Table(self.table_name, self.metadata, *columns, extend_existing=True)

        # Create the table or update schema
        with self.engine.connect() as connection:
            try:
                inspector = inspect(connection)
                if not inspector.has_table(self.table_name, schema=self.schema):
                    # Create the table if it doesn't exist
                    self.metadata.create_all(self.engine, checkfirst=True)
                    self.logger.info(f"Table '{self.table_name}' in schema '{self.schema}' created with columns: {list(self.extra_columns.keys())}")
                else:
                    # Check for missing columns and add them dynamically
                    existing_columns = [col["name"] for col in inspector.get_columns(self.table_name, schema=self.schema)]
                    for column_name, column_type in self.extra_columns.items():
                        if column_name not in existing_columns:
                            sql_type = sql_type_mappings.get(column_type.lower(), "VARCHAR(255)")  # Default to VARCHAR(255) if type is unknown
                            alter_stmt = f'ALTER TABLE {self.schema + "." if self.schema else ""}{self.table_name} ADD COLUMN {column_name} {sql_type}'
                            connection.execute(alter_stmt)
                            self.logger.info(f"Added column '{column_name}' to table '{self.table_name}' in schema '{self.schema}'.")
            except exc.SQLAlchemyError as e:
                self.logger.error(f"Failed to create or update table '{self.table_name}' in schema '{self.schema}': {e}")
                raise

        return table


    def insert_log(self, log_data):
        """
        Inserts a log entry into the database table.
        """
        if log_data:
            # Prepare the insert statement
            insert_stmt = self.table.insert().values(log_data)
            # Execute the insert and close the connection
            with self.engine.connect() as connection:
                try:
                    connection.execute(insert_stmt)
                    self.logger.info(f"Log entry successfully inserted into '{self.table_name}' in schema '{self.schema}'.")
                except exc.SQLAlchemyError as e:
                    self.logger.error(f"Failed to insert log entry into '{self.table_name}' in schema '{self.schema}': {e}")
                    raise
        
    def fetch_pending_messages(self):
        """
        Fetch messages with status IS NULL (unprocessed).
        """
        table_name = f'"{self.schema}"."{self.table_name}"' if self.schema else f'"{self.table_name}"'

        with self.engine.connect() as connection:
            result = connection.execute(
               f"SELECT * FROM {table_name} WHERE status IS NULL"
            ).fetchall()
        return result

    def update_status_bulk(self, updates: List[Dict[str, Any]]):
        """
        Bulk update the status of multiple rows. 
        Expects a list of dicts with keys: 'id' and 'status'.
        """
        if not updates:
            return
        with self.engine.connect() as connection:
            trans = connection.begin()
            try:
                table_name = f'"{self.schema}"."{self.table_name}"' if self.schema else f'"{self.table_name}"'
                update_stmt = text(
                    f"UPDATE {table_name} SET status=:status WHERE id=:id"
                )
                connection.execute(update_stmt, updates)
                trans.commit()
                self.logger.info(f"Batch updated {len(updates)} records in '{self.table_name}'.")
            except exc.SQLAlchemyError as e:
                trans.rollback()
                self.logger.error(f"Failed to batch update records in '{self.table_name}' in schema '{self.schema}': {e}")
                raise
        
    def upsert_log(self, log_data):
        """
        Performs an upsert (insert or update if material_no exists) on the log table.
        If a unique constraint on material_no does not exist, it will be created.

        Args:
            log_data (list of dict): List of log entries to insert or update.
        """
        # Ensure the unique constraint on material_no exists
        with self.engine.connect() as connection:
            inspector = inspect(connection)
            constraints = inspector.get_unique_constraints(self.table_name, schema=self.schema)
            unique_column_names = [constraint['column_names'] for constraint in constraints]

            # Check if material_no is part of any unique constraint
            if not any('material_no' in column_names for column_names in unique_column_names):
                # If no unique constraint exists on material_no, create one
                alter_stmt = f"ALTER TABLE {self.schema + '.' if self.schema else ''}{self.table_name} ADD CONSTRAINT unique_material_no UNIQUE (material_no)"
                connection.execute(alter_stmt)
                self.logger.info(f"Unique constraint on 'material_no' added to table '{self.table_name}'.")

        # Loop over each log entry in the list
        for entry in log_data:
            # Prepare the upsert statement for each entry
            upsert_stmt = insert(self.table).values(entry)

            # Define the conflict target (material_no column in this case) and update the fields on conflict
            upsert_stmt = upsert_stmt.on_conflict_do_update(
                index_elements=['material_no'],  # Conflict on the unique constraint material_no
                set_={key: entry[key] for key in entry if key != 'material_no'}  # Update other columns except 'material_no'
            )

            # Execute the upsert statement
            with self.engine.connect() as connection:
                try:
                    connection.execute(upsert_stmt)
                    self.logger.info(f"Log entry upserted into '{self.table_name}' in schema '{self.schema}'.")
                except exc.SQLAlchemyError as e:
                    self.logger.error(f"Failed to upsert log entry into '{self.table_name}' in schema '{self.schema}': {e}")
                    raise
