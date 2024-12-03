import hashlib
from db_connection import con, query
from flask import Flask, jsonify, request, session

# Utility Functions

def login_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    sql_query = "SELECT id, username, password, role FROM users WHERE username = %s"
    columns, results = query(con, sql_query, (username,))
    if not results:
        return None
    user = results[0]
    user_id, db_username, db_password, role = user
    if db_password == hashed_password:
        return {"user_id": user_id, "username": db_username, "role": role}
    return None

def check_permissions(required_role):
    if 'user_id' not in session:
        return False, "Unauthorized"
    user_role = session.get('role')
    if required_role == "User":
        return True, ""  # Allow all roles for this endpoint
    if user_role != required_role:
        return False, "Permission denied"
    return True, ""


# Alumni management functions
# Alumni CRUD Functions
def add_alumni(data):
    """
    Adds a new alumni record.

    Args:
        data (dict): Alumni data to insert.

    Returns:
        str: Success or error message.
    """
    try:
        sql_query = """
            INSERT INTO alumni (first_name, last_name, address, phone, graduation_year, user_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        query(con, sql_query, (
            data['first_name'], data['last_name'], data['address'],
            data['phone'], data['graduation_year'], data['user_id']
        ))
        return "Alumni added successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def get_alumni(alumni_id):
    """
    Retrieves alumni details.

    Args:
        alumni_id (int): Alumni ID.

    Returns:
        dict: Alumni details or error message.
    """
    try:
        sql_query = "SELECT * FROM alumni WHERE alumni_id = %s"
        columns, results = query(con, sql_query, (alumni_id,))
        if not results:
            return {"status": "error", "message": "Alumni not found"}

        alumni_details = dict(zip(columns, results[0]))
        return {"status": "success", "alumni_details": alumni_details}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def update_alumni(alumni_id, data):
    """
    Updates an alumni record.

    Args:
        alumni_id (int): Alumni ID.
        data (dict): Alumni data to update.

    Returns:
        str: Success or error message.
    """
    try:
        updates = ", ".join(f"{key} = %s" for key in data.keys())
        sql_query = f"UPDATE alumni SET {updates} WHERE alumni_id = %s"
        query(con, sql_query, (*data.values(), alumni_id))
        return "Alumni updated successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def delete_alumni(alumni_id):
    """
    Deletes an alumni record.

    Args:
        alumni_id (int): Alumni ID.

    Returns:
        str: Success or error message.
    """
    try:
        sql_query = "DELETE FROM alumni WHERE alumni_id = %s"
        query(con, sql_query, (alumni_id,))
        return "Alumni deleted successfully."
    except Exception as e:
        return f"Error: {str(e)}"

# Data Queries Functions
def find_alumni_by_name(name):
    """
    Finds alumni by name.

    Args:
        name (str): Name to search for.

    Returns:
        dict: Alumni list or error message.
    """
    try:
        sql_query = "SELECT * FROM alumni WHERE first_name LIKE %s OR last_name LIKE %s"
        columns, results = query(con, sql_query, (f"%{name}%", f"%{name}%"))
        alumni_list = [dict(zip(columns, row)) for row in results]
        return {"status": "success", "alumni_list": alumni_list}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_alumni_by_graduation_year(year):
    """
    Gets alumni by graduation year.

    Args:
        year (int): Graduation year.

    Returns:
        dict: Alumni list or error message.
    """
    try:
        sql_query = "SELECT * FROM alumni WHERE graduation_year = %s"
        columns, results = query(con, sql_query, (year,))
        alumni_list = [dict(zip(columns, row)) for row in results]
        return {"status": "success", "alumni_list": alumni_list}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def list_alumni():
    """
    Lists all alumni.

    Returns:
        dict: List of alumni or error message.
    """
    try:
        sql_query = "SELECT * FROM alumni"
        columns, results = query(con, sql_query)
        alumni_list = [dict(zip(columns, row)) for row in results]
        return {"status": "success", "alumni_list": alumni_list}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Alumni-Specific Functions
def update_alumni_career_history(alumni_id, career_data):
    """
    Updates an alumni's career history.

    Args:
        alumni_id (int): Alumni ID.
        career_data (dict): Career history details.

    Returns:
        str: Success or error message.
    """
    try:
        sql_query = """
            INSERT INTO career_history (job_title, company, start_date, end_date, monthly_salary, alumni_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        query(con, sql_query, (
            career_data['job_title'], career_data['company'], career_data['start_date'],
            career_data.get('end_date'), career_data.get('monthly_salary'), alumni_id
        ))
        return "Career history updated successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def get_alumni_donations(alumni_id):
    """
    Retrieves alumni donations.

    Args:
        alumni_id (int): Alumni ID.

    Returns:
        dict: Donations list or error message.
    """
    try:
        sql_query = "SELECT * FROM donation WHERE alumni_id = %s"
        columns, results = query(con, sql_query, (alumni_id,))
        donations = [dict(zip(columns, row)) for row in results]
        return {"status": "success", "donations": donations}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_alumni_achievements(alumni_id):
    """
    Retrieves alumni achievements.

    Args:
        alumni_id (int): Alumni ID.

    Returns:
        dict: Achievements list or error message.
    """
    try:
        sql_query = "SELECT * FROM achievement WHERE alumni_id = %s"
        columns, results = query(con, sql_query, (alumni_id,))
        achievements = [dict(zip(columns, row)) for row in results]
        return {"status": "success", "achievements": achievements}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
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
