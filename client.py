# this is the terminal user interface for the client (alumni management system)
# it is a simple command line interface that allows the user to interact with the server
# and perform various operations such as adding, deleting, updating, and searching for alumni

import requests
import json
import sys

BASE_URL = "http://localhost:5001"

#global variable to store the user's role
ROLE = None
USER_ID = None
USER_NAME = None
ALUMNI_ID = None

def display_main_menu():
    global ROLE, USER_ID, USER_NAME, ALUMNI_ID
    """Display the main menu."""
    print("\n=== University Alumni Tracking System ===")
    print("1. Login as Alumni")
    print("2. Login as Admin")
    print("3. Login as Analyst")
    print("4. Exit")
    print("=========================================")
    
def register():
    global ROLE, USER_ID, USER_NAME, ALUMNI_ID
    """Register a new user."""
    print("\n=== Register ===")
    username = input("Enter username: ")
    password = input("Enter password: ")
    role = input("Enter role (Alumni/Admin/Analyst): ")
    data = {"user_name": username, "password": password, "role": role}
    response = requests.post(f"{BASE_URL}/create_user", json=data)
    print(response.json())
    print()
    
def login():
    """Login to the system."""
    global ROLE, USER_ID, USER_NAME, ALUMNI_ID
    print("\n=== Login ===")
    
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    data = {"username": username, "password": password}
    
    try:
        response = requests.post(f"{BASE_URL}/login", json=data)
        
        if response.status_code == 200:
            print(response.json()["message"])  # 打印成功訊息
            return response.json().get("role"), response.json().get("user_id"), response.json().get("username")
        
        else:
            print(f"Login failed: {response.json().get('message')}")
            return -1, -1, -1
    
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return -1, -1, -1
    
def get_alumni(alumni_id):
    """
    Fetches alumni details from the server.

    Args:
        alumni_id (string): ID of the alumni to retrieve.

    Returns:
        dict: The response JSON containing alumni details or error message.
    """
    try:
        # Construct the request URL
        url = f"{BASE_URL}/get_alumni/{alumni_id}"
        
        # Send a GET request to the server
        response = requests.get(url)
        
        # Check the status code and handle response
        if response.status_code == 200:
            print("Alumni details retrieved successfully:")
            return response.json()
        elif response.status_code == 404:
            print("Alumni not found.")
            return response.json()
        else:
            print(f"Unexpected error occurred. Status code: {response.status_code}")
            return {"status": "error", "message": "Unexpected error occurred."}
    except requests.RequestException as e:
        # Handle any request exceptions (e.g., network issues)
        print("Error while fetching alumni details:", e)
        return {"status": "error", "message": str(e)}

def get_career(alumni_id):
    """
    Fetches alumni career path from the server.

    Args:
        alumni_id (string): ID of the alumni to retrieve.

    Returns:
        dict: The response JSON containing alumni career details or error message.
    """
    try:
        # Construct the request URL
        url = f"{BASE_URL}/get_career_paths/{alumni_id}"
        
        
        # Send a GET request to the server
        response = requests.get(url)
        
        # Check the status code and handle response
        if response.status_code == 200:
            print("Alumni career path retrieved successfully:")
            return response.json()
        elif response.status_code == 404:
            print("Alumni not found.")
            return response.json()
        else:
            print(f"Unexpected error occurred. Status code: {response.status_code}")
            return {"status": "error", "message": "Unexpected error occurred."}
    except requests.RequestException as e:
        # Handle any request exceptions (e.g., network issues)
        print("Error while fetching alumni career path:", e)
        return {"status": "error", "message": str(e)}

    
def edit_profile(alumni_id):
    """
    Function to edit the alumni profile.
    It sends a PUT request to the server to update alumni details.
    
    Args:
        alumni_id (str): The alumni ID for the profile to update.
    """
    print("\n=== Edit Profile ===")
    print("Enter the information you want to update. Leave blank to skip.")
    
    # Collecting user input for profile fields
    address = input("Enter new address (leave blank to skip): ")
    phone = input("Enter new phone number (leave blank to skip): ")

    # Prepare the data dictionary, only including the fields that were changed
    data = {}
    if address:
        data["address"] = address
    if phone:
        data["phone"] = phone

    # If no fields are provided, inform the user
    if not data:
        print("No changes made. Exiting profile editing.")
        return

    # Send the PUT request to the server
    try:
        response = requests.put(f"{BASE_URL}/update_alumni/{alumni_id}", json=data)
        if response.status_code == 200:
            print("Profile updated successfully!")
        else:
            print(f"Failed to update profile: {response.json()['message']}")
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        
import requests

def get_degree(alumni_id):
    """
    Fetches alumni degree information from the server.

    Args:
        alumni_id (string): ID of the alumni to retrieve.

    Returns:
        dict: The response JSON containing alumni degree details or error message.
    """
    try:
        # Construct the request URL
        url = f"{BASE_URL}/get_degree/{alumni_id}"
        
        # Send a GET request to the server
        response = requests.get(url)
        
        # Check the status code and handle response
        if response.status_code == 200:
            print("Alumni degree details retrieved successfully:")
            return response.json()
        elif response.status_code == 404:
            print("Alumni not found.")
            return response.json()
        else:
            print(f"Unexpected error occurred. Status code: {response.status_code}")
            return {"status": "error", "message": "Unexpected error occurred."}
    except requests.RequestException as e:
        # Handle any request exceptions (e.g., network issues)
        print("Error while fetching alumni degree details:", e)
        return {"status": "error", "message": str(e)}

def add_job(alumni_id):
    """
    Interacts with the server to add a career history record for the given alumni.

    Args:
        alumni_id (str): Alumni ID.
    """
    job_title = input("Enter job title: ")
    company = input("Enter company name: ")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (Optional, YYYY-MM-DD) or press Enter to skip: ")
    monthly_salary = input("Enter monthly salary (Optional, numeric): ")
    job_description = input("Enter job description (Optional): ")

    # Prepare the data
    career_data = {
        "job_title": job_title,
        "company": company,
        "start_date": start_date,
        "end_date": end_date if end_date else None,
        "monthly_salary": int(monthly_salary) if monthly_salary else None,
        "job_description": job_description
    }

    try:
        response = requests.post(f"{BASE_URL}/add_career_history/{alumni_id}", json=career_data)
        if response.status_code == 200:
            print("Career history added successfully.")
        else:
            print(f"Failed to add career history: {response.json()['message']}")
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
    
def alumni_operations():
    global ROLE, USER_ID, USER_NAME, ALUMNI_ID
    """Alumni-specific operations."""
    while True:
        print("\n=== Select the section you want to enter ===")
        print("1. Profile")
        print("2. Career")
        print("3. Achievements")
        print("4. Donation")
        print("5. Alumni Association")
        print("6. Exit")
        print("============================================")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            print("\n=== Profile ===")
            print("1. View Profile")
            print("2. Edit Profile")
            sub_choice = input("Enter your choice: ")

            if sub_choice == "1":
                print("\n=== View Profile ===")
                alumni_details = get_alumni(ALUMNI_ID)
                if alumni_details["status"] == "error":
                    print(f"Error: {alumni_details['message']}")
                else:
                    alumni_info = alumni_details['alumni_details']
                    
                    # 先打印 First Name 和 Last Name
                    if "first_name" in alumni_info:
                        first_name = alumni_info["first_name"]
                        print(f"First Name: {first_name}")
                    
                    if "last_name" in alumni_info:
                        last_name = alumni_info["last_name"]
                        print(f"Last Name: {last_name}")
                    
                    # 打印其他信息
                    for key, value in alumni_info.items():
                        if key not in ["first_name", "last_name", "graduation_year"]:
                            key_print = key.replace('_', ' ').capitalize()
                            if key_print == "Alumni id":
                                key_print = "Alumni ID (User Name)"
                            print(f"{key_print}: {value}")
                degree_details = get_degree(ALUMNI_ID)
                if degree_details["status"] == "error":
                    print(f"Error: {degree_details['message']}")
                # Print the response in a formatted way
                alumni_info = degree_details['degree']
                print("=== Degree Information ===")
                for key, value in alumni_info.items():
                    key_print = key.replace('_', ' ').capitalize()
                    if key_print == "Alumni id" or key_print == "Degree id":
                        continue
                        key_print = "Alumni ID (User Name)"
                    print(f"{key_print}: {value}")
            elif sub_choice == "2":
                print("\n=== Edit Profile ===")
                edit_profile(ALUMNI_ID)

        elif choice == "2":
            print("\n=== Career ===")
            print("1. View Career")
            print("2. Edit Career")
            sub_choice = input("Enter your choice: ")

            if sub_choice == "1":
                print("\n=== View Career ===")
                career_details = get_career(ALUMNI_ID)
                if career_details["status"] == "error":
                    print(f"Error: {career_details['message']}")
                # Print the response in a formatted way
                alumni_info = career_details['career_paths']
                for i in range(len(alumni_info)):
                    print(f"=== Job {i+1} ===")
                    for key, value in alumni_info[i].items():
                        key_print = key.replace('_', ' ').capitalize()
                        if key_print == "Alumni id":
                            continue
                            key_print = "Alumni ID (User Name)"
                        if key_print == "End date":
                            print_later = f"{key_print}: {value if value else 'Present'}"
                            continue
                        print(f"{key_print}: {value}")
                    print(print_later)
      
            elif sub_choice == "2":
                print("\n=== Edit Career ===")
                # 這裡可以實現編輯事業資料功能
                add_job(ALUMNI_ID)
                print("Edit Career functionality is under construction.")

        elif choice == "3":
            print("\n=== Achievements ===")
            print("Achievements functionality is under construction.")

        elif choice == "4":
            print("\n=== Donation ===")
            print("Donation functionality is under construction.")

        elif choice == "5":
            print("\n=== Alumni Association ===")
            print("Alumni Association functionality is under construction.")

        elif choice == "6":
            print("Exiting alumni operations.")
            break  # 退出循環，結束操作

        else:
            print("Invalid choice, please try again.")
    
def admin_operations():
    global ROLE, USER_ID, USER_NAME, ALUMNI_ID
    """Admin-specific operations."""
    print("\nAdmin operations can be implemented here.")
    
def analyst_operations():
    global ROLE, USER_ID, USER_NAME, ALUMNI_ID
    """Analyst-specific operations."""
    print("\nAnalyst operations can be implemented here.")
    
def main():
    """
    Main function to manage user login and role-specific operations.
    """
    global ROLE, USER_ID, USER_NAME, ALUMNI_ID

    while True:
        # Display the main menu
        display_main_menu()
        
        # Prompt the user to select an option
        choice = input("Login as (1: Alumni, 2: Admin, 3: Analyst, 0: Exit): ").strip()
        
        if choice == "1":  # Alumni login
            role, user_id, user_name = login()
            if role == -1:  # Login failed
                print("Invalid credentials. Please try again.")
                continue
            elif role == "Alumni":  # Valid Alumni login
                print("Login successful.")
                ROLE = role
                USER_ID = user_id
                USER_NAME = user_name
                ALUMNI_ID = user_name
                alumni_operations()
            else:  # Incorrect role for this option
                print("Invalid role. Please try again.")
                continue

        elif choice == "2":  # Admin login
            role, user_id, user_name = login()
            if role == -1:  # Login failed
                print("Invalid credentials. Please try again.")
                continue
            elif role == "Admin":  # Valid Admin login
                print("Login successful.")
                ROLE = role
                USER_ID = user_id
                USER_NAME = user_name
                admin_operations()
            else:  # Incorrect role for this option
                print("Invalid role. Please try again.")
                continue

        elif choice == "3":  # Analyst login
            role, user_id, user_name = login()
            if role == -1:  # Login failed
                print("Invalid credentials. Please try again.")
                continue
            elif role == "Analyst":  # Valid Analyst login
                print("Login successful.")
                ROLE = role
                USER_ID = user_id
                USER_NAME = user_name
                analyst_operations()
            else:  # Incorrect role for this option
                print("Invalid role. Please try again.")
                continue

        elif choice == "0":  # Exit the program
            print("Exiting the program. Goodbye!")
            break

        else:  # Handle invalid input
            print("Invalid choice. Please select a valid option.")
            continue

if __name__ == "__main__":
    main()