import inspect
import os
from typing import Any, Optional

import dotenv
import numpy as np
import pandas as pd
import psycopg2
from psycopg2 import sql


class PostgresConnection:
    def __init__(
        self,
        host: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
        ssl_required: bool = False,
    ):
        if os.path.isfile('.env'):
            dotenv.load_dotenv()

        self.host = os.environ['postgres_host'] if host is None else host
        self.username = os.environ['postgres_username'] if username is None else username
        self.password = os.environ['postgres_password'] if password is None else password
        self.database = os.environ['postgres_database'] if database is None else database
        self.ssl_mode = 'require' if ssl_required else 'disable'

        if self.host is None or self.database is None or self.username is None or self.password is None:
            raise RuntimeError('No env. variable set or .env file given while one of the parameters is missing.')

        self.connection: Optional[Any] = None

    def __enter__(self):
        try:
            calling_function = inspect.stack()[2][3]
        except Exception:
            calling_function = ''

        self.connection = psycopg2.connect(
            host=self.host,
            dbname=self.database,
            user=self.username,
            password=self.password,
            application_name=f'{calling_function}()',
            sslmode=self.ssl_mode,
        )

        self.connection.autocommit = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection is not None:
            self.connection.close()
        else:
            raise Exception('Tried to close connection when it was not created yet!')

    def _check_connection_exists(self):
        if self.connection is None or self.connection.closed:
            raise RuntimeError('Connection not made yet.')

    def _execute_or_fetch(self, query: sql.Composable, fetch: bool = False) -> Optional[list]:
        self._check_connection_exists()
        cursor = self.connection.cursor()  # type:ignore

        # print(f"Executing query: ({query.as_string(connection)})")
        cursor.execute(query)
        # print(f"Succesfully executed query: ({cursor.query.decode()})")

        if fetch:
            records = cursor.fetchall()
            # print('Fetched records')
        else:
            records = None

        cursor.close()

        return records

    def fetch(self, query: sql.Composable) -> list:
        return self._execute_or_fetch(query, fetch=True)  # type:ignore

    def execute(self, query: sql.Composable) -> list:
        return self._execute_or_fetch(query, fetch=False)  # type:ignore

    def check_if_table_exists(self, schema_name: str, table_name: str) -> bool:
        exists_query = sql.SQL(
            """select exists (
                        select from information_schema.tables
                        where  table_schema = {schema_name}
                        and    table_name   = {table_name}
            )"""
        ).format(
            schema_name=sql.Literal(schema_name),
            table_name=sql.Literal(table_name),
        )
        exists = self.fetch(exists_query)[0][0]
        return exists

    def create_table(self, schema_name: str, table_name: str, table_columns: sql.SQL, connection: Optional[Any] = None):
        create_table_query = sql.SQL('create table if not exists {schema_name}.{table_name} ({table_columns})').format(
            schema_name=sql.Identifier(schema_name),
            table_name=sql.Identifier(table_name),
            table_columns=table_columns,
        )
        self.execute(create_table_query)

    def create_schema(self, schema_name: str):
        """
        Create the given schema
        """
        schema_query = sql.SQL('create schema if not exists {schema_name};').format(schema_name=sql.Identifier(schema_name))
        self.execute(schema_query)

    def create_database(self, database_name: str):
        """
        Create the given database
        """
        query = sql.SQL('create database {database_name};').format(database_name=sql.Identifier(database_name))
        self.execute(query)

    def insert_df(self, df: pd.DataFrame, schema: str, table: str) -> None:
        """
        Does not upload the index, so make sure to reset_index() if you need it as well
        """
        self._check_connection_exists()
        cursor = self.connection.cursor()  # type:ignore

        n_columns = df.shape[1]
        insert_string_part = ','.join(['%s'] * n_columns)
        columns_string = ','.join([f'"{x}"' for x in list(df.columns)])
        insert_query = f'INSERT INTO {schema}.{table} ({columns_string}) VALUES ({insert_string_part}) ON CONFLICT do nothing'

        values = df.replace({np.nan: None}).values.tolist()

        cursor.executemany(insert_query, values)
        self.connection.commit()  # type:ignore
