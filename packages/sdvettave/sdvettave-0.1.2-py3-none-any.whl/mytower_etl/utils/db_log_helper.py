from sqlalchemy import create_engine, MetaData, Table, Column, String, Text, exc, text
from sqlalchemy.dialects.postgresql import insert
import logging


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
        extra_columns: dict = None,
    ):
        """
        Initializes the DBLogHelper instance, setting up the database connection and
        ensuring the table exists with the specified schema and additional columns.

        :param host: Database host.
        :param port: Database port.
        :param username: Database username.
        :param password: Database password.
        :param database: Database name.
        :param table_name: Name of the log table.
        :param schema: Schema name (optional).
        :param extra_columns: Dictionary of extra columns to add to the log table.
        """
        self.logger = logging.getLogger("DBLogHelper")
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.table_name = table_name
        self.schema = schema
        self.extra_columns = extra_columns or {}

        # Set up the database connection
        db_url = f"postgresql://{username}:{password}@{host}:{port}/{database}"
        self.engine = create_engine(db_url, echo=False, future=True)
        self.logger.info(f"Successfully created database engine for URI '{db_url}'.")

        # Ensure the schema exists
        if self.schema:
            self._ensure_schema_exists()

        # Create or update the table
        self.metadata = MetaData(schema=self.schema)
        self.log_table = self._create_or_update_table()

    def _ensure_schema_exists(self):
        """
        Ensures that the schema exists in the database.
        """
        try:
            schema_create_stmt = f"CREATE SCHEMA IF NOT EXISTS {self.schema}"
            with self.engine.connect() as connection:
                connection.execute(text(schema_create_stmt))
            self.logger.info(f"Schema '{self.schema}' ensured to exist.")
        except exc.SQLAlchemyError as e:
            self.logger.error(f"Failed to ensure schema '{self.schema}' exists: {e}")
            raise

    def _create_or_update_table(self):
        """
        Creates or updates the log table with the specified columns.
        """
        try:
            columns = [
                Column("id", String, primary_key=True),
                Column("timestamp", String),
            ]

            for column_name, column_type in self.extra_columns.items():
                if column_type == "string":
                    columns.append(Column(column_name, String))
                elif column_type == "text":
                    columns.append(Column(column_name, Text))

            log_table = Table(
                self.table_name, self.metadata, *columns, extend_existing=True
            )

            # Create table if it does not exist
            self.metadata.create_all(self.engine)
            self.logger.info(f"Table '{self.table_name}' ensured to exist.")
            return log_table
        except exc.SQLAlchemyError as e:
            self.logger.error(f"Failed to create or update table '{self.table_name}': {e}")
            raise

    def insert_log(self, log_data: dict):
        """
        Inserts a log entry into the database.

        :param log_data: Dictionary of log data to insert.
        """
        try:
            insert_stmt = insert(self.log_table).values(log_data)
            with self.engine.connect() as connection:
                connection.execute(insert_stmt)
                connection.commit()
            self.logger.info(f"Log data inserted: {log_data}")
        except exc.SQLAlchemyError as e:
            self.logger.error(f"Failed to insert log data: {e}")
            raise
