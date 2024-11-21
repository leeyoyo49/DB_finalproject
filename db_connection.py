import pandas as pd
import duckdb
import psycopg2

# PostgreSQL connection setup
DB_PASSWORD = ''  # Replace with your actual PostgreSQL password
DB_NAME = 'your_database'      # Replace with your actual database name
DB_USER = 'postgres'           # PostgreSQL user
DB_HOST = 'localhost'          # Host address
TABLE_NAMES = ['users']        # List of table names to load

# Connect to PostgreSQL and DuckDB
def connect_to_db():
    """
    Establishes a connection to PostgreSQL and DuckDB.

    Returns:
        duckdb.Connection: A DuckDB connection with registered tables.
    """
    # Connect to PostgreSQL
    psql_conn = psycopg2.connect(
        f"dbname='{DB_NAME}' user='{DB_USER}' host='{DB_HOST}' password='{DB_PASSWORD}'"
    )

    # DuckDB connection
    con = duckdb.connect()

    # Load PostgreSQL tables into DuckDB
    for table_name in TABLE_NAMES:
        query_str = f"SELECT * FROM {table_name}"
        df = pd.read_sql_query(query_str, psql_conn)  # Load data into DataFrame
        con.register(table_name, df)  # Register the DataFrame in DuckDB

    # Close PostgreSQL connection
    psql_conn.close()

    return con

# Function to execute SQL queries via DuckDB
def query(con, sql_query):
    """
    Execute a SQL query on the registered tables.

    Args:
        con (duckdb.Connection): The DuckDB connection.
        sql_query (str): SQL query string.

    Returns:
        tuple: Column names and query results.
    """
    result = con.execute(sql_query).fetchall()
    column_names = [desc[0] for desc in con.description]
    return column_names, result
