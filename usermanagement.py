import hashlib
from db_connection import con, query

# User Management Functions

def create_user(username, password, role):
    """
    Creates a new user in the database.

    Args:
        username (str): Username for the new user.
        password (str): Password for the new user.
        role (str): Role of the user (e.g., 'Admin', 'User', 'Analyst').

    Returns:
        str: Success or error message.
    """
    try:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        sql_query = """
            INSERT INTO users (username, password, role)
            VALUES (%s, %s, %s)
        """
        query(con, sql_query, (username, hashed_password, role))
        return "User created successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def delete_user(user_id):
    """
    Deletes a user from the database.

    Args:
        user_id (int): ID of the user to delete.

    Returns:
        str: Success or error message.
    """
    try:
        sql_query = "DELETE FROM users WHERE id = %s"
        query(con, sql_query, (user_id,))
        return "User deleted successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def update_user(user_id, data):
    """
    Updates a user's details.

    Args:
        user_id (int): ID of the user to update.
        data (dict): Dictionary containing fields to update.

    Returns:
        str: Success or error message.
    """
    try:
        updates = ", ".join(f"{key} = %s" for key in data.keys())
        sql_query = f"UPDATE users SET {updates} WHERE id = %s"
        query(con, sql_query, (*data.values(), user_id))
        return "User updated successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def get_user_details(user_id):
    """
    Retrieves user details from the database.

    Args:
        user_id (int): ID of the user.

    Returns:
        dict: User details or error message.
    """
    try:
        sql_query = "SELECT id, username, role FROM users WHERE id = %s"
        columns, results = query(con, sql_query, (user_id,))
        if not results:
            return {"status": "error", "message": "User not found"}
        
        user_details = dict(zip(columns, results[0]))
        return {"status": "success", "user_details": user_details}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# User Role Assignment Functions

def assign_role(user_id, role):
    """
    Assigns a role to a user.

    Args:
        user_id (int): ID of the user.
        role (str): Role to assign.

    Returns:
        str: Success or error message.
    """
    try:
        sql_query = "UPDATE users SET role = %s WHERE id = %s"
        query(con, sql_query, (role, user_id))
        return "Role assigned successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def change_role(user_id, new_role):
    """
    Changes a user's role.

    Args:
        user_id (int): ID of the user.
        new_role (str): New role to assign.

    Returns:
        str: Success or error message.
    """
    return assign_role(user_id, new_role)
