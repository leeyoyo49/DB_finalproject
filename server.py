from flask import Flask, jsonify, request, session
from db_connection import connect_to_db, query
from usermanagement import *

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for session management

# Establish database connection
con = connect_to_db()

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


# User management functions
@app.route('/login', methods=['POST'])
def login():
    """
    Endpoint for user login.

    Input JSON:
        {
            "username": "b11705022",
            "password": "admin"
        }

    Returns:
        JSON with login success or failure.
    """
    data = request.json
    if not data or "username" not in data or "password" not in data:
        return jsonify({"status": "error", "message": "Missing username or password"}), 400

    username = data['username']
    password = data['password']
    user = login_user(username, password)

    if user:
        session['user_id'] = user['user_id']
        session['username'] = user['username']
        session['role'] = user['role']
        return jsonify({"status": "success", "message": "Login successful"}), 200
    return jsonify({"status": "error", "message": "Invalid username or password"}), 401


@app.route('/logout', methods=['POST'])
def logout():
    """
    Endpoint for user logout.
    
    Clears the session and logs the user out.
    """
    session.clear()
    return jsonify({"status": "success", "message": "Logout successful"}), 200


@app.route('/dashboard', methods=['GET'])
def dashboard():
    """
    Example protected endpoint for logged-in users.
    """
    if 'user_id' not in session:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    return jsonify({
        "status": "success",
        "message": f"Welcome, {session['username']}!",
        "role": session['role']
    }), 200


# User management endpoints
@app.route('/create_user', methods=['POST'])
def create_user_endpoint():
    """
    Endpoint for creating a new user.

    Input JSON:
        {
            "username": "new_user",
            "password": "password123",
            "role": "User"
        }

    Returns:
        JSON with status and message.
    """
    # Role check: only Admin can create new users
    has_permission, message = check_permissions("Admin")
    if not has_permission:
        return jsonify({"status": "error", "message": message}), 403

    data = request.json
    if not data or "username" not in data or "password" not in data or "role" not in data:
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    username = data['username']
    password = data['password']
    role = data['role']

    message = create_user(username, password, role)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 201


@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user_endpoint(user_id):
    """
    Endpoint for deleting a user.

    Args:
        user_id (int): User ID to delete.

    Returns:
        JSON with status and message.
    """
    # Role check: only Admin can delete users
    has_permission, message = check_permissions("Admin")
    if not has_permission:
        return jsonify({"status": "error", "message": message}), 403

    message = delete_user(user_id)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 200

@app.route('/update_user/<int:user_id>', methods=['PUT'])
def update_user_endpoint(user_id):
    """
    Endpoint for updating a user's details.

    Input JSON:
        {
            "username": "updated_user",
            "password": "new_password"
        }

    Args:
        user_id (int): User ID to update.

    Returns:
        JSON with status and message.
    """
    # Role check: Admins can update any user, Users can update themselves
    if 'user_id' not in session or (session['role'] != "Admin" and session['user_id'] != user_id):
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "Missing data to update"}), 400

    message = update_user(user_id, data)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 200

@app.route('/get_user_details/<int:user_id>', methods=['GET'])
def get_user_details_endpoint(user_id):
    """
    Endpoint for retrieving user details.

    Args:
        user_id (int): User ID.

    Returns:
        JSON with status and user details.
    """
    # Role check: Admins can retrieve any user details, Users can retrieve their own
    if 'user_id' not in session or (session['role'] != "Admin" and session['user_id'] != user_id):
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    user_details = get_user_details(user_id)
    if user_details["status"] == "error":
        return jsonify(user_details), 404
    return jsonify(user_details), 200

@app.route('/assign_role/<int:user_id>', methods=['PUT'])
def assign_role_endpoint(user_id):
    """
    Endpoint for assigning a role to a user.

    Input JSON:
        {
            "role": "Admin"
        }

    Args:
        user_id (int): User ID.

    Returns:
        JSON with status and message.
    """
    # Role check: only Admin can assign roles
    has_permission, message = check_permissions("Admin")
    if not has_permission:
        return jsonify({"status": "error", "message": message}), 403

    data = request.json
    if not data or "role" not in data:
        return jsonify({"status": "error", "message": "Missing role"}), 400

    role = data['role']
    message = assign_role(user_id, role)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 200


@app.route('/change_role/<int:user_id>', methods=['PUT'])
def change_role_endpoint(user_id):
    """
    Endpoint for changing a user's role.

    Input JSON:
        {
            "new_role": "User"
        }

    Args:
        user_id (int): User ID.

    Returns:
        JSON with status and message.
    """
    # Role check: only Admin can change roles
    has_permission, message = check_permissions("Admin")
    if not has_permission:
        return jsonify({"status": "error", "message": message}), 403

    data = request.json
    if not data or "new_role" not in data:
        return jsonify({"status": "error", "message": "Missing new role"}), 400

    new_role = data['new_role']
    message = change_role(user_id, new_role)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 200



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

# Alumni Management Endpoints

@app.route('/add_alumni', methods=['POST'])
def add_alumni_endpoint():
    data = request.json
    if not data or not all(k in data for k in ['first_name', 'last_name', 'address', 'phone', 'graduation_year', 'user_id']):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    message = add_alumni(data)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 201

@app.route('/get_alumni/<int:alumni_id>', methods=['GET'])
def get_alumni_endpoint(alumni_id):
    alumni_details = get_alumni(alumni_id)
    if alumni_details["status"] == "error":
        return jsonify(alumni_details), 404
    return jsonify(alumni_details), 200

@app.route('/update_alumni/<int:alumni_id>', methods=['PUT'])
def update_alumni_endpoint(alumni_id):
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "Missing data to update"}), 400

    message = update_alumni(alumni_id, data)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 200

@app.route('/delete_alumni/<int:alumni_id>', methods=['DELETE'])
def delete_alumni_endpoint(alumni_id):
    message = delete_alumni(alumni_id)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 200

@app.route('/find_alumni_by_name', methods=['GET'])
def find_alumni_by_name_endpoint():
    name = request.args.get('name')
    if not name:
        return jsonify({"status": "error", "message": "Missing name parameter"}), 400

    alumni_list = find_alumni_by_name(name)
    return jsonify(alumni_list), 200

@app.route('/get_alumni_by_graduation_year/<int:year>', methods=['GET'])
def get_alumni_by_graduation_year_endpoint(year):
    alumni_list = get_alumni_by_graduation_year(year)
    return jsonify(alumni_list), 200

@app.route('/list_alumni', methods=['GET'])
def list_alumni_endpoint():
    alumni_list = list_alumni()
    return jsonify(alumni_list), 200

@app.route('/update_alumni_career_history/<int:alumni_id>', methods=['POST'])
def update_alumni_career_history_endpoint(alumni_id):
    career_data = request.json
    if not career_data or not all(k in career_data for k in ['job_title', 'company', 'start_date']):
        return jsonify({"status": "error", "message": "Missing required career fields"}), 400

    message = update_alumni_career_history(alumni_id, career_data)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 201

@app.route('/get_alumni_donations/<int:alumni_id>', methods=['GET'])
def get_alumni_donations_endpoint(alumni_id):
    donations = get_alumni_donations(alumni_id)
    if donations["status"] == "error":
        return jsonify(donations), 404
    return jsonify(donations), 200

@app.route('/get_alumni_achievements/<int:alumni_id>', methods=['GET'])
def get_alumni_achievements_endpoint(alumni_id):
    achievements = get_alumni_achievements(alumni_id)
    if achievements["status"] == "error":
        return jsonify(achievements), 404
    return jsonify(achievements), 200




if __name__ == "__main__":
    app.run(debug=True, port=5000)
