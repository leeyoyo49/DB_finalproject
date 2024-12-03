# this is the terminal user interface for the client (alumni management system)
# it is a simple command line interface that allows the user to interact with the server
# and perform various operations such as adding, deleting, updating, and searching for alumni

import requests
import sys

BASE_URL = "http://localhost:5000"

#global variable to store the user's role
role = None
user_id = None
user_name = None
alumni_id = None

def display_main_menu():
    """Display the main menu."""
    print("\n=== University Alumni Tracking System ===")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    print("=========================================")
    
def register():
    """Register a new user."""
    print("\n=== Register ===")
    username = input("Enter username: ")
    password = input("Enter password: ")
    role = input("Enter role (User/Admin/Analyst): ")
    data = {"username": username, "password": password, "role": role}
    response = requests.post(f"{BASE_URL}/register", json=data)
    print(response.json()["message"])
    
def login():
    """Login to the system."""
    print("\n=== Login ===")
    username = input("Enter username: ")
    password = input("Enter password: ")
    data = {"username": username, "password": password}
    response = requests.post(f"{BASE_URL}/login", json=data)
    if response.status_code == 200:
        print(response.json()["message"])
        return response.json().get("role")
    else:
        print(f"Login failed: {response.json().get('message')}")
        return None
    
def alumni_operations():
    """Alumni-specific operations."""
    # Let the user choose an operation
    action = input()
    
    if input == 'add_career':
        print("Enter the following information to add a career:")
        job_title = input("Enter job title: ")
        company = input("Enter company: ")
        start_date = input("Enter start date (YYYY-MM-YY): ")
        end_date = input("Enter end date (YYYY-MM-YY): ")
        monthy_salary = input("Enter monthly salary (NTD, please enter a number): ")
        Job_Description = input("Enter job description: ")
        
    
def admin_operations():
    """Admin-specific operations."""
    print("\nAdmin operations can be implemented here.")
    
def analyst_operations():
    """Analyst-specific operations."""
    print("\nAnalyst operations can be implemented here.")
    
def main():
    while True:
        display_main_menu()
        choice = input("Type 1 for register, 2 for login, or 3 for exit: ")
        if choice == "1":
            register()
        elif choice == "2":
            role = login()
            if role == "User":
                alumni_operations()
            elif role == "Admin":
                admin_operations()
            elif role == "Analyst":
                analyst_operations()
        elif choice == "3":
            print("Exiting...")
            sys.exit()