from flask import Flask, request, jsonify
from HelpFunctions import *

# 初始化 Flask 應用
app = Flask(__name__)

# 模擬的用戶登入狀態
logged_in_users = {}


def check_permissions(username, required_role):
    """
    Checks if the specified user has the required role to access an endpoint.

    Args:
        username (str): The username of the user attempting to access the endpoint.
        required_role (str): The role required to access the endpoint (e.g., "Admin", "User").

    Returns:
        tuple: A tuple containing:
            - (bool): Whether the user has the required permissions.
            - (str): A message indicating the status ("Unauthorized", "Permission denied", or an empty string if successful).
    """
    if username not in logged_in_users:
        return False, "Unauthorized"
    user_role = logged_in_users[username].get("role")
    if required_role == "User":
        return True, ""  # Allow all roles for this endpoint
    if user_role != required_role:
        return False, "Permission denied"
    return True, ""


# === 用戶管理 ===
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
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"status": "error", "message": "缺少用戶名或密碼"}), 400

    user = login_user(username, password)
    if user:
        logged_in_users[username] = {
            "user_id": user["user_id"],
            "role": user["role"]
        }
        print("logged_in_users:", logged_in_users)
        return jsonify({
            "status": "success",
            "user_id": user["user_id"],
            "username": username,
            "role": user["role"],
            "message": "登入成功"
        }), 200

    return jsonify({"status": "error", "message": "用戶名或密碼錯誤"}), 401

@app.route('/logout', methods=['POST'])
def logout():
    """
    Endpoint for user logout.

    Input JSON:
        {
            "username": "b11705022",
        }

    Return JSON:
        {
            "status": "success",
            "message": "登出成功"
        }
        or
        {
            "status": "error",
            "message": "用戶名或密碼錯誤"
        }
    """
    data = request.json
    username = data.get("username")
    if username not in logged_in_users:
        return jsonify({"status": "error", "message": f"用戶 {username} 尚未登入"}), 400
    
    # Remove the user from logged_in_users
    del logged_in_users[username]
    return jsonify({"status": "success", "message": "登出成功"}), 200



@app.route('/dashboard', methods=['GET'])
def dashboard():
    """
    Endpoint for the dashboard.
    Input JSON:
        {
            "username": "b11705022"
        }
    Return JSON:
        {
            "status": "success",
            "message": "歡迎, b11705022!",
            "role": "Admin"
        }
    """

    data = request.json
    username = data.get("username")
    if username not in logged_in_users:
        return jsonify({"status": "error", "message": f"用戶 {username} 尚未登入"}), 400
    
    user = logged_in_users[username]
    return jsonify({
        "status": "success",
        "message": f"歡迎, {username}!",
        "role": user["role"]
    }), 200


@app.route('/logged_in_users', methods=['GET'])
def get_logged_in_users():
    """
    Endpoint for retrieving the list of logged in users.
    Return JSON:
        {
            "status": "success",
            "logged_in_users": ["b11705022", "b11705023"]
        }
    """
    if logged_in_users:
        return jsonify({"status": "success", "logged_in_users": logged_in_users}), 200

    return jsonify({"status": "success", "message": "目前無用戶登入"}), 200



@app.route('/create_user', methods=['POST'])
def create_user_endpoint():
    """
    創建用戶（僅限 Admin）
    Input JSON:
        {
            "username": "b11705022",
            "password": "admin",
            "role": "Admin",
            "current_user": "b11705023"
        }
    Return JSON:
        {
            "status": "success",
            "message": "用戶 b11705022 創建成功"
        }
    """
    data = request.json
    username = data.get("username")
    if username not in logged_in_users:
        return jsonify({"status": "error", "message": f"用戶 {username} 尚未登入"}), 400
    
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")
    current_user = data.get("current_user")

    if not username or not password or not role:
        return jsonify({"status": "error", "message": "缺少必要欄位"}), 400

    has_permission, message = check_permissions(current_user, "Admin")
    if not has_permission:
        return jsonify({"status": "error", "message": message}), 403

    result_message = create_user(username, password, role)
    if "Error" in result_message:
        return jsonify({"status": "error", "message": result_message}), 500

    return jsonify({"status": "success", "message": result_message}), 201



@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user_endpoint(user_id):
    """
    Endpoint for deleting a user.

    Input JSON:
        {
            "username": "b11705023"
        }

    Args:
        user_id (int): User ID to delete.

    Returns:
        JSON with status and message
    """
    # check if the user is logged in
    data = request.json
    username = data.get("username")
    if username not in logged_in_users:
        return jsonify({"status": "error", "message": f"用戶 {username} 尚未登入"}), 400
    
    # Role check: only Admin can delete users
    data = request.json
    username = data.get("username")
    has_permission, message = check_permissions(username, "Admin")
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
    # check if the user is logged in
    data = request.json
    username = data.get("username")
    if username not in logged_in_users:
        return jsonify({"status": "error", "message": f"用戶 {username} 尚未登入"}), 400
    
    # Role check: only Admin can update users
    has_permission, message = check_permissions(username, "Admin")
    if not has_permission:
        return jsonify({"status": "error", "message": message}), 403
    
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
    # check if the user is logged in
    data = request.json
    username = data.get("username")
    if username not in logged_in_users:
        return jsonify({"status": "error", "message": f"用戶 {username} 尚未登入"}), 400
    
    # Role check: only Admin can view user details
    has_permission, message = check_permissions(username, "Admin")
    if not has_permission:
        return jsonify({"status": "error", "message": message}), 403

    user_details = get_user_details(user_id)
    if user_details["status"] == "error":
        return jsonify(user_details), 404
    return jsonify(user_details), 200

@app.route('/get_degree/<string:alumni_id>', methods=['GET'])
def get_degree_endpoint(alumni_id):
    """
    Retrieves the degree of an alumni.

    Input:
        alumni_id (String): The unique ID of the alumni.
    
    Output:
        JSON with degree details.
    """
    degree = get_degree(alumni_id)
    if degree["status"] == "error":
        return jsonify(degree), 404  # 返回狀態碼404及錯誤信息
    return jsonify(degree), 200  # 返回狀態碼200及學歷詳細信息


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
    # check if the user is logged in
    data = request.json
    username = data.get("username")
    if username not in logged_in_users:
        return jsonify({"status": "error", "message": f"用戶 {username} 尚未登入"}), 400
    
    # Role check: only Admin can assign roles
    has_permission, message = check_permissions(username, "Admin")
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
    # check if the user is logged in
    data = request.json
    username = data.get("username")
    if username not in logged_in_users:
        return jsonify({"status": "error", "message": f"用戶 {username} 尚未登入"}), 400
    
    # Role check: only Admin can change roles
    has_permission, message = check_permissions(username, "Admin")
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
            "sex": "M",
            "address": "123 Main St, City, Country",
            "graduation_year": 2020,   
            "user_id": 1
            "phone": "1234567890",
        }

    Returns:
        JSON with status and message.
    """
    data = request.json
    if not data or not all(k in data for k in ['first_name', 'last_name', 'sex', 'address', 'graduation_year', 'user_id', 'phone']):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    message = add_alumni(data)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 201

@app.route('/get_alumni/<string:alumni_id>', methods=['GET'])
def get_alumni_endpoint(alumni_id):
    """
    Retrieves alumni details.

    Args:
        alumni_id (string): ID of the alumni to retrieve.

    Returns:
        JSON with alumni details.
    """
    alumni_details = get_alumni(alumni_id)
    if alumni_details["status"] == "error":
        return jsonify(alumni_details), 404
    return jsonify(alumni_details), 200

@app.route('/update_alumni/<string:alumni_id>', methods=['PUT'])
def update_alumni_endpoint(alumni_id):
    """
    Updates an alumni record.

    Input JSON:
        {
            "address": "456 Elm St, City, Country",
            "phone": "0987654321"
        }

    Args:
        alumni_id (int): ID of the alumni to update.

    Returns:
        JSON with status and message.
    """
    data = request.json
    print(data)
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


@app.route('/list_alumni', methods=['GET'])
def list_alumni_endpoint():
    """
    Lists all alumni.

    Returns:
        JSON with list of all alumni.
    """
    alumni_list = list_alumni()
    return jsonify(alumni_list), 200


@app.route('/get_alumni_donations/<string:alumni_id>', methods=['GET'])
def get_alumni_donations_endpoint(alumni_id):
    """
    Retrieves donations made by an alumni.

    Args:
        alumni_id (int): ID of the alumni.

    Returns:
        JSON with list of donations made by the alumni.
    """
    # print(alumni_id)
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
@app.route('/add_career_history/<string:alumni_id>', methods=['POST'])
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
            "job_description": "Developed software applications."  # Optional
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
@app.route('/get_career_paths/<string:alumni_id>', methods=['GET'])
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

@app.route('/record_donation/<string:alumni_id>', methods=['POST'])
def record_donation_endpoint(alumni_id):
    """
    Records a donation for an alumni.

    Input JSON:
        {
            "amount": 1000,
            "date": "2024-10-20",
            "donation_type": 'Regular'
        }

    Args:
        alumni_id (string): ID of the alumni making the donation.

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
            "donation_type": 'Regular'
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

@app.route('/get_donation/<string:donation_id>', methods=['GET'])
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

@app.route('/add_achievement/<string:alumni_id>', methods=['POST'])
def add_achievement_endpoint(alumni_id):
    """
    Adds an achievement for an alumni.

    Input JSON:
        {
            "title": "Best Research Paper",
            "description": "Awarded for publishing the best research paper of the year.",
            "date": "2024-10-15",
            "category": "Academic"
            "alumnileader_id": "B11705048"
        }


    Returns:
        JSON with status and message.
    """
    achievement_data = request.json
    if not achievement_data or not all(k in achievement_data for k in ['title', 'description', 'date', 'category']):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    message = add_achievement(achievement_data)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 201

@app.route('/update_achievement', methods=['PUT'])
def update_achievement_endpoint():
    """
    Updates an achievement record.

    Input JSON:
        {
            "title": "Outstanding Research Contribution", // pk
            "date": "2024-11-01"  //pk
            'alumnileader_id': "B11705048" //pk
            'category': "Academic" //optional
            "description": "Awarded for outstanding research contribution." //optional
        }

    Args:
        achievement_id (int): ID of the achievement to update.

    Returns:
        JSON with status and message.
    """
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "Missing data to update"}), 400

    message = update_achievement(data)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 200

@app.route('/delete_achievement', methods=['DELETE'])
def delete_achievement_endpoint(achievement_id):
    """
    Deletes an achievement record.

    Args:
    Input JSON:
        {
            "title": "Outstanding Research Contribution", // pk
            "date": "2024-11-01"  //pk
            'alumnileader_id': "B11705048" //pk
        }
    Returns:
        JSON with status and message.
    """
    data = request.json
    message = delete_achievement(data)
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
            "associaiton_name": "Alumni Association",
            "address": "No. 123, ZhonZheng Rd., Daan District, Taipei City 106, Taiwan",
            "phone": "0123456789",
            "email": "a@gmail.cmo",
            "founded_year": 2020,
            "description": "An association for alumni to network.",
        }

    Returns:
        JSON with status and message.
    """

    data = request.json
    if not data or not all(k in data for k in ['association_name', 'address', 'phone', 'email', 'founded_year', 'description']):
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
            "association_name": "New Alumni Association",
            "address": "456 Elm St, City, Country",
            "phone": "0987654321",
            "email": ""
            "founded_year": 2021,
            "description": "An association for alumni to network and collaborate."
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

@app.route('/add_member_to_association/<int:association_id>/<string:alumni_id>', methods=['POST'])
def add_member_to_association_endpoint(association_id, alumni_id):
    """
    Adds a member to an association.

    Args:
        alumni_id (int): Alumni ID.
        association_id (int): Association ID.
    
    JSON:
        {
            "join_date": '2024-10-15',
        }

    Returns:
        JSON with status and message.
    """
    message = add_member_to_association(alumni_id, association_id)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 201

@app.route('/remove_member_from_association/<int:association_id>/<string:alumni_id>', methods=['DELETE'])
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

@app.route('/get_association_members/<int:association_id>', methods=['GET'])
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
            "event_name": 1,
            "date": "2024-05-15",
            'description': "Annual networking event.",
            'location': "123 Main St, City, Country"    
        }

    Args:
        association_id (int): ID of the association hosting the event.

    Returns:
        JSON with status and message.
    """
    event_data = request.json
    if not event_data or not all(k in event_data for k in ['event_name', 'date']):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    message = create_event(association_id, event_data)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 201

@app.route('/update_event', methods=['PUT'])
def update_event_endpoint():
    """
    Updates an event record, can only change the description and location.
    Since the event name and date are unique, they cannot be changed.

    Input JSON:
        {
            "event_name": 1,
            "date": "2024-05-15",
            'description': "Annual networking event.",
            'location': "123 Main St, City, Country"    
        }

    Args:
        association (int): ID of the association to update.

    Returns:
        JSON with status and message.
    """
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "Missing data to update"}), 400

    message = update_event(data)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 200

@app.route('/delete_event', methods=['DELETE'])
def delete_event_endpoint():
    """
    Deletes an event.

    JSON:
        {
            "event_name": 1,
            "date": "2024-05-15",
        }
    Returns:
        JSON with status and message.
    """
    data = request.json
    message = delete_event(data)
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
# @app.route('/get_alumni_employment_trends', methods=['GET'])
# def get_alumni_employment_trends_endpoint():
#     """
#     Retrieves alumni employment trends for a specific department over a year range.

#     Query Parameters:
#         - department (str): Department name (e.g., "Computer Science").
#         - start_year (int): Start year (e.g., "2010").
#         - end_year (int): End year (e.g., "2020").

#     Example URL:
#         /get_alumni_employment_trends?department=Computer%20Science&start_year=2010&end_year=2020

#     Returns:
#         JSON with employment trends data.
#     """
#     department = request.args.get('department')
#     start_year = request.args.get('start_year', type=int)
#     end_year = request.args.get('end_year', type=int)

#     if not department or not start_year or not end_year:
#         return jsonify({"status": "error", "message": "Missing required parameters"}), 400

#     trends = get_alumni_employment_trends(department, (start_year, end_year))
#     return jsonify(trends), 200


# @app.route('/calculate_donation_correlations', methods=['GET'])
# def calculate_donation_correlations_endpoint():
#     """
#     Calculates correlations between alumni demographics and donation amounts.

#     Returns:
#         JSON with donation correlations.
#     """
#     correlations = calculate_donation_correlations()
#     return jsonify(correlations), 200

# @app.route('/generate_30_year_reunion_list', methods=['GET'])
# def generate_30_year_reunion_list_endpoint():
#     """
#     Generates a list of alumni who graduated 30 years ago.

#     Returns:
#         JSON with reunion list.
#     """
#     reunion_list = generate_30_year_reunion_list()
#     return jsonify(reunion_list), 200


# @app.route('/get_top_achievers', methods=['GET'])
# def get_top_achievers_endpoint():
#     """
#     Retrieves the top achievers.

#     Query Parameters:
#         - limit (int): Number of top achievers to retrieve (e.g., 5).

#     Example URL:
#         /get_top_achievers?limit=5

#     Returns:
#         JSON with list of top achievers.
#     """
#     limit = request.args.get('limit', default=10, type=int)
#     top_achievers = get_top_achievers(limit)
#     return jsonify(top_achievers), 200


# Event Participation Endpoints
@app.route('/add_event_participant', methods=['POST'])
def add_event_participant_endpoint():
    """
    Adds a participant to an event.
    JSON:
        {
            "alumni_id": 1,
            "event_name": "Annual Networking Event",
            "date": "2024-05-15"
        }
    Returns:
        JSON with status and message.
    """
    data = request.json
    message = add_event_participant(data)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 201

@app.route('/remove_event_participant', methods=['DELETE'])
def remove_event_participant_endpoint():
    """
    Adds a participant to an event.

    JSON:
        {
            "alumni_id": 1,
            "event_name": "Annual Networking Event",
            "date": "2024-05-15"
        }

    Returns:
        JSON with status and message.
    """
    data = request.json
    message = remove_event_participant(data)
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    return jsonify({"status": "success", "message": message}), 200

@app.route('/list_participants', methods=['GET'])
def list_participants_endpoint(data):
    """
    Lists all participants for a specific event.
    
    JSON:   
        {
            "event_name": 1,
            "date": "2024-05-15",
        }

    Returns:
        JSON with list of participants.
    """
    data = request.json
    participants = list_participants(data)
    if participants["status"] == "error":
        return jsonify(participants), 404
    return jsonify(participants), 200

@app.route('/get_participation_by_alumni/<string:alumni_id>', methods=['GET'])
def get_participation_by_alumni_endpoint(alumni_id):
    """
    Retrieves all events an alumni has participated in.

    URL Parameters:
        alumni_id (string): The ID of the alumni.

    Returns:
        JSON with a list of events or an error message.
    """
    # Call a function to retrieve the events based on alumni_id
    events = get_participation_by_alumni(alumni_id)
    
    if events["status"] == "error":
        return jsonify(events), 404
    
    return jsonify(events), 200

@app.route('/get_association_by_alumni/<string:alumni_id>', methods=['GET'])
def get_association_by_alumni_endpoint(alumni_id):
    """
    Retrieves all associations an alumni has joined.

    URL Parameters:
        alumni_id (string): The ID of the alumni.

    Returns:
        JSON with a list of associations or an error message.
    """
    # Call a function to retrieve the associations based on alumni_id
    associations = list_user_associations(alumni_id)
    
    if associations["status"] == "error":
        return jsonify(associations), 404
    
    return jsonify(associations), 200

@app.route('/get_personal_events/<string:alumni_id>', methods=['GET'])
def get_personal_events_endpoint(alumni_id):
    """
    Retrieves all personal events an alumni has created.

    URL Parameters:
        alumni_id (string): The ID of the alumni.

    Returns:
        JSON with a list of personal events or an error message.
    """
    # Call a function to retrieve the personal events based on alumni_id
    events = list_user_association_events(alumni_id)
    
    if events["status"] == "error":
        return jsonify(events), 404
    
    return jsonify(events), 200

@app.route('/get_all_open_associations', methods=['GET'])
def get_all_associations_endpoint():
    """
    Retrieves all associations.

    Returns:
        JSON with a list of all associations.
    """
    associations = get_all_open_association()
    
    if associations["status"] == "error":
        return jsonify(associations), 404
    return jsonify(associations), 200

@app.route('/get_all_upcoming_events', methods=['GET'])
def get_all_upcoming_events_endpoint():
    """
    Retrieves all upcoming events.

    Returns:
        JSON with a list of all upcoming events.
    """
    events = get_all_upcoming_events()
    
    if events["status"] == "error":
        return jsonify(events), 404
    return jsonify(events), 200

@app.route('/is_association_cadre/<string:alumni_id>', methods=['GET'])
def is_association_cadre_endpoint(alumni_id):
    """
    Checks if an alumni is a cadre of an association.

    URL Parameters:
        alumni_id (string): The ID of the alumni.

    Returns:
        JSON with a message indicating if the alumni is a cadre or not.
    """
    # Call a function to check if the alumni is a cadre
    cadre_status = is_association_cadre(alumni_id)
    
    if cadre_status["status"] == "error":
        return jsonify(cadre_status), 404
    
    return jsonify(cadre_status), 200

@app.route('/end_cadre/<int:association_id>/<string:alumni_id>', methods=['POST'])
def end_cadre_endpoint(association_id, alumni_id):
    """
    Ends the cadre position of an alumni in an association.

    URL Parameters:
        association_id (int): The ID of the association.
        alumni_id (string): The ID of the alumni.

    Returns:
        JSON with a message indicating the result of the operation.
    """
    try:
        # Call a function to end the cadre position
        message = end_cadre(association_id, alumni_id)
        
        if "Error" in message:
            return jsonify({"status": "error", "message": message}), 500
        
        return jsonify({"status": "success", "message": message}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/add_cadre_to_association/<string:alumni_id>/<int:association_id>/<string:pos>', methods=['POST'])
def add_cadre_to_association_endpoint(alumni_id, association_id, pos):
    """
    Adds a cadre to an association.

    URL Parameters:
        alumni_id (string): The ID of the alumni.
        association_id (int): The ID of the association.

    Returns:
        JSON with a message indicating the result of the operation.
    """
    # Call a function to add the cadre to the association
    data = request.json
    message = add_cadre_to_association(data)
    
    if "Error" in message:
        return jsonify({"status": "error", "message": message}), 500
    
    return jsonify({"status": "success", "message": message}), 201


if __name__ == "__main__":
    app.run(debug=True, port=5001)
    
