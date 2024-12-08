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
    global ROLE, USER_ID, USER, ALUMNI_ID
    """Display the main menu."""
    print("\n=== University Alumni Tracking System ===")
    print("1. Login as Alumni")
    print("2. Login as Admin")
    print("3. Login as Analyst")
    print("4. Exit")
    print("=========================================")
    
def register():
    global ROLE, USER_ID, USER, ALUMNI_ID
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
    global ROLE, USER_ID, USER, ALUMNI_ID
    print("\n=== Login ===")
    username = input("Enter username: ")
    password = input("Enter password: ")
    data = {"username": username, "password": password}
    response = requests.post(f"{BASE_URL}/login", json=data)
    if response.status_code == 200:
        print(response.json()["message"])
        return response.json().get("role"), response.json().get("user_id"), response.json().get("username")
    else:
        print(f"Login failed: {response.json().get('message')}")
        return -1, -1, -1
    
def alumni_operations():
    global ROLE, USER_ID, USER, ALUMNI_ID
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
    global ROLE, USER_ID, USER, ALUMNI_ID
    """Admin-specific operations."""
    print("\nAdmin operations can be implemented here.")
    
def analyst_operations():
    global ROLE, USER_ID, USER, ALUMNI_ID
    """Analyst-specific operations."""
    print("\nAnalyst operations can be implemented here.")
    
def main():
    global ROLE, USER_ID, USER, ALUMNI_ID
    while True:
        display_main_menu()
        choice = input("Loggin as: ")
        if choice == "1":
            role, user_id, user_name = login()
            if role == -1:
                print("Invalid credentials. Please try again.")
                continue
            else:
                if role == "Alumni":
                    print("Login successful.")
                    ROLE = role
                    USER_ID = user_id
                    USER_NAME = user_name
                    alumni_operations()
                else:
                    print("Invalid role. Please try again.")
                    continue
        elif choice == "2":
            role, user_id, user_name = login()
            if role == -1:
                print("Invalid credentials. Please try again.")
                continue
            else:
                if role == "Admin":
                    print("Login successful.")
                    ROLE = role
                    USER_ID = user_id
                    USER_NAME = user_name
                    admin_operations()
                else:
                    print("Invalid role. Please try again.")
                    continue
        elif choice == "3":
            role, user_id, user_name = login()
            if role == -1:
                print("Invalid credentials. Please try again.")
                continue
            else:
                if role == "Analyst":
                    print("Login successful.")
                    ROLE = role
                    USER_ID = user_id
                    USER_NAME = user_name
                    analyst_operations()
                else:
                    print("Invalid role. Please try again.")
                    continue

if __name__ == "__main__":
    main()