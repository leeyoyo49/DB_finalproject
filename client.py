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
                # 這裡可以實現查看事業資料功能
                print("View Career functionality is under construction.")
            
            elif sub_choice == "2":
                print("\n=== Edit Career ===")
                # 這裡可以實現編輯事業資料功能
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

def insert_donation(alumni_id: str, amount: int, date: str, campaign_id = "Regular") -> bool:
    """
    insert the donation records to the server.

    Args:
        alumni_id (string): ID of the alumni.

    Returns:
        JSON with status and message.
    """
    data = {
        "amount": amount,
        "date": date,
        "donation_type": campaign_id    
    }
    try:
        url = f"{BASE_URL}/record_donation/{alumni_id}"
        response = requests.post(url, json=data)
        if response.status_code == 201:
            print("Success")
            return True
        elif response.status_code == 500:
            print("Error")
            return False
        else:
            print(f"Unexpected error occurred. Status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        print("Error while fetching alumni details:", e)
        return False
        
def update_donation(donation_id: int, amount: int, date: str) -> bool:
    """
    Update a donation record on the server.

    Args:
        donation_id (int): ID of the donation to update.
        amount (int): The new donation amount.
        date (str): The new donation date in 'YYYY-MM-DD' format.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    data = {
        "amount": amount,
        "date": date
    }
    try:
        url = f"{BASE_URL}/update_donation/{donation_id}"
        response = requests.put(url, json=data)
        
        if response.status_code == 200:
            print("Update successful.")
            return True
        elif response.status_code == 400:
            print("Error: Invalid or missing data.")
            return False
        elif response.status_code == 500:
            print("Server error occurred while updating the donation.")
            return False
        else:
            print(f"Unexpected error occurred. Status code: {response.status_code}")
            return False

    except requests.RequestException as e:
        print("Error while updating donation details:", e)
        return False

def delete_donation(donation_id: int) -> bool:
    """
    Deletes a donation record on the server.

    Args:
        donation_id (int): ID of the donation to delete.

    Returns:
        bool: True if the deletion was successful, False otherwise.
    """
    try:
        url = f"{BASE_URL}/delete_donation/{donation_id}"
        response = requests.delete(url)
        
        if response.status_code == 200:
            print("Donation deleted successfully.")
            return True
        elif response.status_code == 404:
            print("Error: Donation not found.")
            return False
        elif response.status_code == 500:
            print("Server error occurred while deleting the donation.")
            return False
        else:
            print(f"Unexpected error occurred. Status code: {response.status_code}")
            return False

    except requests.RequestException as e:
        print("Error while deleting donation:", e)
        return False

def get_donation(donation_id: str) -> dict:
    """
    Retrieves a donation record from the server.

    Args:
        donation_id (int): ID of the donation to retrieve.

    Returns:
        dict: A dictionary containing donation details or error message.
    """
    try:
        url = f"{BASE_URL}/get_donation/{donation_id}"
        response = requests.get(url)
        
        if response.status_code == 200:
            # 如果請求成功，返回捐款資料
            return response.json()
        elif response.status_code == 404:
            # 找不到捐款紀錄時
            print("Donation not found.")
            return {"status": "error", "message": "Donation not found"}
        else:
            # 處理其他錯誤
            print(f"Unexpected error occurred. Status code: {response.status_code}")
            return {"status": "error", "message": f"Unexpected error occurred. Status code: {response.status_code}"}
    
    except requests.RequestException as e:
        print(f"Error while fetching donation details: {e}")
        return {"status": "error", "message": str(e)}

def add_achievement(alumni_id: str, title: str, description: str, date: str, category: str) -> bool:
    """
    Adds an achievement for the specified alumni.

    Args:
        alumni_id (int): ID of the alumni receiving the achievement.
        title (str): The title of the achievement.
        description (str): A description of the achievement.
        date (str): The date of the achievement in 'YYYY-MM-DD' format.
        category (str): The category of the achievement (e.g., 'Academic').

    Returns:
        bool: True if the achievement was added successfully, False otherwise.
    """
    data = {
        "title": title,
        "description": description,
        "date": date,
        "category": category
    }
    
    try:
        url = f"{BASE_URL}/add_achievement/{alumni_id}"
        response = requests.post(url, json=data)
        
        if response.status_code == 201:
            print("Achievement added successfully.")
            return True
        elif response.status_code == 400:
            print("Error: Missing required fields.")
            return False
        elif response.status_code == 500:
            print("Server error occurred while adding the achievement.")
            return False
        else:
            print(f"Unexpected error occurred. Status code: {response.status_code}")
            return False

    except requests.RequestException as e:
        print(f"Error while adding achievement: {e}")
        return False

def update_achievement(alumnileader_id: str, title: str, date: str, 
                       new_description: str = None, new_category: str = None) -> bool:
    """
    Update an achievement record on the server.

    Args:
        achievement_id (int): ID of the achievement to update.
        title (str, optional): The new title of the achievement.
        date (str, optional): The new date of the achievement in 'YYYY-MM-DD' format.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    # Prepare the data to be updated, only include fields that are provided
    data = {
        "alumnileader_id": alumnileader_id,
        "title": title,
        "date": date,
        "description": new_description,
        "category": new_category
    }

    try:
        url = f"{BASE_URL}/update_achievement"
        response = requests.put(url, json=data)
        
        if response.status_code == 200:
            print("Update successful.")
            return True
        elif response.status_code == 400:
            print("Error: Missing or invalid data.")
            return False
        elif response.status_code == 500:
            print("Server error occurred while updating the achievement.")
            return False
        else:
            print(f"Unexpected error occurred. Status code: {response.status_code}")
            return False

    except requests.RequestException as e:
        print("Error while updating achievement details:", e)
        return False


def delete_achievement(achievement_id: int) -> bool:
    """
    Delete an achievement record on the server.

    Args:
        achievement_id (int): ID of the achievement to delete.

    Returns:
        bool: True if the deletion was successful, False otherwise.
    """
    try:
        url = f"{BASE_URL}/delete_achievement/{achievement_id}"
        response = requests.delete(url)

        if response.status_code == 200:
            print("Deletion successful.")
            return True
        elif response.status_code == 404:
            print("Error: Achievement not found.")
            return False
        elif response.status_code == 500:
            print("Server error occurred while deleting the achievement.")
            return False
        else:
            print(f"Unexpected error occurred. Status code: {response.status_code}")
            return False

    except requests.RequestException as e:
        print("Error while deleting achievement details:", e)
        return False

def admin_operations():
    while True:

        # ********** Admin Interface **********

        print("\n=== Select the section number you want to enter ===")
        print("1: Donation Information\n")
        print("2: Alumni Account\n")
        print("3: Alumni Association\n")
        print("4. Achievement\n")
        print("============================================")
        sub_choice = input("Enter your choice: ")

        # ********** Working Content **********

        # 1: Donation Information

        if sub_choice == "1":

            print("\n=== Donation ===")
            print("1. Insert")
            print("2. Edit")
            print("3. Delete")
            print("4. View")
            print("==================")
            donation_choice = input("Enter your choice: ")

            # === Donation Content ===
            
            # View
            if donation_choice == "1":

                donar = input("Enter the donor's name: ")
                amount = int(input("Enter the donation amount: "))
                date = input("Enter the donation date (YYYY-MM-DD): ")

                insert_donation(donar, amount, date)

            elif donation_choice == "2":

                donation_id = int(input("Enter the donation ID to update: "))
                amount = int(input("Enter the new donation amount: "))
                date = input("Enter the new donation date (YYYY-MM-DD): ")

                update_donation(donation_id, amount, date)

            elif donation_choice == "3":
                donation_id = int(input("Enter the donation ID to delete: "))
                if delete_donation(donation_id):
                    print(f"Donation {donation_id} deleted successfully.")
                else:
                    print(f"Failed to delete donation {donation_id}.")
            elif donation_choice == "4":
                alu_id = input("Enter the alumni ID to look up: ")            
                donations = get_donation(alu_id)
                for donation in donations.items():
                    print(donation)
        elif sub_choice == "2":
            print("\n=== Alumni Account ===")
            print("1. Register")
            print("2. Update")
            print("3. Delete")
            print("==================")
            alumni_choice = input("Enter your choice: ")

            # === Alumni Account Content ===
            
            # Register
            if alumni_choice == "1":
                alumni_id = input("Enter the alumni ID: ")
                name = input("Enter the alumni name: ")
                email = input("Enter the alumni email: ")
                password = input("Enter the alumni password: ")
        elif sub_choice == "4":
            print("\n=== Achievement ===")
            print("1. Insert")
            print("2. Edit")
            print("3. Delete")
            print("==================")
            achievement_choice = input("Enter your choice: ")

            # === Achievement Content ===
            
            # Insert
            if achievement_choice == "1":

                alumni_id = input("Enter the alumni ID: ")
                title = input("Enter the achievement title: ")
                description = input("Enter the achievement description: ")
                date = input("Enter the achievement date (YYYY-MM-DD): ")
                category = input("Enter the achievement category (e.g., Academic, Sports, etc.): ")

                add_achievement(alumni_id, title, description, date, category)
            elif achievement_choice == "2":
                # 必須輸入的欄位
                alumnileader_id = input("Enter the alumnileader ID: ")
                title = input("Enter the achievement title: ")
                date = input("Enter the achievement date (YYYY-MM-DD): ")

                # 可選輸入的欄位，若無輸入則設為 None
                new_description = input("Enter the new description (or press Enter to skip): ")
                new_category = input("Enter the new category (or press Enter to skip): ")
                if new_description == "":
                    new_description = None
                if new_category == "":
                    new_category = None
                update_achievement(alumnileader_id, title, date, 
                                   new_description, new_category)            
            elif achievement_choice == "3":
                pass



    
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