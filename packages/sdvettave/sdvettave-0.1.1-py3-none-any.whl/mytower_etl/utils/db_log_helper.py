import logging
from typing import Dict, List, Any
from sqlalchemy import create_engine, Table, Column, MetaData, String, Integer, exc, inspect, Text, Date
from sqlalchemy.exc import NoSuchModuleError
from sqlalchemy.sql import text
from sqlalchemy.dialects.postgresql import insert


class DBLogHelper:
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        database: str,
        table_name: str,
        schema: str = None,
        extra_columns: Dict[str, str] = None,
    ):
        """
        Initializes the DBLogHelper.

        Args:
            host (str): Database host.
            port (int): Database port.
            username (str): Database username.
            password (str): Database password.
            database (str): Database name.
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

        # Create the connection URI
        connection_uri = f'postgresql://{username}:{password}@{host}:{port}/{database}'

        # Ensure SQLAlchemy can understand the URI
        try:
            execution_options = {}
            if schema:
                execution_options = {"schema_translate_map": {None: schema}}
            self.engine = create_engine(connection_uri, execution_options=execution_options)
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

    def insert_log(self, log_data: Dict[str, Any]):
        """
        Inserts a log entry into the table.

        Args:
            log_data (dict): A dictionary of log data to insert into the table.
        """
        try:
            with self.engine.connect() as connection:
                # Insert the log entry using SQLAlchemy
                insert_stmt = insert(self.table).values(log_data)
                connection.execute(insert_stmt)
                self.logger.info(f"Log entry inserted: {log_data}")
        except exc.SQLAlchemyError as e:
            self.logger.error(f"Failed to insert log entry {log_data}: {e}")
            raise

    def fetch_pending_messages(self, limit: int = 100):
        """
        Fetches pending messages from the table.

        Args:
            limit (int): The maximum number of messages to fetch.

        Returns:
            List[Dict]: A list of log entries.
        """
        try:
            with self.engine.connect() as connection:
                # Fetch pending log entries from the table
                select_stmt = text(f"SELECT * FROM {self.schema + '.' if self.schema else ''}{self.table_name} WHERE status = 'pending' LIMIT :limit")
                result = connection.execute(select_stmt, {'limit': limit})
                return [dict(row) for row in result]
        except exc.SQLAlchemyError as e:
            self.logger.error(f"Failed to fetch pending messages: {e}")
            raise

    def update_status_bulk(self, log_keys: List[str], status: str):
        """
        Updates the status of multiple log entries in bulk.

        Args:
            log_keys (List[str]): A list of log keys to update.
            status (str): The new status to set.
        """
        try:
            with self.engine.connect() as connection:
                # Update the status of the log entries
                update_stmt = text(f"UPDATE {self.schema + '.' if self.schema else ''}{self.table_name} SET status = :status WHERE log_key IN :log_keys")
                connection.execute(update_stmt, {'status': status, 'log_keys': tuple(log_keys)})
                self.logger.info(f"Bulk updated status to '{status}' for log keys: {log_keys}")
        except exc.SQLAlchemyError as e:
            self.logger.error(f"Failed to update status for log keys {log_keys}: {e}")
            raise

    def upsert_log(self, log_data: Dict[str, Any]):
        """
        Performs an upsert (insert or update) operation on the log table.

        Args:
            log_data (dict): A dictionary of log data to upsert.
        """
        try:
            with self.engine.connect() as connection:
                # Perform an upsert operation
                insert_stmt = insert(self.table).values(log_data)
                conflict_stmt = insert_stmt.on_conflict_do_update(
                    index_elements=['log_key'],
                    set_=log_data
                )
                connection.execute(conflict_stmt)
                self.logger.info(f"Upserted log entry: {log_data}")
        except exc.SQLAlchemyError as e:
            self.logger.error(f"Failed to upsert log entry {log_data}: {e}")
            raise
