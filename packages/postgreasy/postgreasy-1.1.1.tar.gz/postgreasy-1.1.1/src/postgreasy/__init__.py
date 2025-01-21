import inspect
import os
from typing import Any, Optional

import dotenv
import numpy as np
import pandas as pd
import psycopg2
from psycopg2 import sql

from .postgres_connection import PostgresConnection  # noqa F402


def get_connection(
    host: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    database: Optional[str] = None,
):
    if os.path.isfile('.env'):
        dotenv.load_dotenv('.env')

    host = os.environ['postgres_host'] if host is None else host
    username = os.environ['postgres_username'] if username is None else username
    password = os.environ['postgres_password'] if password is None else password
    database = os.environ['postgres_database'] if database is None else database

    if host is None or database is None or username is None or password is None:
        raise RuntimeError('No env. variable set or .env file given while one of the parameters is missing.')

    try:
        calling_function = inspect.stack()[2][3]
    except Exception:
        calling_function = ''

    connection = psycopg2.connect(
        host=host,
        dbname=database,
        user=username,
        password=password,
        application_name=f'{calling_function}()',
    )

    connection.autocommit = True
    return connection


def create_database(database_name: str, connection: Optional[Any] = None):
    """
    Create the given database
    """
    query = sql.SQL('create database {database_name};').format(database_name=sql.Identifier(database_name))
    execute(query, connection)


def create_schema(schema_name: str, connection: Optional[Any] = None):
    """
    Create the given schema,
    """
    schema_query = sql.SQL('create schema if not exists {schema_name};').format(schema_name=sql.Identifier(schema_name))
    execute(schema_query, connection)


def create_table(schema_name: str, table_name: str, table_columns: sql.SQL, connection: Optional[Any] = None):
    create_table_query = sql.SQL('create table if not exists {schema_name}.{table_name} ({table_columns})').format(
        schema_name=sql.Identifier(schema_name),
        table_name=sql.Identifier(table_name),
        table_columns=table_columns,
    )
    execute(create_table_query, connection)


def check_if_table_exists(schema_name: str, table_name: str, connection: Optional[Any] = None) -> bool:
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
    exists = fetch(exists_query, connection)[0][0]
    return exists


def _execute_or_fetch(query: sql.Composable, fetch: bool = False, connection: Optional[Any] = None) -> Optional[list]:
    # TODO maakt nu iedere keer een nieuwe connectie niet heel nice
    if connection is None:
        must_close = True
        connection = get_connection()
    else:
        must_close = False

    connection.autocommit = True
    # print("Created connection")
    cursor = connection.cursor()

    # print(f"Executing query: ({query.as_string(connection)})")
    cursor.execute(query)
    # print(f"Succesfully executed query: ({cursor.query.decode()})")

    if fetch:
        records = cursor.fetchall()
        # print('Fetched records')
    else:
        records = None

    cursor.close()
    if must_close:
        connection.close()

        if connection.closed:
            # print("Closed connection")
            pass
        else:
            print('Connection not closed yet...')
    else:
        pass
        # print("Warning, not closing connection!")

    return records


def fetch(query: sql.Composable, connection: Optional[Any] = None) -> list:
    return _execute_or_fetch(query, fetch=True, connection=connection)  # type:ignore


def execute(query: sql.Composable, connection: Optional[Any] = None) -> list:
    return _execute_or_fetch(query, fetch=False, connection=connection)  # type:ignore


# def get_most_recent_time_value(time_column: str, schema: str, table: str) -> dt.datetime:
#     """
#     Returns the most recent timestamp from the time column from the table, of the table does not exist,
#     it returns 1st January 2023
#     """
#     database_newest_date = dt.datetime(0, 0, 0, tzinfo=dt.timezone.utc)
#     if check_if_table_exists(schema, table):
#         newest_entry_date_query = sql.SQL('select {time_column_name} from {schema}.{table} order by {time_column_name} desc limit 1').format(
#             schema=sql.Identifier(schema),
#             table=sql.Identifier(table),
#             time_column_name=sql.Identifier(time_column),
#         )
#         result = fetch_with_query_on_db(newest_entry_date_query)
#         if len(result) > 0:
#             database_newest_date = result[0][0]

#     return database_newest_date


def insert_df(df: pd.DataFrame, schema: str, table: str, connection: Optional[Any] = None) -> None:
    """
    Does not upload the index, so make sure to reset_index() if you need it as well
    """

    n_columns = df.shape[1]

    insert_string_part = ','.join(['%s'] * n_columns)
    columns_string = ','.join([f'"{x}"' for x in list(df.columns)])

    insert_query = f'INSERT INTO {schema}.{table} ({columns_string}) VALUES ({insert_string_part}) ON CONFLICT do nothing'

    values = df.replace({np.nan: None}).values.tolist()

    must_close = False
    if connection is None:
        must_close = True
        connection = get_connection()

    cursor = connection.cursor()
    cursor.executemany(insert_query, values)
    connection.commit()

    if must_close:
        connection.close()
