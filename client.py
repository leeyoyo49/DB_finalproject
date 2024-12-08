# this is the terminal user interface for the client (alumni management system)
# it is a simple command line interface that allows the user to interact with the server
# and perform various operations such as adding, deleting, updating, and searching for alumni

import requests
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
    
def alumni_operations():
    global ROLE, USER_ID, USER_NAME, ALUMNI_ID
    """Alumni-specific operations."""
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
        endpoint = f"{BASE_URL}/get_user_details/{USER_ID}"
        # Make the request - let the browser handle the session cookies automatically
        response = requests.get(endpoint, cookies=requests.cookies.get_dict())  # The browser will handle session cookies automatically
        print(response.json())
    # Let the user choose an operation  
    
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