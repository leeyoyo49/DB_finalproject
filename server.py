from flask import Flask, jsonify, request, session
from db_connection import connect_to_db, query
from HelpFunctions import *

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for session management

# Establish database connection
con = connect_to_db()


# User management endpoints
@app.route('/login', methods=['POST'])
def login():
    """
    Endpoint for user login.

    Input JSON:
        {
            "username": "b11705022",
            "password": "admin"
        }

    Return JSON:
        {
            "status": "success",
            "user_id": 1,
            "username": "b11705022",
            "role": "Admin"
        }
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
        return jsonify({"status": "success","user_id": session['user_id'], "username": session['username'], "role": session['role']}), 200
    return jsonify({"status": "error","user_id":"", "username": "", "role": ""}), 401


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


# Alumni Management Endpoints

@app.route('/add_alumni', methods=['POST'])
def add_alumni_endpoint():
    """
    Adds a new alumni record.

    Input JSON:
        {
            "first_name": "John",
            "last_name": "Doe",
            "address": "123 Main St, City, Country",
            "phone": "1234567890",
            "graduation_year": 2020,
            "user_id": 1
        }

    Returns:
        JSON with status and message.
    """
    data = request.json
    if not data or not all(k in data for k in ['first_name', 'last_name', 'address', 'phone', 'graduation_year', 'user_id']):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    message = add_alumni(data)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 201

@app.route('/get_alumni/<int:alumni_id>', methods=['GET'])
def get_alumni_endpoint(alumni_id):
    """
    Retrieves alumni details.

    Args:
        alumni_id (int): ID of the alumni to retrieve.

    Returns:
        JSON with alumni details.
    """
    alumni_details = get_alumni(alumni_id)
    if alumni_details["status"] == "error":
        return jsonify(alumni_details), 404
    return jsonify(alumni_details), 200

@app.route('/update_alumni/<int:alumni_id>', methods=['PUT'])
def update_alumni_endpoint(alumni_id):
    """
    Updates an alumni record.

    Input JSON:
        {
            "address": "456 Elm St, City, Country",  // Optional fields to update
            "phone": "0987654321"
        }

    Args:
        alumni_id (int): ID of the alumni to update.

    Returns:
        JSON with status and message.
    """
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "Missing data to update"}), 400

    message = update_alumni(alumni_id, data)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 200

@app.route('/delete_alumni/<int:alumni_id>', methods=['DELETE'])
def delete_alumni_endpoint(alumni_id):
    """
    Deletes an alumni record.

    Args:
        alumni_id (int): ID of the alumni to delete.

    Returns:
        JSON with status and message.
    """
    message = delete_alumni(alumni_id)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 200

@app.route('/find_alumni_by_name', methods=['GET'])
def find_alumni_by_name_endpoint():
    """
    Finds alumni by name.

    Query Parameters:
        - name (str): The name to search for (e.g., "John").

    Example URL:
        /find_alumni_by_name?name=John

    Returns:
        JSON with list of alumni that match the name.
    """
    name = request.args.get('name')
    if not name:
        return jsonify({"status": "error", "message": "Missing name parameter"}), 400

    alumni_list = find_alumni_by_name(name)
    return jsonify(alumni_list), 200

@app.route('/get_alumni_by_graduation_year/<int:year>', methods=['GET'])
def get_alumni_by_graduation_year_endpoint(year):
    """
    Retrieves alumni by graduation year.

    Args:
        year (int): Graduation year of alumni to retrieve (e.g., 2020).

    Returns:
        JSON with list of alumni for the specified graduation year.
    """
    alumni_list = get_alumni_by_graduation_year(year)
    return jsonify(alumni_list), 200

@app.route('/list_alumni', methods=['GET'])
def list_alumni_endpoint():
    """
    Lists all alumni.

    Returns:
        JSON with list of all alumni.
    """
    alumni_list = list_alumni()
    return jsonify(alumni_list), 200

@app.route('/update_alumni_career_history/<int:alumni_id>', methods=['POST'])
def update_alumni_career_history_endpoint(alumni_id):
    """
    Updates career history for an alumni.

    Input JSON:
        {
            "job_title": "Software Engineer",
            "company": "Tech Corp",
            "start_date": "2021-01-15",
            "end_date": "2023-06-30"  // Optional
        }

    Args:
        alumni_id (int): ID of the alumni whose career history is being updated.

    Returns:
        JSON with status and message.
    """
    career_data = request.json
    if not career_data or not all(k in career_data for k in ['job_title', 'company', 'start_date']):
        return jsonify({"status": "error", "message": "Missing required career fields"}), 400

    message = update_alumni_career_history(alumni_id, career_data)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 201

@app.route('/get_alumni_donations/<int:alumni_id>', methods=['GET'])
def get_alumni_donations_endpoint(alumni_id):
    """
    Retrieves donations made by an alumni.

    Args:
        alumni_id (int): ID of the alumni.

    Returns:
        JSON with list of donations made by the alumni.
    """
    donations = get_alumni_donations(alumni_id)
    if donations["status"] == "error":
        return jsonify(donations), 404
    return jsonify(donations), 200

@app.route('/get_alumni_achievements/<int:alumni_id>', methods=['GET'])
def get_alumni_achievements_endpoint(alumni_id):
    """
    Retrieves achievements of an alumni.

    Args:
        alumni_id (int): ID of the alumni.

    Returns:
        JSON with list of achievements by the alumni.
    """
    achievements = get_alumni_achievements(alumni_id)
    if achievements["status"] == "error":
        return jsonify(achievements), 404
    return jsonify(achievements), 200


# Career History Management Endpoints
@app.route('/add_career_history/<int:alumni_id>', methods=['POST'])
def add_career_history_endpoint(alumni_id):
    """
    Adds a career history record for an alumni.

    Input JSON:
        {
            "job_title": "Software Engineer",
            "company": "Tech Corp",
            "start_date": "2020-01-15",
            "end_date": "2023-05-30",  # Optional
            "monthly_salary": 5000  # Optional
        }

    Args:
        alumni_id (int): Alumni ID.

    Returns:
        JSON with status and message.
    """
    career_data = request.json
    if not career_data or not all(k in career_data for k in ['job_title', 'company', 'start_date']):
        return jsonify({"status": "error", "message": "Missing required career fields"}), 400

    message = add_career_history(alumni_id, career_data)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 201

@app.route('/update_career_history/<int:career_id>', methods=['PUT'])
def update_career_history_endpoint(career_id):
    """
    Updates a career history record.

    Input JSON:
        {
            "job_title": "Senior Software Engineer",
            "company": "Tech Corp International",
            "end_date": "2024-08-01"  # Optional, if updating the career record
        }

    Args:
        career_id (int): Career History ID.

    Returns:
        JSON with status and message.
    """
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "Missing data to update"}), 400

    message = update_career_history(career_id, data)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 200

@app.route('/delete_career_history/<int:career_id>', methods=['DELETE'])
def delete_career_history_endpoint(career_id):
    """
    Deletes a career history record.

    Args:
        career_id (int): Career History ID to delete.

    Returns:
        JSON with status and message.
    """
    message = delete_career_history(career_id)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 200

@app.route('/get_career_history/<int:career_id>', methods=['GET'])
def get_career_history_endpoint(career_id):
    """
    Retrieves a career history record.

    Args:
        career_id (int): Career History ID.

    Returns:
        JSON with career history details.
    """
    career_details = get_career_history(career_id)
    if career_details["status"] == "error":
        return jsonify(career_details), 404
    return jsonify(career_details), 200

# Career Analysis Endpoints

@app.route('/get_salary_trends', methods=['GET'])
def get_salary_trends_endpoint():
    """
    Retrieves salary trends for a given department over a specific year range.

    Query Parameters:
        - department (str): The name of the department (e.g., "Computer Science").
        - start_year (str): The start year for the range (e.g., "2015").
        - end_year (str): The end year for the range (e.g., "2023").

    Example URL:
        /get_salary_trends?department=Computer%20Science&start_year=2015&end_year=2023

    Returns:
        JSON with salary trends data.
    """
    department = request.args.get('department')
    start_year = request.args.get('start_year')
    end_year = request.args.get('end_year')

    if not department or not start_year or not end_year:
        return jsonify({"status": "error", "message": "Missing required parameters"}), 400

    try:
        year_range = (int(start_year), int(end_year))
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid year format"}), 400

    salary_trends = get_salary_trends(department, year_range)
    return jsonify(salary_trends), 200

@app.route('/get_career_paths/<int:alumni_id>', methods=['GET'])
def get_career_paths_endpoint(alumni_id):
    """
    Retrieves the career paths of an alumni.

    Args:
        alumni_id (int): Alumni ID.

    Returns:
        JSON with career path details.
    """
    career_paths = get_career_paths(alumni_id)
    if career_paths["status"] == "error":
        return jsonify(career_paths), 404
    return jsonify(career_paths), 200

# Donation Management Endpoints

@app.route('/record_donation/<int:alumni_id>', methods=['POST'])
def record_donation_endpoint(alumni_id):
    """
    Records a donation for an alumni.

    Input JSON:
        {
            "amount": 1000,
            "date": "2024-10-20",
            "campaign_id": 1  // Optional
        }

    Args:
        alumni_id (int): ID of the alumni making the donation.

    Returns:
        JSON with status and message.
    """
    donation_data = request.json
    if not donation_data or "amount" not in donation_data or "date" not in donation_data:
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    message = record_donation(alumni_id, donation_data)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 201

@app.route('/update_donation/<int:donation_id>', methods=['PUT'])
def update_donation_endpoint(donation_id):
    """
    Updates a donation record.

    Input JSON:
        {
            "amount": 1500,
            "date": "2024-10-25"
        }

    Args:
        donation_id (int): ID of the donation to update.

    Returns:
        JSON with status and message.
    """
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "Missing data to update"}), 400

    message = update_donation(donation_id, data)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 200

@app.route('/delete_donation/<int:donation_id>', methods=['DELETE'])
def delete_donation_endpoint(donation_id):
    """
    Deletes a donation record.

    Args:
        donation_id (int): ID of the donation to delete.

    Returns:
        JSON with status and message.
    """
    message = delete_donation(donation_id)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 200

@app.route('/get_donation/<int:donation_id>', methods=['GET'])
def get_donation_endpoint(donation_id):
    """
    Retrieves a donation record.

    Args:
        donation_id (int): ID of the donation to retrieve.

    Returns:
        JSON with donation details.
    """
    donation_details = get_donation(donation_id)
    if donation_details["status"] == "error":
        return jsonify(donation_details), 404
    return jsonify(donation_details), 200

# Donation Analysis Endpoints

@app.route('/get_total_donations_by_alumni/<int:alumni_id>', methods=['GET'])
def get_total_donations_by_alumni_endpoint(alumni_id):
    """
    Retrieves the total donations made by an alumni.

    Args:
        alumni_id (int): ID of the alumni.

    Returns:
        JSON with the total donation amount.
    """
    total_donations = get_total_donations_by_alumni(alumni_id)
    if total_donations["status"] == "error":
        return jsonify(total_donations), 404
    return jsonify(total_donations), 200

@app.route('/get_top_donors', methods=['GET'])
def get_top_donors_endpoint():
    """
    Retrieves the top donors.

    Query Parameters:
        - limit (int): The number of top donors to retrieve (e.g., 5).
    
    Example URL:
        /get_top_donors?limit=5

    Returns:
        JSON with list of top donors.
    """
    limit = request.args.get('limit', default=10, type=int)
    top_donors = get_top_donors(limit)
    return jsonify(top_donors), 200

@app.route('/get_donation_trends', methods=['GET'])
def get_donation_trends_endpoint():
    """
    Retrieves donation trends over a specific year range.

    Query Parameters:
        - start_year (int): The start year for the range (e.g., "2020").
        - end_year (int): The end year for the range (e.g., "2024").

    Example URL:
        /get_donation_trends?start_year=2020&end_year=2024

    Returns:
        JSON with donation trends data.
    """
    start_year = request.args.get('start_year', type=int)
    end_year = request.args.get('end_year', type=int)

    if not start_year or not end_year:
        return jsonify({"status": "error", "message": "Missing required year range parameters"}), 400

    donation_trends = get_donation_trends((start_year, end_year))
    return jsonify(donation_trends), 200


# Achievement Management Endpoints

@app.route('/add_achievement/<int:alumni_id>', methods=['POST'])
def add_achievement_endpoint(alumni_id):
    """
    Adds an achievement for an alumni.

    Input JSON:
        {
            "title": "Best Research Paper",
            "description": "Awarded for publishing the best research paper of the year.",
            "date": "2024-10-15",
            "category": "Academic"
        }

    Args:
        alumni_id (int): ID of the alumni receiving the achievement.

    Returns:
        JSON with status and message.
    """
    achievement_data = request.json
    if not achievement_data or not all(k in achievement_data for k in ['title', 'description', 'date', 'category']):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    message = add_achievement(alumni_id, achievement_data)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 201

@app.route('/update_achievement/<int:achievement_id>', methods=['PUT'])
def update_achievement_endpoint(achievement_id):
    """
    Updates an achievement record.

    Input JSON:
        {
            "title": "Outstanding Research Contribution",
            "date": "2024-11-01"  // Optional, fields to be updated
        }

    Args:
        achievement_id (int): ID of the achievement to update.

    Returns:
        JSON with status and message.
    """
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "Missing data to update"}), 400

    message = update_achievement(achievement_id, data)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 200

@app.route('/delete_achievement/<int:achievement_id>', methods=['DELETE'])
def delete_achievement_endpoint(achievement_id):
    """
    Deletes an achievement record.

    Args:
        achievement_id (int): ID of the achievement to delete.

    Returns:
        JSON with status and message.
    """
    message = delete_achievement(achievement_id)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 200

@app.route('/get_achievement/<int:achievement_id>', methods=['GET'])
def get_achievement_endpoint(achievement_id):
    """
    Retrieves an achievement record.

    Args:
        achievement_id (int): ID of the achievement to retrieve.

    Returns:
        JSON with achievement details.
    """
    achievement_details = get_achievement(achievement_id)
    if achievement_details["status"] == "error":
        return jsonify(achievement_details), 404
    return jsonify(achievement_details), 200

@app.route('/list_achievements/<int:alumni_id>', methods=['GET'])
def list_achievements_endpoint(alumni_id):
    """
    Lists all achievements for an alumni.

    Args:
        alumni_id (int): ID of the alumni.

    Returns:
        JSON with list of achievements.
    """
    achievements = list_achievements(alumni_id)
    if achievements["status"] == "error":
        return jsonify(achievements), 404
    return jsonify(achievements), 200

@app.route('/find_achievements_by_category', methods=['GET'])
def find_achievements_by_category_endpoint():
    """
    Finds achievements by category.

    Query Parameters:
        - category (str): Category of achievements to search for (e.g., "Academic").

    Example URL:
        /find_achievements_by_category?category=Academic

    Returns:
        JSON with list of achievements in the specified category.
    """
    category = request.args.get('category')
    if not category:
        return jsonify({"status": "error", "message": "Missing category parameter"}), 400

    achievements = find_achievements_by_category(category)
    return jsonify(achievements), 200

# Association Management Endpoints

@app.route('/create_association', methods=['POST'])
def create_association_endpoint():
    """
    Creates a new association.

    Input JSON:
        {
            "name": "Alumni Association",
            "description": "An association for alumni to network.",
            "created_date": "2024-01-15"
        }

    Returns:
        JSON with status and message.
    """
    data = request.json
    if not data or not all(k in data for k in ['name', 'description', 'created_date']):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    message = create_association(data)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 201

@app.route('/update_association/<int:association_id>', methods=['PUT'])
def update_association_endpoint(association_id):
    """
    Updates an association record.

    Input JSON:
        {
            "name": "Updated Alumni Association",
            "description": "An updated description for alumni to network."
        }

    Args:
        association_id (int): ID of the association to update.

    Returns:
        JSON with status and message.
    """
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "Missing data to update"}), 400

    message = update_association(association_id, data)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 200

@app.route('/delete_association/<int:association_id>', methods=['DELETE'])
def delete_association_endpoint(association_id):
    """
    Deletes an association.

    Args:
        association_id (int): ID of the association to delete.

    Returns:
        JSON with status and message.
    """
    message = delete_association(association_id)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 200

@app.route('/get_association/<int:association_id>', methods=['GET'])
def get_association_endpoint(association_id):
    """
    Retrieves an association record.

    Args:
        association_id (int): ID of the association to retrieve.

    Returns:
        JSON with association details.
    """
    association_details = get_association(association_id)
    if association_details["status"] == "error":
        return jsonify(association_details), 404
    return jsonify(association_details), 200

# Membership Management Endpoints

@app.route('/add_member_to_association/<int:association_id>/<int:alumni_id>', methods=['POST'])
def add_member_to_association_endpoint(association_id, alumni_id):
    """
    Adds a member to an association.

    Args:
        alumni_id (int): Alumni ID.
        association_id (int): Association ID.

    Returns:
        JSON with status and message.
    """
    message = add_member_to_association(alumni_id, association_id)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 201

@app.route('/remove_member_from_association/<int:association_id>/<int:alumni_id>', methods=['DELETE'])
def remove_member_from_association_endpoint(association_id, alumni_id):
    """
    Removes a member from an association.

    Args:
        alumni_id (int): Alumni ID.
        association_id (int): Association ID.

    Returns:
        JSON with status and message.
    """
    message = remove_member_from_association(alumni_id, association_id)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 200

@app.route('/list_association_members/<int:association_id>', methods=['GET'])
def list_association_members_endpoint(association_id):
    """
    Lists all members of an association.

    Args:
        association_id (int): ID of the association.

    Returns:
        JSON with list of members.
    """
    members = list_association_members(association_id)
    if members["status"] == "error":
        return jsonify(members), 404
    return jsonify(members), 200

# Event Management Endpoints

@app.route('/create_event/<int:association_id>', methods=['POST'])
def create_event_endpoint(association_id):
    """
    Creates an event for an association.

    Input JSON:
        {
            "title": "Annual Meetup",
            "description": "A networking event for all alumni members.",
            "event_date": "2024-05-15"
        }

    Args:
        association_id (int): ID of the association hosting the event.

    Returns:
        JSON with status and message.
    """
    event_data = request.json
    if not event_data or not all(k in event_data for k in ['title', 'description', 'event_date']):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    message = create_event(association_id, event_data)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 201

@app.route('/update_event/<int:event_id>', methods=['PUT'])
def update_event_endpoint(event_id):
    """
    Updates an event record.

    Input JSON:
        {
            "title": "Updated Annual Meetup",
            "description": "Updated networking event details."
        }

    Args:
        event_id (int): ID of the event to update.

    Returns:
        JSON with status and message.
    """
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "Missing data to update"}), 400

    message = update_event(event_id, data)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 200

@app.route('/delete_event/<int:event_id>', methods=['DELETE'])
def delete_event_endpoint(event_id):
    """
    Deletes an event.

    Args:
        event_id (int): ID of the event to delete.

    Returns:
        JSON with status and message.
    """
    message = delete_event(event_id)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 200

@app.route('/list_events_by_association/<int:association_id>', methods=['GET'])
def list_events_by_association_endpoint(association_id):
    """
    Lists all events for a specific association.

    Args:
        association_id (int): ID of the association.

    Returns:
        JSON with list of events.
    """
    events = list_events_by_association(association_id)
    if events["status"] == "error":
        return jsonify(events), 404
    return jsonify(events), 200

# Data Analysis Endpoints

@app.route('/get_alumni_employment_trends', methods=['GET'])
def get_alumni_employment_trends_endpoint():
    """
    Retrieves alumni employment trends for a specific department over a year range.

    Query Parameters:
        - department (str): Department name (e.g., "Computer Science").
        - start_year (int): Start year (e.g., "2010").
        - end_year (int): End year (e.g., "2020").

    Example URL:
        /get_alumni_employment_trends?department=Computer%20Science&start_year=2010&end_year=2020

    Returns:
        JSON with employment trends data.
    """
    department = request.args.get('department')
    start_year = request.args.get('start_year', type=int)
    end_year = request.args.get('end_year', type=int)

    if not department or not start_year or not end_year:
        return jsonify({"status": "error", "message": "Missing required parameters"}), 400

    trends = get_alumni_employment_trends(department, (start_year, end_year))
    return jsonify(trends), 200

@app.route('/analyze_event_participation_rates', methods=['GET'])
def analyze_event_participation_rates_endpoint():
    """
    Analyzes participation rates for all events.

    Returns:
        JSON with participation rates.
    """
    participation_rates = analyze_event_participation_rates()
    return jsonify(participation_rates), 200

@app.route('/calculate_donation_correlations', methods=['GET'])
def calculate_donation_correlations_endpoint():
    """
    Calculates correlations between alumni demographics and donation amounts.

    Returns:
        JSON with donation correlations.
    """
    correlations = calculate_donation_correlations()
    return jsonify(correlations), 200

@app.route('/generate_30_year_reunion_list', methods=['GET'])
def generate_30_year_reunion_list_endpoint():
    """
    Generates a list of alumni who graduated 30 years ago.

    Returns:
        JSON with reunion list.
    """
    reunion_list = generate_30_year_reunion_list()
    return jsonify(reunion_list), 200

@app.route('/get_top_achievers', methods=['GET'])
def get_top_achievers_endpoint():
    """
    Retrieves the top achievers.

    Query Parameters:
        - limit (int): Number of top achievers to retrieve (e.g., 5).

    Example URL:
        /get_top_achievers?limit=5

    Returns:
        JSON with list of top achievers.
    """
    limit = request.args.get('limit', default=10, type=int)
    top_achievers = get_top_achievers(limit)
    return jsonify(top_achievers), 200

@app.route('/get_event_participation_statistics/<int:event_id>', methods=['GET'])
def get_event_participation_statistics_endpoint(event_id):
    """
    Retrieves participation statistics for a specific event.

    Args:
        event_id (int): ID of the event.

    Returns:
        JSON with participation statistics.
    """
    participation_stats = get_event_participation_statistics(event_id)
    if participation_stats["status"] == "error":
        return jsonify(participation_stats), 404
    return jsonify(participation_stats), 200


# Event Participation Endpoints

@app.route('/add_event_participant/<int:event_id>/<int:alumni_id>', methods=['POST'])
def add_event_participant_endpoint(event_id, alumni_id):
    """
    Adds a participant to an event.

    Args:
        alumni_id (int): Alumni ID.
        event_id (int): Event ID.

    Returns:
        JSON with status and message.
    """
    message = add_event_participant(alumni_id, event_id)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 201

@app.route('/remove_event_participant/<int:event_id>/<int:alumni_id>', methods=['DELETE'])
def remove_event_participant_endpoint(event_id, alumni_id):
    """
    Removes a participant from an event.

    Args:
        alumni_id (int): Alumni ID.
        event_id (int): Event ID.

    Returns:
        JSON with status and message.
    """
    message = remove_event_participant(alumni_id, event_id)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 200

@app.route('/list_participants/<int:event_id>', methods=['GET'])
def list_participants_endpoint(event_id):
    """
    Lists all participants for a specific event.

    Args:
        event_id (int): Event ID.

    Returns:
        JSON with list of participants.
    """
    participants = list_participants(event_id)
    if participants["status"] == "error":
        return jsonify(participants), 404
    return jsonify(participants), 200

@app.route('/get_participation_by_alumni/<int:alumni_id>', methods=['GET'])
def get_participation_by_alumni_endpoint(alumni_id):
    """
    Retrieves all events an alumni has participated in.

    Args:
        alumni_id (int): Alumni ID.

    Returns:
        JSON with list of events.
    """
    events = get_participation_by_alumni(alumni_id)
    if events["status"] == "error":
        return jsonify(events), 404
    return jsonify(events), 200




if __name__ == "__main__":
    app.run(debug=True, port=5000)