import uuid
import pandas as pd
import pytest
from src import postgreasy
from psycopg2 import sql


@pytest.fixture
def database_connection_postgres_db():
    conn = postgreasy.get_connection()
    yield conn
    conn.close()


def test_connect():
    conn = postgreasy.get_connection()
    dsn_params = conn.get_dsn_parameters()

    assert dsn_params['dbname'] == 'production'
    assert dsn_params['user'] == 'report_reader'
    assert dsn_params['host'] == 'db-psql-vanhout-prd-01.postgres.database.azure.com'
    assert dsn_params['application_name'] == 'pytest_pyfunc_call()'


def test_connect_other_db():
    conn = postgreasy.get_connection(database='postgres')
    dsn_params = conn.get_dsn_parameters()

    assert dsn_params['dbname'] == 'postgres'


def test_execute():
    postgreasy.execute(sql.SQL('select 1'))


def test_fetch():
    x = postgreasy.fetch(sql.SQL('select 1'))
    assert x == [(1,)]


def test_create_table():
    schema_name = 'public'
    table_name = f'test_{str(uuid.uuid4())[:4]}'
    assert not postgreasy.check_if_table_exists(schema_name, table_name)

    postgreasy.create_table('public', table_name, sql.SQL('x int, y text'))
    assert postgreasy.check_if_table_exists(schema_name, table_name)

    postgreasy.execute(sql.SQL('drop table {schema}.{table}').format(schema=sql.Identifier(schema_name), table=sql.Identifier(table_name)))
    assert not postgreasy.check_if_table_exists(schema_name, table_name)


def test_insert():
    df = pd.DataFrame({'x': [1, 2, 3], 'y': [5, 28, 8]})
    test_table = f'test_insert_{str(uuid.uuid4())[:4]}'

    postgreasy.create_table('public', test_table, sql.SQL('x int, y int'))
    postgreasy.insert_df(df, 'public', test_table)
    records = postgreasy.fetch(sql.SQL('select x,y from {test_table}').format(test_table=sql.Identifier(test_table)))
    postgreasy.execute(sql.SQL('drop table {test_table}').format(test_table=sql.Identifier(test_table)))

    print(records)
    assert records == [(1, 5), (2, 28), (3, 8)]


def test_insert_swap_columns():
    df = pd.DataFrame({'x': [1, 2, 3], 'y': [5, 28, 8]})
    test_table = f'test_insert_{str(uuid.uuid4())[:4]}'

    postgreasy.create_table('public', test_table, sql.SQL('y int, x int'))
    postgreasy.insert_df(df, 'public', test_table)
    records = postgreasy.fetch(sql.SQL('select x,y from {test_table}').format(test_table=sql.Identifier(test_table)))
    postgreasy.execute(sql.SQL('drop table {test_table}').format(test_table=sql.Identifier(test_table)))

    print(records)
    assert records == [(1, 5), (2, 28), (3, 8)]


def test_create_schema():
    name = f'test_{str(uuid.uuid4())[:4]}'
    postgreasy.create_schema(name)
    exist_query = sql.SQL('select exists(SELECT * from information_schema.schemata WHERE schema_name = {schema})').format(schema=sql.Literal(name))
    result = postgreasy.fetch(exist_query)

    delete_query = sql.SQL('drop schema {schema}').format(schema=sql.Identifier(name))
    postgreasy.execute(delete_query)

    assert result == [(True,)]


# def test_create_db(database_connection_postgres_db):
#     name = f'test_{str(uuid.uuid4())[:4]}'
#     postgreasy.create_database(name, database_connection_postgres_db)
#     exists_query = sql.SQL('select exists(SELECT datname FROM pg_catalog.pg_database WHERE lower(datname) = lower({database}))').format(database=sql.Literal(name))
#     result = postgreasy.fetch_with_query_on_db(exists_query, database_connection_postgres_db)

#     delete_query = sql.SQL('drop database {database}').format(database=sql.Identifier(name))
#     postgreasy.execute_query_on_db(delete_query)

#     assert result == [(True,)]
