from flask import Flask, jsonify, request, session
from db_connection import connect_to_db, query

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for session management

# Establish database connection
con = connect_to_db()

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

    try:
        # Fetch user from database
        sql_query = f"SELECT id, username, password, role FROM users WHERE username = '{username}'"
        columns, results = query(con, sql_query)

        if not results:
            return jsonify({"status": "error", "message": "Invalid username or password"}), 401

        user = results[0]  # Assuming username is unique
        user_id, db_username, db_password, role = user

        # Validate password (in a real-world application, use hashed passwords)
        if password != db_password:
            return jsonify({"status": "error", "message": "Invalid username or password"}), 401

        # Store user details in session
        session['user_id'] = user_id
        session['username'] = db_username
        session['role'] = role

        return jsonify({"status": "success", "message": "Login successful"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


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

if __name__ == "__main__":
    app.run(debug=True, port=5000)
