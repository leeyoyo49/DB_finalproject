import hashlib
from db_connection import query, execute_update
from flask import Flask, jsonify, request, session
import logging


def login_user(username, password):
    """
    Authenticates a user by verifying the provided credentials.

    Args:
        username (str): The username of the user attempting to log in.
        password (str): The plaintext password of the user.

    Returns:
        dict or None: A dictionary containing the user's details ('user_id', 'username', 'role') if authentication is successful, otherwise None.
    """
    try:
        # SQL query with parameterized placeholders
        sql_query = "SELECT user_id, user_name, password, role FROM user_ WHERE user_name = %s"

        # Execute the query with parameters
        result = query(sql_query, (username,))

        if not result or not result[1]:
            return None  # Return None if no user is found

        # Extract user details from the query result
        _, rows = result
        user_id, db_username, db_password, role = rows[0]

        # Verify the provided password matches the stored password
        if db_password == password:
            return {"user_id": user_id, "username": db_username, "role": role}

        return None  # Return None if authentication fails

    except Exception as e:
        logging.error("Error during user login", exc_info=True)
        return None




def add_alumni(data):
    """
    Adds a new alumni record.

    Args:
        data (dict): Alumni data to insert.
            - first_name (str): The first name of the alumni. (Required)
            - last_name (str): The last name of the alumni. (Required)
            - sex (str): The gender of the alumni (e.g., 'M', 'F'). (Required)
            - address (str): The address of the alumni. (Required)
            - graduation_year (int): The year the alumni graduated. (Required)
            - user_id (int): The user ID associated with the alumni. (Required)
            - phone (str): The contact phone number of the alumni. (Required)

    Returns:
        str: Success or error message.
    """
    try:
        # SQL query to insert a new alumni record
        sql_query = """
            INSERT INTO alumni (alumni_id, first_name, last_name, sex, address, graduation_year, user_id, phone)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        # Extract the required fields from the data dictionary
        params = (
            data.get('alumni_id'),
            data.get('first_name'),
            data.get('last_name'),
            data.get('sex'),
            data.get('address'),
            data.get('graduation_year'),
            data.get('user_id'),
            data.get('phone')
        )

        # Validate that all required fields are provided
        if not all(params):
            return "Error: Missing required fields."

        # Execute the query
        rows_affected = execute_update(sql_query, params)
        return "Alumni added successfully." if rows_affected else "Failed to add alumni."

    except Exception as e:
        logging.error("Error adding alumni", exc_info=True)
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
        # SQL query to fetch alumni details
        sql_query = "SELECT * FROM alumni WHERE alumni_id = %s"
        # Execute the query with the provided alumni ID
        columns, results = query(sql_query, (alumni_id,))
        
        # If no results are returned, alumni ID does not exist
        if not results:
            return {"status": "error", "message": "Alumni not found"}
        
        # Map the result to column names to create a dictionary
        alumni_details = dict(zip(columns, results[0]))
        
        # Return success response with alumni details
        return {"status": "success", "alumni_details": alumni_details}
    
    except Exception as e:
        # Return error response with exception message
        # Consider logging the error instead of returning full details in production
        return {"status": "error", "message": "An error occurred while retrieving alumni details."}

def update_alumni(alumni_id, data):
    """
    Constructs the SQL query to update alumni and executes it.

    Args:
        - first_name (str): The first name of the alumni. (Required)
        - last_name (str): The last name of the alumni. (Required)
        - sex (str): The gender of the alumni (e.g., 'M', 'F'). (Required)
        - address (str): The address of the alumni. (Required)
        - graduation_year (int): The year the alumni graduated. (Required)
        - user_id (int): The user ID associated with the alumni. (Required)
        - phone (str): The contact phone number of the alumni. (Required)

    Returns:
        str: Update status message.
    """
    try:
        # Construct the SET clause with %s placeholders
        set_clause = ", ".join(f"{col} = %s" for col in data.keys())

        # Construct the SQL query
        sql_query = f"UPDATE alumni SET {set_clause} WHERE alumni_id = %s"

        # Create a tuple of parameter values, appending alumni_id at the end
        params = tuple(data.values()) + (alumni_id,)

        # Debugging: Print the query and parameters
        print(f"Constructed SQL Query: {sql_query}")
        print(f"Parameters: {params}")

        # Call the execute_update function
        rows_affected = execute_update(sql_query, params)

        return f"Update successful. Rows affected: {rows_affected}" if rows_affected else "No rows updated."

    except Exception as e:
        return f"Error in update_alumni: {str(e)}"


def delete_alumni(alumni_id):
    """
    Deletes an alumni record from the database.

    Args:
        alumni_id (int): The unique ID of the alumni to delete. (Required)

    Returns:
        str: A success message if the deletion is successful,
             or an error message if something goes wrong.
    """
    try:
        # SQL query to delete the alumni record
        sql_query = "DELETE FROM alumni WHERE alumni_id = %s"

        # Execute the query with the alumni_id as a parameter
        rows_affected = execute_update(sql_query, (alumni_id,))

        # Check if any row was deleted
        if rows_affected > 0:
            return "Alumni deleted successfully."
        else:
            return "No alumni found with the given ID."

    except Exception as e:
        logging.error("Error deleting alumni", exc_info=True)
        return f"Error: {str(e)}"


def find_alumni_by_name(name):
    """
    Finds alumni by their first or last name.

    Args:
        name (str): Name or partial name to search for.

    Returns:
        dict: A dictionary containing:
            - 'status' (str): 'success' or 'error'.
            - 'alumni_list' (list): List of alumni records as dictionaries (on success).
            - 'message' (str): Error message (on failure).
    """
    try:
        # SQL query with parameterized LIKE clauses
        sql_query = "SELECT * FROM alumni WHERE first_name ILIKE %s OR last_name ILIKE %s"
        
        # Execute the query with the search pattern
        columns, results = query(sql_query, (f"%{name}%", f"%{name}%"))
        
        # Convert the query results to a list of dictionaries
        alumni_list = [dict(zip(columns, row)) for row in results]
        
        return {"status": "success", "alumni_list": alumni_list}
    except Exception as e:
        logging.error("Error finding alumni by name", exc_info=True)
        return {"status": "error", "message": str(e)}


def get_alumni_by_graduation_year(year):
    """
    Retrieves alumni by their graduation year.

    Args:
        year (int): The graduation year to filter by.

    Returns:
        dict: A dictionary containing:
            - 'status' (str): 'success' or 'error'.
            - 'alumni_list' (list): List of alumni records as dictionaries (on success).
            - 'message' (str): Error message (on failure).
    """
    try:
        # SQL query to filter alumni by graduation year
        sql_query = "SELECT * FROM alumni WHERE graduation_year = %s"
        
        # Execute the query with the year parameter
        columns, results = query(sql_query, (year,))
        
        # Convert the query results to a list of dictionaries
        alumni_list = [dict(zip(columns, row)) for row in results]
        
        return {"status": "success", "alumni_list": alumni_list}
    except Exception as e:
        logging.error("Error retrieving alumni by graduation year", exc_info=True)
        return {"status": "error", "message": str(e)}

def list_alumni():
    """
    Lists all alumni in the database.

    Returns:
        dict: A dictionary containing:
            - 'status' (str): 'success' or 'error'.
            - 'alumni_list' (list): List of alumni records as dictionaries (on success).
            - 'message' (str): Error message (on failure).
    """
    try:
        # SQL query to fetch all alumni records
        sql_query = "SELECT * FROM alumni"
        
        # Execute the query
        columns, results = query(sql_query)
        
        # Convert results to a list of dictionaries
        alumni_list = [dict(zip(columns, row)) for row in results]
        
        return {"status": "success", "alumni_list": alumni_list}
    except Exception as e:
        logging.error("Error listing alumni", exc_info=True)
        return {"status": "error", "message": str(e)}

def update_alumni_career_history(alumni_id, career_data):
    """
    Updates an alumni's career history in the database.

    Args:
        alumni_id (int): The unique ID of the alumni.
        career_data (dict): A dictionary containing career history details:
            - job_title (str): The title of the job. (Required)
            - company (str): The name of the company. (Required)
            - start_date (str): The start date of the job in YYYY-MM-DD format. (Required)
            - end_date (str): The end date of the job in YYYY-MM-DD format. (Optional)
            - monthly_salary (float): The monthly salary for the job. (Optional)

    Returns:
        str: A success message or an error message.
    """
    try:
        # SQL query to insert new career history for the alumni
        sql_query = """
            INSERT INTO career_history (job_title, company, start_date, end_date, monthly_salary, alumni_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        # Execute the query with the provided career data
        params = (
            career_data['job_title'],
            career_data['company'],
            career_data['start_date'],
            career_data.get('end_date'),
            career_data.get('monthly_salary'),
            alumni_id
        )
        
        rows_affected = execute_update(sql_query, params)
        return "Career history updated successfully." if rows_affected else "No records updated."
    except Exception as e:
        logging.error("Error updating career history", exc_info=True)
        return f"Error: {str(e)}"

def get_alumni_donations(alumni_id):
    """
    Retrieves a list of donations made by an alumni.

    Args:
        alumni_id (int): The unique ID of the alumni.

    Returns:
        dict: A dictionary containing:
            - 'status' (str): 'success' or 'error'.
            - 'donations' (list): List of donation records as dictionaries (on success).
            - 'message' (str): Error message (on failure).
    """
    try:
        # SQL query to retrieve donations for a specific alumni
        sql_query = "SELECT * FROM donation WHERE alumni_id = %s"

        # Execute the query
        columns, results = query(sql_query, (alumni_id,))

        # Convert results to a list of dictionaries
        donations = [dict(zip(columns, row)) for row in results]

        return {"status": "success", "donations": donations}
    except Exception as e:
        logging.error("Error retrieving alumni donations", exc_info=True)
        return {"status": "error", "message": str(e)}

def get_degree(Alumni_ID):
    """
    Retrieves the degree details of an alumni.

    Args:
        Alumni_ID (int): The unique ID of the alumni.

    Returns:
        dict: A dictionary containing:
            - 'status' (str): 'success' or 'error'.
            - 'degree' (dict): Degree details as a dictionary (on success).
            - 'message' (str): Error message (on failure).
    """
    try:
        # SQL query to retrieve degree details for a specific alumni
        sql_query = "SELECT * FROM earned_by JOIN degree_ ON earned_by.degree_id = degree_.degree_id WHERE alumni_id = %s"

        # Execute the query
        columns, results = query(sql_query, (Alumni_ID,))

        # Convert results to a dictionary
        degree = dict(zip(columns, results[0]) if results else {})

        return {"status": "success", "degree": degree}
    except Exception as e:
        logging.error("Error retrieving alumni degree", exc_info=True)
        return {"status": "error", "message": str(e)}

def get_alumni_achievements(alumni_id):
    """
    Retrieves a list of achievements for a specific alumni.

    Args:
        alumni_id (int): The unique ID of the alumni.

    Returns:
        dict: A dictionary containing:
            - 'status' (str): 'success' or 'error'.
            - 'achievements' (list): List of achievement records as dictionaries (on success).
            - 'message' (str): Error message (on failure).
    """
    try:
        # SQL query to retrieve achievements for a specific alumni
        sql_query = "SELECT * FROM achievement WHERE alumni_id = %s"

        # Execute the query
        columns, results = query(sql_query, (alumni_id,))

        # Convert results to a list of dictionaries
        achievements = [dict(zip(columns, row)) for row in results]

        return {"status": "success", "achievements": achievements}
    except Exception as e:
        logging.error("Error retrieving alumni achievements", exc_info=True)
        return {"status": "error", "message": str(e)}

def create_user(username, password, role):
    """
    Creates a new user in the database.

    Args:
        username (str): Username for the new user. (Required)
        password (str): Password for the new user. (Required)
        role (str): Role of the user (e.g., 'Admin', 'User', 'Analyst'). (Required)

    Returns:
        str: A success message or an error message.
    """
    try:
        # SQL query to insert a new user
        sql_query = """
            INSERT INTO user_ (user_name, password, role)
            VALUES (%s, %s, %s)
        """
        
        # Execute the query with the provided parameters
        rows_affected = execute_update(sql_query, (username, password, role))
        
        sql_query_4_user_id = """
            select user_id from user_ where user_name = %s and password = %s and role = %s
        """
        import time
        time.sleep(0.1)

        column_names, rows = query(sql_query_4_user_id, (username, password, role))
        user_id = rows[0][0]
        
        return str(user_id) if user_id else "Error: Failed to create user."
    except Exception as e:
        logging.error("Error creating user", exc_info=True)
        return f"Error: {str(e)}"

def delete_user(user_id):
    """
    Deletes a user from the database.

    Args:
        user_id (int): ID of the user to delete. (Required)

    Returns:
        str: A success message or an error message.
    """
    try:
        # SQL query to delete a user
        sql_query = "DELETE FROM user_ WHERE user_id = %s"

        # Execute the query with the user ID as a parameter
        rows_affected = execute_update(sql_query, (user_id,))
        
        return "User deleted successfully." if rows_affected else "No user found with the given ID."
    except Exception as e:
        logging.error("Error deleting user", exc_info=True)
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
        query(sql_query, (*data.values(), user_id))
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
        columns, results = query(sql_query, (user_id,))
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
        sql_query = "UPDATE users SET role = %s WHERE alumni_id = %s"
        query(sql_query, (role, user_id))
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
# Career History Management Functions

# Career History CRUD Functions
def add_career_history(alumni_id, career_data):
    """
    Adds a career history record for an alumni.

    Args:
        alumni_id (int): Alumni ID.
        career_data (dict): Career history details.

    Returns:
        str: Success or error message.
    """
    try:
        sql_query = """
            INSERT INTO career_history (job_title, company, start_date, end_date, monthly_salary, job_description, alumni_id)
            VALUES (%s, %s, %s, %s, %s,%s, %s)
        """
        query(sql_query, (
            career_data['job_title'], career_data['company'], career_data['start_date'],
            career_data.get('end_date'),career_data.get('monthly_salary'), career_data.get('job_description'), alumni_id
        ))
        return "Career history added successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def update_career_history(career_id, data):
    """
    Updates a career history record.

    Args:
        career_id (int): Career History ID.
        data (dict): Career history details to update.

    Returns:
        str: Success or error message.
    """
    try:
        updates = ", ".join(f"{key} = %s" for key in data.keys())
        sql_query = f"UPDATE career_history SET {updates} WHERE career_id = %s"
        query(sql_query, (*data.values(), career_id))
        return "Career history updated successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def delete_career_history(career_id):
    """
    Deletes a career history record.

    Args:
        career_id (int): Career History ID.

    Returns:
        str: Success or error message.
    """
    try:
        sql_query = "DELETE FROM career_history WHERE career_id = %s"
        query(sql_query, (career_id,))
        return "Career history deleted successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def get_career_history(career_id):
    """
    Retrieves a career history record.

    Args:
        career_id (int): Career History ID.

    Returns:
        dict: Career history details or error message.
    """
    try:
        sql_query = "SELECT * FROM career_history WHERE career_id = %s"
        columns, results = query(sql_query, (career_id,))
        if not results:
            return {"status": "error", "message": "Career history not found"}

        career_details = dict(zip(columns, results[0]))
        return {"status": "success", "career_details": career_details}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Career Analysis Functions
def get_salary_trends(department, year_range):
    """
    Retrieves salary trends for alumni in a given department over a specific year range.

    Args:
        department (str): Department name.
        year_range (tuple): Tuple containing start year and end year.

    Returns:
        dict: Salary trends data or error message.
    """
    try:
        start_year, end_year = year_range
        sql_query = """
            SELECT ch.start_date, ch.monthly_salary, d.department
            FROM career_history ch
            JOIN degree_ d ON ch.alumni_id = d.alumni_id
            WHERE d.department = %s AND EXTRACT(YEAR FROM ch.start_date) BETWEEN %s AND %s
        """
        columns, results = query(sql_query, (department, start_year, end_year))
        salary_trends = [dict(zip(columns, row)) for row in results]
        return {"status": "success", "salary_trends": salary_trends}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_career_paths(alumni_id):
    """
    Retrieves the career paths of an alumni.

    Args:
        alumni_id (int): Alumni ID.

    Returns:
        dict: Career path details or error message.
    """
    try:
        sql_query = """
            SELECT *
            FROM career_history
            WHERE alumni_id = %s
            ORDER BY start_date ASC
        """
        columns, results = query(sql_query, (alumni_id,))
        career_paths = [dict(zip(columns, row)) for row in results]
        return {"status": "success", "career_paths": career_paths}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Donation Management Functions

# Donation CRUD Functions
def record_donation(alumni_id, donation_data):
    """
    Records a new donation for an alumni.

    Args:
        alumni_id (int): Alumni ID.
        donation_data (dict): Donation details.

    Returns:
        str: Success or error message.
    """
    try:
        sql_query = """
            INSERT INTO donation (alumni_id, amount, date, donation_type)
            VALUES (%s, %s, %s, %s)
        """
        query(sql_query, (
            alumni_id, donation_data['amount'], donation_data['date'], donation_data['donation_type']
        ))
        return "Donation recorded successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def update_donation(donation_id, data):
    """
    Updates a donation record.

    Args:
        donation_id (int): Donation ID.
        data (dict): Donation details to update.

    Returns:
        str: Success or error message.
    """
    try:
        updates = ", ".join(f"{key} = %s" for key in data.keys())
        sql_query = f"UPDATE donation SET {updates} WHERE donation_id = %s"
        query(sql_query, (*data.values(), donation_id))
        return "Donation updated successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def delete_donation(donation_id):
    """
    Deletes a donation record.

    Args:
        donation_id (int): Donation ID.

    Returns:
        str: Success or error message.
    """
    try:
        sql_query = "DELETE FROM donation WHERE donation_id = %s"
        query(sql_query, (donation_id,))
        return "Donation deleted successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def get_donation(donation_id):
    """
    Retrieves a donation record.

    Args:
        donation_id (string): Donation ID.

    Returns:
        dict: Donation details or error message.
    """
    try:
        sql_query = "SELECT * FROM donation WHERE alumni_id = %s"
        columns, results = query(sql_query, (donation_id,))
        if not results:
            return {"status": "error", "message": "Donation not found"}

        donation_details = dict(zip(columns, results))
        return {"status": "success", "donation_details": donation_details}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Donation Analysis Functions
def get_total_donations_by_alumni(alumni_id):
    """
    Retrieves the total amount of donations made by an alumni.

    Args:
        alumni_id (int): Alumni ID.

    Returns:
        dict: Total donation amount or error message.
    """
    try:
        sql_query = "SELECT SUM(amount) as total_donations FROM donation WHERE alumni_id = %s"
        columns, results = query(sql_query, (alumni_id,))
        total_donations = dict(zip(columns, results[0]))
        return {"status": "success", "total_donations": total_donations}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_top_donors(limit=10):
    """
    Retrieves the top donors.

    Args:
        limit (int): Number of top donors to retrieve.

    Returns:
        dict: List of top donors or error message.
    """
    try:
        sql_query = """
            SELECT alumni_id, SUM(amount) as total_amount
            FROM donation
            GROUP BY alumni_id
            ORDER BY total_amount DESC
            LIMIT %s
        """
        columns, results = query(sql_query, (limit,))
        top_donors = [dict(zip(columns, row)) for row in results]
        return {"status": "success", "top_donors": top_donors}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_donation_trends(year_range):
    """
    Retrieves donation trends over a specific year range.

    Args:
        year_range (tuple): Tuple containing start year and end year.

    Returns:
        dict: Donation trends data or error message.
    """
    try:
        start_year, end_year = year_range
        sql_query = """
            SELECT EXTRACT(YEAR FROM date) as year, SUM(amount) as total_amount
            FROM donation
            WHERE EXTRACT(YEAR FROM date) BETWEEN %s AND %s
            GROUP BY year
            ORDER BY year
        """
        columns, results = query(sql_query, (start_year, end_year))
        trends = [dict(zip(columns, row)) for row in results]
        return {"status": "success", "donation_trends": trends}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Achievement Management Functions

# Achievement CRUD Functions
def add_achievement(achievement_data):
    """
    Adds a new achievement for an alumni.

    Args:
        achievement_data (dict): Achievement details.

    Returns:
        str: Success or error message.
    """
    try:
        sql_query = """
            INSERT INTO achievement (alumnileader_id, title, description, date, category)
            VALUES (%s, %s, %s, %s, %s)
        """
        query(sql_query, (
            achievement_data['title'], achievement_data['description'], 
            achievement_data['date'], achievement_data['category'], achievement_data['alumnileader_id']
        ))
        return "Achievement added successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def update_achievement(data):
    """
    Updates an achievement record.

    Args:
        achievement_id (int): Achievement ID.
        data (dict): Achievement details to update.

    Returns:
        str: Success or error message.
    """
    try:
        updates = ", ".join(f"{key} = %s" for key in data.keys() if key!= 'alumnileader_id' and key!= 'date' and key!= 'title')
        
        sql_query = f"UPDATE achievement SET {updates} WHERE title = %s AND date = %s AND alumnileader_id = %s"
        alumnileader_id = data.pop('alumnileader_id')
        date = data.pop('date')
        title = data.pop('title')
        query(sql_query, (*data.values(), title, date, alumnileader_id))
        return "Achievement updated successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def delete_achievement(data):
    """
    Deletes an achievement record.

    Args:
        data (dict): Achievement details to delete.
            - title (str): Achievement title.
            - date (str): Achievement date.
            - alumnileader_id (int): Alumni leader ID.
    Returns:
        str: Success or error message.
    """
    try:
        sql_query = "DELETE FROM achievement WHERE title = %s AND date = %s AND alumnileader_id = %s"
        query(sql_query, (data['title'], data['date'], data['alumnileader_id']))
        return "Achievement deleted successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def get_achievement(achievement_id):
    """
    Retrieves an achievement record.

    Args:
        achievement_id (int): Achievement ID.

    Returns:
        dict: Achievement details or error message.
    """
    try:
        sql_query = "SELECT * FROM achievement WHERE achievement_id = %s"
        columns, results = query(sql_query, (achievement_id,))
        if not results:
            return {"status": "error", "message": "Achievement not found"}

        achievement_details = dict(zip(columns, results[0]))
        return {"status": "success", "achievement_details": achievement_details}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Achievement Queries Functions
def list_achievements(alumni_id):
    """
    Lists all achievements for a specific alumni.

    Args:
        alumni_id (int): Alumni ID.

    Returns:
        dict: List of achievements or error message.
    """
    try:
        sql_query = "SELECT * FROM achievement WHERE alumni_id = %s"
        columns, results = query(sql_query, (alumni_id,))
        achievements = [dict(zip(columns, row)) for row in results]
        return {"status": "success", "achievements": achievements}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def find_achievements_by_category(category):
    """
    Finds achievements by category.

    Args:
        category (str): Achievement category to search for.

    Returns:
        dict: List of achievements or error message.
    """
    try:
        sql_query = "SELECT * FROM achievement WHERE category = %s"
        columns, results = query(sql_query, (category,))
        achievements = [dict(zip(columns, row)) for row in results]
        return {"status": "success", "achievements": achievements}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Association Management Functions

# Association CRUD Functions
def create_association(data):
    """
    Creates a new association.

    Args:
        data (dict): Association details.
            - associaiton_name (str): Association name.
            - address (str): Association address.
            - phone (str): Association phone number.
            - email (str): Association email address.
            - founded_year (int): Year the association was founded.
            - description (str): Association description.
    Returns:
        str: Success or error message.
    """
    try:
        sql_query = """
            INSERT INTO alumni_association (association_name, address, phone, email, founded_year, description)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        query(sql_query, (data['association_name'], data['address'], data['phone'], data['email'], data['founded_year'], data['description']))
        return "Association created successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def update_association(association_id, data):
    """
    Updates an association record.

    Args:
        association_id (int): Association ID.
        data (dict): Association details to update.

    Returns:
        str: Success or error message.
    """
    try:
        updates = ", ".join(f"{key} = %s" for key in data.keys())
        sql_query = f"UPDATE alumni_association SET {updates} WHERE association_id = %s"
        query(sql_query, (*data.values(), association_id))
        return "Association updated successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def delete_association(association_id):
    """
    Deletes an association.

    Args:
        association_id (int): Association ID.

    Returns:
        str: Success or error message.
    """
    try:
        sql_query = "DELETE FROM alumni_association WHERE association_id = %s"
        query(sql_query, (association_id,))
        return "Association deleted successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def get_association(association_id):
    """
    Retrieves an association record.

    Args:
        association_id (int): Association ID.

    Returns:
        dict: Association details or error message.
    """
    try:
        sql_query = "SELECT * FROM alumni_association WHERE association_id = %s"
        columns, results = query(sql_query, (association_id,))
        if not results:
            return {"status": "error", "message": "Association not found"}

        association_details = dict(zip(columns, results[0]))
        return {"status": "success", "association_details": association_details}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Membership Management Functions
def add_member_to_association(alumni_id, association_id, data):
    """
    Adds a member to an association.

    Args:
        alumni_id (int): Alumni ID.
        association_id (int): Association ID.

    Returns:
        str: Success or error message.
    """
    try:
        sql_query = """
            INSERT INTO is_member (alumni_id, association_id, date_joined)
            VALUES (%s, %s, %s)
        """
        query(sql_query, (alumni_id, association_id, data['date_joined']))
        return "Member added to association successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def remove_member_from_association(alumni_id, association_id):
    """
    Removes a member from an association.

    Args:
        alumni_id (int): Alumni ID.
        association_id (int): Association ID.

    Returns:
        str: Success or error message.
    """
    try:
        sql_query = "DELETE FROM is_member WHERE alumni_id = %s AND association_id = %s"
        query(sql_query, (alumni_id, association_id))
        return "Member removed from association successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def list_association_members(association_id):
    """
    Lists all members of an association.

    Args:
        association_id (int): Association ID.

    Returns:
        dict: List of members or error message.
    """
    try:
        sql_query = """
            SELECT a.alumni_id, al.first_name, al.last_name
            FROM is_member a
            JOIN alumni al ON a.alumni_id = al.alumni_id
            WHERE a.association_id = %s
        """
        columns, results = query(sql_query, (association_id,))
        members = [dict(zip(columns, row)) for row in results]
        return {"status": "success", "members": members}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Event Management Functions
def create_event(association_id, event_data):
    """
    Creates an event for an association.

    Args:
        association_id (int): Association ID.
        event_name (int): Association ID.
        date (str): Event date in YYYY-MM-DD format.
        description (str): Event description.
        location (str): Event location.

    Returns:
        str: Success or error message.
    """
    try:
        sql_query = """
            INSERT INTO association_event (event_name, date, description, location)
            VALUES (%s, %s, %s, %s)
        """
        query(sql_query, (
            event_data['event_name'], event_data['date'], event_data['description'], event_data['location']
        ))

        sql_query = """
            INSERT INTO held_by (association_id, event_name, date)
            VALUES (%s, %s, %s)
        """
        query(sql_query, (association_id, event_data['event_name'], event_data['date']))
        return "Event created successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def update_event(association_id, event_data):
    """
    Updates an event record.

    Args:
        association_id (int): Association ID.
        event_name (int): Association ID.
        date (str): Event date in YYYY-MM-DD format.
        description (str): Event description.
        location (str): Event location.

    Returns:
        str: Success or error message.
    """
    try:
        sql_query = """
            UPDATE association_event
            SET description = %s, location = %s
            WHERE event_name = %s AND date = %s
        """
        query(sql_query, (event_data['description'], event_data['location'], event_data['event_name'], event_data['date']))
        return "Event updated successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def delete_event(event_id, data):
    """
    Deletes an event.

    Args:
        event_name (int): Event name,
        date (str): Event date in YYYY-MM-DD format.

    Returns:
        str: Success or error message.
    """
    try:
        sql_query = "DELETE FROM association_event WHERE event_name = %s AND date = %s"
        query(sql_query, (data['event_name'],data['date']))
        return "Event deleted successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def list_events_by_association(association_id):
    """
    Lists all events for a specific association.

    Args:
        association_id (int): Association ID.

    Returns:
        dict: List of events or error message.
    """
    try:
        sql_query = "SELECT * FROM held_by WHERE association_id = %s"
        columns, results = query(sql_query, (association_id,))
        events = [dict(zip(columns, row)) for row in results]
        return {"status": "success", "events": events}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Alumni Association Management Functions

# Association CRUD Functions
def create_association(data):
    """
    Creates a new association.

    Args:
        data (dict): Association details.

    Returns:
        str: Success or error message.
    """
    try:
        sql_query = """
            INSERT INTO association (name, description, created_date)
            VALUES (%s, %s, %s)
        """
        query(sql_query, (data['name'], data['description'], data['created_date']))
        return "Association created successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def update_association(association_id, data):
    """
    Updates an association record.

    Args:
        association_id (int): Association ID.
        data (dict): Association details to update.

    Returns:
        str: Success or error message.
    """
    try:
        updates = ", ".join(f"{key} = %s" for key in data.keys())
        sql_query = f"UPDATE association SET {updates} WHERE association_id = %s"
        query(sql_query, (*data.values(), association_id))
        return "Association updated successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def delete_association(association_id):
    """
    Deletes an association.

    Args:
        association_id (int): Association ID.

    Returns:
        str: Success or error message.
    """
    try:
        sql_query = "DELETE FROM association WHERE association_id = %s"
        query(sql_query, (association_id,))
        return "Association deleted successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def get_association(association_id):
    """
    Retrieves an association record.

    Args:
        association_id (int): Association ID.

    Returns:
        dict: Association details or error message.
    """
    try:
        sql_query = "SELECT * FROM association WHERE association_id = %s"
        columns, results = query(sql_query, (association_id,))
        if not results:
            return {"status": "error", "message": "Association not found"}

        association_details = dict(zip(columns, results[0]))
        return {"status": "success", "association_details": association_details}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Membership Management Functions
def add_member_to_association(alumni_id, association_id):
    """
    Adds a member to an association.

    Args:
        alumni_id (int): Alumni ID.
        association_id (int): Association ID.

    Returns:
        str: Success or error message.
    """
    try:
        sql_query = """
            INSERT INTO association_membership (alumni_id, association_id)
            VALUES (%s, %s)
        """
        query(sql_query, (alumni_id, association_id))
        return "Member added to association successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def remove_member_from_association(alumni_id, association_id):
    """
    Removes a member from an association.

    Args:
        alumni_id (int): Alumni ID.
        association_id (int): Association ID.

    Returns:
        str: Success or error message.
    """
    try:
        sql_query = "DELETE FROM association_membership WHERE alumni_id = %s AND association_id = %s"
        query(sql_query, (alumni_id, association_id))
        return "Member removed from association successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def list_association_members(association_id):
    """
    Lists all members of an association.

    Args:
        association_id (int): Association ID.

    Returns:
        dict: List of members or error message.
    """
    try:
        sql_query = """
            SELECT a.alumni_id, al.first_name, al.last_name
            FROM association_membership a
            JOIN alumni al ON a.alumni_id = al.alumni_id
            WHERE a.association_id = %s
        """
        columns, results = query(sql_query, (association_id,))
        members = [dict(zip(columns, row)) for row in results]
        return {"status": "success", "members": members}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Event Management Functions
def create_event(association_id, event_data):
    """
    Creates an event for an association.

    Args:
        association_id (int): Association ID.
        event_data (dict): Event details.

    Returns:
        str: Success or error message.
    """
    try:
        sql_query = """
            INSERT INTO association_event (association_id, title, description, event_date)
            VALUES (%s, %s, %s, %s)
        """
        query(sql_query, (
            association_id, event_data['title'], event_data['description'], event_data['event_date']
        ))
        return "Event created successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def update_event(data):
    """
    Updates an event record.

    Args:
        data (dict): Event details to update.

    Returns:
        str: Success or error message.
    """
    try:
        updates = ", ".join(f"{key} = %s" for key in data.keys() if key not in ['title', 'event_date'])
        sql_query = f"UPDATE association_event SET {updates} WHERE title = %s AND event_date = %s"
        data['event_date'] = data.pop('event_date')
        data['title'] = data.pop('title')
        query(sql_query, (*data.values(), data['title'], data['event_date']))
        return "Event updated successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def delete_event(data):
    """
    Deletes an event.

    Args:
        event_name (int): Event name,
        date (str): Event date in YYYY-MM-DD format.
    
    Returns:
        str: Success or error message.
    """
    try:
        sql_query = "DELETE FROM association_event WHERE event_name = %s AND date = %s"
        query(sql_query, (data['event_name'],data['date']))
        return "Event deleted successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def list_events_by_association(association_id):
    """
    Lists all events for a specific association.

    Args:
        association_id (int): Association ID.

    Returns:
        dict: List of events or error message.
    """
    try:
        sql_query = """
            SELECT * FROM association_event
            JOIN held_by ON association_event.event_name = held_by.event_name AND association_event.date = held_by.date
            WHERE held_by.association_id = %s
        """
        columns, results = query(sql_query, (association_id,))
        events = [dict(zip(columns, row)) for row in results]
        return {"status": "success", "events": events}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Data Analysis Functions

# Trends and Insights Functions
# def get_alumni_employment_trends(department, year_range):
#     """
#     Retrieves alumni employment trends for a specific department over a year range.

#     Args:
#         department (str): Department name.
#         year_range (tuple): Tuple containing start year and end year.

#     Returns:
#         dict: Employment trend data or error message.
#     """
#     try:
#         start_year, end_year = year_range
#         sql_query = """
#             SELECT graduation_year, COUNT(*) AS total_employed
#             FROM career_history ch
#             JOIN alumni al ON ch.alumni_id = al.alumni_id
#             WHERE al.department = %s AND graduation_year BETWEEN %s AND %s
#             GROUP BY graduation_year
#             ORDER BY graduation_year
#         """
#         columns, results = query(sql_query, (department, start_year, end_year))
#         trends = [dict(zip(columns, row)) for row in results]
#         return {"status": "success", "employment_trends": trends}
#     except Exception as e:
#         return {"status": "error", "message": str(e)}

# def calculate_donation_correlations():
#     """
#     Calculates correlations between alumni demographics and donation amounts.

#     Returns:
#         dict: Correlation results or error message.
#     """
#     try:
#         sql_query = """
#             SELECT al.department, COUNT(d.donation_id) AS total_donations, AVG(d.amount) AS avg_donation_amount
#             FROM donation d
#             JOIN alumni al ON d.alumni_id = al.alumni_id
#             GROUP BY al.department
#         """
#         columns, results = query(sql_query)
#         correlations = [dict(zip(columns, row)) for row in results]
#         return {"status": "success", "donation_correlations": correlations}
#     except Exception as e:
#         return {"status": "error", "message": str(e)}

# # Special Reports Functions
# def generate_30_year_reunion_list():
#     """
#     Generates a list of alumni who graduated 30 years ago.

#     Returns:
#         dict: List of alumni or error message.
#     """
#     try:
#         sql_query = """
#             SELECT first_name, last_name, graduation_year
#             FROM alumni
#             WHERE graduation_year = EXTRACT(YEAR FROM NOW()) - 30
#         """
#         columns, results = query(sql_query)
#         reunion_list = [dict(zip(columns, row)) for row in results]
#         return {"status": "success", "reunion_list": reunion_list}
#     except Exception as e:
#         return {"status": "error", "message": str(e)}

# def get_top_achievers(limit=10):
#     """
#     Retrieves the top achievers.

#     Args:
#         limit (int): Number of top achievers to retrieve.

#     Returns:
#         dict: List of top achievers or error message.
#     """
#     try:
#         sql_query = """
#             SELECT alumni_id, title, description, date
#             FROM achievement
#             ORDER BY date DESC
#             LIMIT %s
#         """
#         columns, results = query(sql_query, (limit,))
#         top_achievers = [dict(zip(columns, row)) for row in results]
#         return {"status": "success", "top_achievers": top_achievers}
#     except Exception as e:
#         return {"status": "error", "message": str(e)}

# Event Participation CRUD Functions
def add_event_participant(data):
    """
    Adds a participant to an event.

    Args:
        alumni_id (int): Alumni ID.
        event_name (int): Event name.
        date (str): Date of participation.

    Returns:
        str: Success or error message.
    """
    try:
        sql_query = """
            INSERT INTO event_participated_by (alumni_id, event_name, date)
            VALUES (%s, %s, %s)
        """
        query(sql_query, (data['alumni_id'], data['event_name'], data['date']))
        return "Participant added to event successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def remove_event_participant(data):
    """
    Removes a participant from an event.

    Args:
        alumni_id (int): Alumni ID.
        event_name (int): Event name.

    Returns:
        str: Success or error message.
    """
    try:
        sql_query = "DELETE FROM event_participated_by WHERE alumni_id = %s AND event_name = %s AND date = %s"
        query(sql_query, (data['alumni_id'], data['event_name'], data['date'])) 
        return "Participant removed from event successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def list_participants(data):
    """
    Lists all participants for a specific event.

    Args:
        event_name (int): Event name.
        date (str): Event date.

    Returns:
        dict: List of participants or error message.
    """
    try:
        sql_query = """
            SELECT al.alumni_id, al.first_name, al.last_name
            FROM event_participated_by ep
            JOIN alumni al ON ep.alumni_id = al.alumni_id
            WHERE ep.event_name = %s AND ep.date = %s
        """
        columns, results = query(sql_query, (data['event_name'], data['date']))
        participants = [dict(zip(columns, row)) for row in results]
        return {"status": "success", "participants": participants}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_participation_by_alumni(data):
    """
    Retrieves all events an alumni has participated in.

    Args:
        alumni_id (int): Alumni ID.
    Returns:
        dict: List of events or error message.
    """
    try:
        sql_query = """
            SELECT ae.event_name, ae.date
            FROM event_participated_by ep
            JOIN association_event ae ON ep.event_name = ae.event_name AND ep.date = ae.date
            WHERE ep.alumni_id = %s
        """
        columns, results = query(sql_query, (data['alumni_id'],))
        events = [dict(zip(columns, row)) for row in results]
        return {"status": "success", "events": events}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
def list_user_associations(alumni_id):
    """
    Lists all associations a specific alumni belongs to.

    Args:
        alumni_id (str): Alumni ID.

    Returns:
        dict: List of associations or error message.
    """
    try:
        # SQL query to fetch associations for the given alumni
        sql_query = """
            SELECT a.association_id, 
                asso.association_name,
                asso.address,
                asso.phone,
                asso.email,
                asso.description
            FROM is_member a
            JOIN alumni_association asso ON a.association_id = asso.association_id
            WHERE a.alumni_id = %s
        """
        # Execute the query
        columns, results = query(sql_query, (alumni_id,))
        
        # Format results into a list of dictionaries
        associations = [dict(zip(columns, row)) for row in results]
        
        # Return success response
        return {"status": "success", "associations": associations}
    except Exception as e:
        # Handle errors and return an error response
        return {"status": "error", "message": str(e)}
    
def list_user_association_events(alumni_id):
    """
    Lists all events organized by the associations a specific alumni belongs to.

    Args:
        alumni_id (str): Alumni ID.

    Returns:
        dict: List of events or error message.
    """
    try:
        # SQL query to fetch events organized by associations the alumni belongs to
        sql_query = """
        SELECT DISTINCT ae.event_name, ae.date, ae.description, ae.location, asso.association_name
        FROM association_event ae
        JOIN held_by hb ON ae.event_name = hb.event_name AND ae.date = hb.date
        JOIN is_member a ON hb.association_id = a.association_id
        JOIN alumni_association asso ON a.association_id = asso.association_id
        WHERE a.alumni_id = %s
        ORDER BY ae.date DESC;
        """
        
        # Execute the query
        columns, results = query(sql_query, (alumni_id,))
        
        # Format results into a list of dictionaries
        events = [dict(zip(columns, row)) for row in results]
        
        # Return success response
        return {"status": "success", "events": events}
    except Exception as e:
        # Handle errors and return an error response
        return {"status": "error", "message": str(e)}

    
def get_all_open_association():
    """
    Retrieves an association record.

    Args:
        association_id (int): Association ID.

    Returns:
        dict: Association details or error message.
    """
    try:
        sql_query = "SELECT * FROM alumni_association"
        columns, results = query(sql_query, ())
        if not results:
            return {"status": "error", "message": "Association not found"}

        #association_details = dict(zip(columns, results))
        #there are multiple associations
        associations = [dict(zip(columns, row)) for row in results]
        return {"status": "success", "association_details": associations}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
def get_all_upcoming_events():
    """
    Retrieves an association record.

    Args:
        association_id (int): Association ID.

    Returns:
        dict: Association details or error message.
    """
    try:
        sql_query = "SELECT * FROM association_event WHERE date >= NOW()"
        columns, results = query(sql_query, ())
        if not results:
            return {"status": "error", "message": "Events not found"}

        #association_details = dict(zip(columns, results))
        #there are multiple associations
        events = [dict(zip(columns, row)) for row in results]
        return {"status": "success", "events": events}
    except Exception as e:
        return {"status": "error", "message": str(e)}