# Postgreasy

This package contains some simple helper functions to interact with a postgress database. Makes use of a `.env` file to make the connection with the database. It's basically a simple wrapper around the `psycopg2` library.

Fill in the following 4 parameters in the `.env` file in the root folder like so:

```lua
postgres_host = ...
postgres_username = ...
postgres_database = ...
postgres_password = ...
```

## Methods

### Create a database

```py
import postgreasy

postgreasy.create_database(database_name='example_db')
```

### Create a schema

```py
import postgreasy

postgreasy.create_schema(database_name='example_db')
```

### Create a table

```py
import postgreasy
from psycopg2 import sql

postgreasy.create_table('example_schema', 'example_table', sql.SQL('id serial, temperature int, name text'))
```

### Execute a query

```py
import postgreasy
from psycopg2 import sql

postgreasy.execute(sql.SQL('...'))
```

### Fetch with a query (Execute a query and get the results)

```py
import postgreasy
from psycopg2 import sql

x = postgreasy.execute(sql.SQL('select 1'))
```

### Insert a Pandas DataFrame

```py
import postgreasy
import pandas as pd

df = pd.DataFrame({'x': [1, 2, 3], 'y': [5, 28, 8]})
postgreasy.insert_df(df, 'example_schema', 'example_table')
```

## Connection

Normally when you execute one of the postgreasy methods, a connection is automatically established and closed. For example:

```py
import postgreasy
from psycopg2 import sql

postgreasy.execute_query_on_db(sql.SQL('select 1'))
```

To create a connection without the .env or if you want to execute multiple queries and not create a connection for each separate query there are 2 ways to go about it. Either use the `get_connection()` method or use the `with ...` structure with a `PostgresConnection()` object. The latter is the preferred option as it requires less steps that can be forgotten.

### `get_connection()`

This way you create a connection object which you supply to the other postgreasy methods. Here you have to remember to manually close the connection with the `.close()` function.

**Example:**

```py
import postgreasy
from psycopg2 import sql

conn = postgreasy.get_connection(host='...', database='...', username='...', password='...')
postgreasy.execute_query_on_db(sql.SQL('select 1'), conn )
conn.close()

```

### `PostgresConnection()`

In this case the connection is automatically opened, you also don't have to supply the connection paramter to the postgreasy methods.

**Example:**

```py
import postgreasy
from psycopg2 import sql

with PostgresConnection(host='...', database='...', username='...', password='...') as conn:
    conn.execute_query_on_db(sql.SQL('select 1') )
```

## Contact

Go to the GitHub page if you hav any issues.