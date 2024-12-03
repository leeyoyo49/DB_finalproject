import pandas as pd
import duckdb
import psycopg2
from sqlalchemy import create_engine


# PostgreSQL connection setup
# DB_PASSWORD = '0418'  # Replace with your actual PostgreSQL password
DB_PASSWORD = ''  # Replace with your actual PostgreSQL password
DB_NAME = 'final proposal'     # Replace with your actual database name
DB_USER = 'postgres'           # PostgreSQL user
DB_HOST = 'localhost'          # Host address
TABLE_NAMES = [
    "achieve",
    "achievement",
    "alumni",
    "alumni_association",
    "association_event",
    "career_history",
    "degree_",
    "donation",
    "earned_by",
    "event_participated_by",
    "held_by",
    "is_cadre",
    "is_member",
    "user_"
]


def connect_to_db():
    """
    Establishes a connection to PostgreSQL using SQLAlchemy and DuckDB.

    Returns:
        duckdb.Connection: A DuckDB connection with registered tables.
    """
    # Create SQLAlchemy engine for PostgreSQL
    engine = create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )

    # DuckDB connection
    con = duckdb.connect()

    # Load PostgreSQL tables into DuckDB
    for table_name in TABLE_NAMES:
        query_str = f"SELECT * FROM {table_name}"
        # Use the SQLAlchemy engine instead of psycopg2 connection
        df = pd.read_sql_query(query_str, engine)
        con.register(table_name, df)  # Register the DataFrame in DuckDB

    # SQLAlchemy handles connection closing automatically, but you can explicitly dispose of it
    engine.dispose()

    return con

def query(con, sql_query, params=None):
    """
    Execute a SQL query on the database with optional parameters.

    Args:
        con (duckdb.Connection): The DuckDB connection.
        sql_query (str): SQL query string.
        params (tuple): Optional tuple containing query parameters.

    Returns:
        tuple: Column names and query results.
    """
    try:
        if params:
            cursor = con.execute(sql_query, params)
        else:
            cursor = con.execute(sql_query)
        result = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        return column_names, result
    except Exception as e:
        print(f"Error executing query: {str(e)}")
        return None, None
