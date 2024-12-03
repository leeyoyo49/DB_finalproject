import hashlib
from db_connection import con, query
from flask import Flask, jsonify, request, session

# Utility Functions
def login_user(username, password):
    """
    Authenticates a user by verifying the provided credentials.

    Args:
        username (str): The username of the user attempting to log in.
        password (str): The plaintext password of the user.

    Returns:
        dict or None: A dictionary containing the user's details ('user_id', 'username', 'role') if authentication is successful, otherwise None.
    """
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
    """
    Checks if the current session user has the required role to access an endpoint.

    Args:
        required_role (str): The role required to access the endpoint (e.g., "Admin", "User").

    Returns:
        tuple: A tuple containing:
            - (bool): Whether the user has the required permissions.
            - (str): A message indicating the status ("Unauthorized", "Permission denied", or an empty string if successful).
    """
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
            INSERT INTO career_history (job_title, company, start_date, end_date, monthly_salary, alumni_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        query(con, sql_query, (
            career_data['job_title'], career_data['company'], career_data['start_date'],
            career_data.get('end_date'), career_data.get('monthly_salary'), alumni_id
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
        query(con, sql_query, (*data.values(), career_id))
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
        query(con, sql_query, (career_id,))
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
        columns, results = query(con, sql_query, (career_id,))
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
            JOIN degree d ON ch.alumni_id = d.alumni_id
            WHERE d.department = %s AND EXTRACT(YEAR FROM ch.start_date) BETWEEN %s AND %s
        """
        columns, results = query(con, sql_query, (department, start_year, end_year))
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
            SELECT job_title, company, start_date, end_date
            FROM career_history
            WHERE alumni_id = %s
            ORDER BY start_date ASC
        """
        columns, results = query(con, sql_query, (alumni_id,))
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
            INSERT INTO donation (alumni_id, amount, date, campaign_id)
            VALUES (%s, %s, %s, %s)
        """
        query(con, sql_query, (
            alumni_id, donation_data['amount'], donation_data['date'], donation_data.get('campaign_id')
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
        query(con, sql_query, (*data.values(), donation_id))
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
        query(con, sql_query, (donation_id,))
        return "Donation deleted successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def get_donation(donation_id):
    """
    Retrieves a donation record.

    Args:
        donation_id (int): Donation ID.

    Returns:
        dict: Donation details or error message.
    """
    try:
        sql_query = "SELECT * FROM donation WHERE donation_id = %s"
        columns, results = query(con, sql_query, (donation_id,))
        if not results:
            return {"status": "error", "message": "Donation not found"}

        donation_details = dict(zip(columns, results[0]))
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
        columns, results = query(con, sql_query, (alumni_id,))
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
        columns, results = query(con, sql_query, (limit,))
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
        columns, results = query(con, sql_query, (start_year, end_year))
        trends = [dict(zip(columns, row)) for row in results]
        return {"status": "success", "donation_trends": trends}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Achievement Management Functions

# Achievement CRUD Functions
def add_achievement(alumni_id, achievement_data):
    """
    Adds a new achievement for an alumni.

    Args:
        alumni_id (int): Alumni ID.
        achievement_data (dict): Achievement details.

    Returns:
        str: Success or error message.
    """
    try:
        sql_query = """
            INSERT INTO achievement (alumni_id, title, description, date, category)
            VALUES (%s, %s, %s, %s, %s)
        """
        query(con, sql_query, (
            alumni_id, achievement_data['title'], achievement_data['description'], 
            achievement_data['date'], achievement_data['category']
        ))
        return "Achievement added successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def update_achievement(achievement_id, data):
    """
    Updates an achievement record.

    Args:
        achievement_id (int): Achievement ID.
        data (dict): Achievement details to update.

    Returns:
        str: Success or error message.
    """
    try:
        updates = ", ".join(f"{key} = %s" for key in data.keys())
        sql_query = f"UPDATE achievement SET {updates} WHERE achievement_id = %s"
        query(con, sql_query, (*data.values(), achievement_id))
        return "Achievement updated successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def delete_achievement(achievement_id):
    """
    Deletes an achievement record.

    Args:
        achievement_id (int): Achievement ID.

    Returns:
        str: Success or error message.
    """
    try:
        sql_query = "DELETE FROM achievement WHERE achievement_id = %s"
        query(con, sql_query, (achievement_id,))
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
        columns, results = query(con, sql_query, (achievement_id,))
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
        columns, results = query(con, sql_query, (alumni_id,))
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
        columns, results = query(con, sql_query, (category,))
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

    Returns:
        str: Success or error message.
    """
    try:
        sql_query = """
            INSERT INTO association (name, description, created_date)
            VALUES (%s, %s, %s)
        """
        query(con, sql_query, (data['name'], data['description'], data['created_date']))
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
        query(con, sql_query, (*data.values(), association_id))
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
        query(con, sql_query, (association_id,))
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
        columns, results = query(con, sql_query, (association_id,))
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
        query(con, sql_query, (alumni_id, association_id))
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
        query(con, sql_query, (alumni_id, association_id))
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
        columns, results = query(con, sql_query, (association_id,))
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
        query(con, sql_query, (
            association_id, event_data['title'], event_data['description'], event_data['event_date']
        ))
        return "Event created successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def update_event(event_id, data):
    """
    Updates an event record.

    Args:
        event_id (int): Event ID.
        data (dict): Event details to update.

    Returns:
        str: Success or error message.
    """
    try:
        updates = ", ".join(f"{key} = %s" for key in data.keys())
        sql_query = f"UPDATE association_event SET {updates} WHERE event_id = %s"
        query(con, sql_query, (*data.values(), event_id))
        return "Event updated successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def delete_event(event_id):
    """
    Deletes an event.

    Args:
        event_id (int): Event ID.

    Returns:
        str: Success or error message.
    """
    try:
        sql_query = "DELETE FROM association_event WHERE event_id = %s"
        query(con, sql_query, (event_id,))
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
        sql_query = "SELECT * FROM association_event WHERE association_id = %s"
        columns, results = query(con, sql_query, (association_id,))
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
        query(con, sql_query, (data['name'], data['description'], data['created_date']))
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
        query(con, sql_query, (*data.values(), association_id))
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
        query(con, sql_query, (association_id,))
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
        columns, results = query(con, sql_query, (association_id,))
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
        query(con, sql_query, (alumni_id, association_id))
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
        query(con, sql_query, (alumni_id, association_id))
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
        columns, results = query(con, sql_query, (association_id,))
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
        query(con, sql_query, (
            association_id, event_data['title'], event_data['description'], event_data['event_date']
        ))
        return "Event created successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def update_event(event_id, data):
    """
    Updates an event record.

    Args:
        event_id (int): Event ID.
        data (dict): Event details to update.

    Returns:
        str: Success or error message.
    """
    try:
        updates = ", ".join(f"{key} = %s" for key in data.keys())
        sql_query = f"UPDATE association_event SET {updates} WHERE event_id = %s"
        query(con, sql_query, (*data.values(), event_id))
        return "Event updated successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def delete_event(event_id):
    """
    Deletes an event.

    Args:
        event_id (int): Event ID.

    Returns:
        str: Success or error message.
    """
    try:
        sql_query = "DELETE FROM association_event WHERE event_id = %s"
        query(con, sql_query, (event_id,))
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
        sql_query = "SELECT * FROM association_event WHERE association_id = %s"
        columns, results = query(con, sql_query, (association_id,))
        events = [dict(zip(columns, row)) for row in results]
        return {"status": "success", "events": events}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Data Analysis Functions

# Trends and Insights Functions
def get_alumni_employment_trends(department, year_range):
    """
    Retrieves alumni employment trends for a specific department over a year range.

    Args:
        department (str): Department name.
        year_range (tuple): Tuple containing start year and end year.

    Returns:
        dict: Employment trend data or error message.
    """
    try:
        start_year, end_year = year_range
        sql_query = """
            SELECT graduation_year, COUNT(*) AS total_employed
            FROM career_history ch
            JOIN alumni al ON ch.alumni_id = al.alumni_id
            WHERE al.department = %s AND graduation_year BETWEEN %s AND %s
            GROUP BY graduation_year
            ORDER BY graduation_year
        """
        columns, results = query(con, sql_query, (department, start_year, end_year))
        trends = [dict(zip(columns, row)) for row in results]
        return {"status": "success", "employment_trends": trends}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def analyze_event_participation_rates():
    """
    Analyzes participation rates for all events.

    Returns:
        dict: Participation rates or error message.
    """
    try:
        sql_query = """
            SELECT event_id, title, COUNT(participant_id) AS total_participants
            FROM event_participation ep
            JOIN association_event ae ON ep.event_id = ae.event_id
            GROUP BY event_id, title
            ORDER BY total_participants DESC
        """
        columns, results = query(con, sql_query)
        participation_rates = [dict(zip(columns, row)) for row in results]
        return {"status": "success", "participation_rates": participation_rates}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def calculate_donation_correlations():
    """
    Calculates correlations between alumni demographics and donation amounts.

    Returns:
        dict: Correlation results or error message.
    """
    try:
        sql_query = """
            SELECT al.department, COUNT(d.donation_id) AS total_donations, AVG(d.amount) AS avg_donation_amount
            FROM donation d
            JOIN alumni al ON d.alumni_id = al.alumni_id
            GROUP BY al.department
        """
        columns, results = query(con, sql_query)
        correlations = [dict(zip(columns, row)) for row in results]
        return {"status": "success", "donation_correlations": correlations}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Special Reports Functions
def generate_30_year_reunion_list():
    """
    Generates a list of alumni who graduated 30 years ago.

    Returns:
        dict: List of alumni or error message.
    """
    try:
        sql_query = """
            SELECT first_name, last_name, graduation_year
            FROM alumni
            WHERE graduation_year = EXTRACT(YEAR FROM NOW()) - 30
        """
        columns, results = query(con, sql_query)
        reunion_list = [dict(zip(columns, row)) for row in results]
        return {"status": "success", "reunion_list": reunion_list}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_top_achievers(limit=10):
    """
    Retrieves the top achievers.

    Args:
        limit (int): Number of top achievers to retrieve.

    Returns:
        dict: List of top achievers or error message.
    """
    try:
        sql_query = """
            SELECT alumni_id, title, description, date
            FROM achievement
            ORDER BY date DESC
            LIMIT %s
        """
        columns, results = query(con, sql_query, (limit,))
        top_achievers = [dict(zip(columns, row)) for row in results]
        return {"status": "success", "top_achievers": top_achievers}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_event_participation_statistics(event_id):
    """
    Retrieves participation statistics for a specific event.

    Args:
        event_id (int): Event ID.

    Returns:
        dict: Event participation statistics or error message.
    """
    try:
        sql_query = """
            SELECT event_id, title, COUNT(participant_id) AS total_participants
            FROM event_participation ep
            JOIN association_event ae ON ep.event_id = ae.event_id
            WHERE ep.event_id = %s
            GROUP BY event_id, title
        """
        columns, results = query(con, sql_query, (event_id,))
        if not results:
            return {"status": "error", "message": "Event not found or no participants"}

        participation_stats = dict(zip(columns, results[0]))
        return {"status": "success", "participation_statistics": participation_stats}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Event Participation Functions

# Event Participation CRUD Functions
def add_event_participant(alumni_id, event_id):
    """
    Adds a participant to an event.

    Args:
        alumni_id (int): Alumni ID.
        event_id (int): Event ID.

    Returns:
        str: Success or error message.
    """
    try:
        sql_query = """
            INSERT INTO event_participation (alumni_id, event_id)
            VALUES (%s, %s)
        """
        query(con, sql_query, (alumni_id, event_id))
        return "Participant added to event successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def remove_event_participant(alumni_id, event_id):
    """
    Removes a participant from an event.

    Args:
        alumni_id (int): Alumni ID.
        event_id (int): Event ID.

    Returns:
        str: Success or error message.
    """
    try:
        sql_query = "DELETE FROM event_participation WHERE alumni_id = %s AND event_id = %s"
        query(con, sql_query, (alumni_id, event_id))
        return "Participant removed from event successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def list_participants(event_id):
    """
    Lists all participants for a specific event.

    Args:
        event_id (int): Event ID.

    Returns:
        dict: List of participants or error message.
    """
    try:
        sql_query = """
            SELECT ep.alumni_id, al.first_name, al.last_name
            FROM event_participation ep
            JOIN alumni al ON ep.alumni_id = al.alumni_id
            WHERE ep.event_id = %s
        """
        columns, results = query(con, sql_query, (event_id,))
        participants = [dict(zip(columns, row)) for row in results]
        return {"status": "success", "participants": participants}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_participation_by_alumni(alumni_id):
    """
    Retrieves all events an alumni has participated in.

    Args:
        alumni_id (int): Alumni ID.

    Returns:
        dict: List of events or error message.
    """
    try:
        sql_query = """
            SELECT ep.event_id, ae.title, ae.event_date
            FROM event_participation ep
            JOIN association_event ae ON ep.event_id = ae.event_id
            WHERE ep.alumni_id = %s
        """
        columns, results = query(con, sql_query, (alumni_id,))
        events = [dict(zip(columns, row)) for row in results]
        return {"status": "success", "events": events}
    except Exception as e:
        return {"status": "error", "message": str(e)}

