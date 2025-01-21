import uuid
import pandas as pd
import pytest
from psycopg2 import sql

from src.postgreasy import PostgresConnection


def test_connect():
    with PostgresConnection() as conn:
        x = conn.fetch(sql.SQL('select 1'))
        print(x)
        assert x == [(1,)]


def test_connect_ssl():
    with PostgresConnection(ssl_required=True) as conn:
        x = conn.fetch(sql.SQL('select 1'))
        print(x)
        assert x == [(1,)]


def test_disconnect():
    with PostgresConnection() as conn:
        x = conn.fetch(sql.SQL('select 1'))
        assert x == [(1,)]

    with pytest.raises(RuntimeError):
        conn.fetch(sql.SQL('select 1'))


def test_create_table():
    with PostgresConnection(database='ovviadatatransaction_test') as conn:
        schema_name = 'public'
        table_name = f'test_{str(uuid.uuid4())[:4]}'
        assert not conn.check_if_table_exists(schema_name, table_name)

        conn.create_table('public', table_name, sql.SQL('x int, y text'))
        assert conn.check_if_table_exists(schema_name, table_name)

        conn.execute(sql.SQL('drop table {schema}.{table}').format(schema=sql.Identifier(schema_name), table=sql.Identifier(table_name)))
        assert not conn.check_if_table_exists(schema_name, table_name)


def test_insert():
    df = pd.DataFrame({'x': [1, 2, 3], 'y': [5, 28, 8]})
    test_table = f'test_insert_{str(uuid.uuid4())[:4]}'
    with PostgresConnection(database='ovviadatatransaction_test') as conn:
        conn.create_table('public', test_table, sql.SQL('x int, y int'))
        conn.insert_df(df, 'public', test_table)
        records = conn.fetch(sql.SQL('select x,y from {test_table}').format(test_table=sql.Identifier(test_table)))
        conn.execute(sql.SQL('drop table {test_table}').format(test_table=sql.Identifier(test_table)))
        print(records)
        assert records == [(1, 5), (2, 28), (3, 8)]


def test_insert_swap_columns():
    df = pd.DataFrame({'x': [1, 2, 3], 'y': [5, 28, 8]})
    test_table = f'test_insert_{str(uuid.uuid4())[:4]}'
    with PostgresConnection(database='ovviadatatransaction_test') as conn:
        conn.create_table('public', test_table, sql.SQL('y int, x int'))
        conn.insert_df(df, 'public', test_table)
        records = conn.fetch(sql.SQL('select x,y from {test_table}').format(test_table=sql.Identifier(test_table)))
        conn.execute(sql.SQL('drop table {test_table}').format(test_table=sql.Identifier(test_table)))
        print(records)
        assert records == [(1, 5), (2, 28), (3, 8)]


def test_create_schema():
    with PostgresConnection() as conn:
        name = f'test_{str(uuid.uuid4())[:4]}'
        conn.create_schema(name)
        exist_query = sql.SQL('select exists(SELECT * from information_schema.schemata WHERE schema_name = {schema})').format(schema=sql.Literal(name))
        result = conn.fetch(exist_query)

        delete_query = sql.SQL('drop schema {schema}').format(schema=sql.Identifier(name))
        conn.execute(delete_query)

        assert result == [(True,)]
