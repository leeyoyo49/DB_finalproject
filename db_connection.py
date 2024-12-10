import psycopg2
import logging
import os

# PostgreSQL connection setup
#DB_PASSWORD = os.getenv('DB_PASSWORD', 'b11705059')
DB_PASSWORD = ''  # Replace with your actual PostgreSQL password
DB_NAME = 'final proposal'  # Replace with your actual database name
DB_USER = 'postgres'  # PostgreSQL user
DB_HOST = 'localhost'  # Host address
# DB_PORT = os.getenv('DB_PORT', '5433')
DB_PORT = '5432'


def execute_update(sql_query, params=None):
    """
    Executes an UPDATE SQL query on the database.

    Args:
        sql_query (str): SQL query string with placeholders.
        params (tuple): Parameters for the query.

    Returns:
        int: The number of rows affected.
    """
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,  # Explicitly specify port
        )
        cursor = connection.cursor()

        # Execute the query with parameters
        cursor.execute(sql_query, params)

        # Commit the changes
        connection.commit()

        # Return the number of rows affected
        return cursor.rowcount

    except Exception as e:
        logging.error("Error executing update query", exc_info=True)
        return None

    finally:
        # Ensure the connection is closed
        if connection:
            cursor.close()
            connection.close()


def query(sql_query, params=None):
    """
    Execute a SQL query on the database.

    Args:
        sql_query (str): SQL query string.
        params (tuple): Parameters to substitute in the SQL query.

    Returns:
        tuple or int: For SELECT queries, returns column names and results.
                      For non-SELECT queries, returns the number of affected rows.
    """
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,  # Explicitly specify port
        )
        cursor = connection.cursor()

        # Execute the SQL query with parameters
        cursor.execute(sql_query, params)

        # Fetch results if the query is a SELECT statement
        if cursor.description:  # Indicates a query returning rows
            column_names = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return column_names, rows
        else:
            # For non-SELECT queries, commit the changes and return row count
            connection.commit()
            return cursor.rowcount

    except Exception as e:
        logging.error("Error executing query", exc_info=True)
        return None

    finally:
        # Ensure the connection is closed
        if connection:
            cursor.close()
            connection.close()
