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
        
def get_personal_association(alumni_id):
    """
    Fetches all associations an alumni has participated in from the server.

    Args:
        alumni_id (int): Alumni ID.
        base_url (str): Base URL of the Flask application (default: localhost).

    Returns:
        dict: JSON response containing association details or an error message.
    """
    try:
        # Construct the full URL for the API endpoint
        url = f"{BASE_URL}/get_association_by_alumni/{alumni_id}"
        
        # Send a GET request to the API
        response = requests.get(url)
        
        #print(response.json())

        if response.status_code == 200:
            print("Personal association retrieved successfully:")
            return response.json()
        elif response.status_code == 404:
            print("Association not found.")
            return response.json()
        else:
            print(f"Unexpected error occurred. Status code: {response.status_code}")
            return {"status": "error", "message": "Unexpected error occurred."}
    except requests.RequestException as e:
        print("Error while fetching personal association:", e)
        return {"status": "error", "message": str(e)}
    
def get_personal_events(alumni_id):
    '''
    Fetches all events that is held by the association that the alumni is affiliated with.
    Args:
        alumni_id (int): Alumni ID.
    
    Returns:
        dict: JSON response containing event details or an error message.
    '''
    try:
        # Construct the full URL for the API endpoint
        url = f"{BASE_URL}/get_personal_events/{alumni_id}"
        
        # Send a GET request to the API
        response = requests.get(url)
        
        if response.status_code == 200:
            print("Personal events retrieved successfully:")
            return response.json()
        elif response.status_code == 404:
            print("Events not found.")
            return response.json()
        else:
            print(f"Unexpected error occurred. Status code: {response.status_code}")
            return {"status": "error", "message": "Unexpected error occurred."}
    except requests.RequestException as e:
        print("Error while fetching personal events:", e)
        return {"status": "error", "message": str(e)}
    
def get_all_associations():
    '''
    Fetches all associations that are registered in the system.
    
    Returns:
        dict: JSON response containing association details or an error message.
    '''
    try:
        # Construct the full URL for the API endpoint
        url = f"{BASE_URL}/get_all_open_associations"
        
        # Send a GET request to the API
        response = requests.get(url)
        
        if response.status_code == 200:
            print("All associations retrieved successfully:")
            return response.json()
        elif response.status_code == 404:
            print("Associations not found.")
            return response.json()
        else:
            print(f"Unexpected error occurred. Status code: {response.status_code}")
            return {"status": "error", "message": "Unexpected error occurred."}
    except requests.RequestException as e:
        print("Error while fetching all associations:", e)
        return {"status": "error", "message": str(e)}
    
def get_all_upcoming_events():
    '''
    Fetches all upcoming events that are registered in the system.
    
    Returns:
        dict: JSON response containing event details or an error message.
    '''
    try:
        # Construct the full URL for the API endpoint
        url = f"{BASE_URL}/get_all_upcoming_events"
        
        # Send a GET request to the API
        response = requests.get(url)
        
        if response.status_code == 200:
            print("All upcoming events retrieved successfully:")
            return response.json()
        elif response.status_code == 404:
            print("Events not found.")
            return response.json()
        else:
            print(f"Unexpected error occurred. Status code: {response.status_code}")
            return {"status": "error", "message": "Unexpected error occurred."}
    except requests.RequestException as e:
        print("Error while fetching all upcoming events:", e)
        return {"status": "error", "message": str(e)}
    
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
            
            sub_choice = input("Enter your choice: ")
            
            if sub_choice == '1':
                print("\n=== Your Affiliated Association ===")
                response = get_personal_association(ALUMNI_ID)
                if response["status"] == "error":
                    print(f"Error: {response['message']}")
                else:
                    #print(response)
                    for i in range(len(response['associations'])):
                        print(f"=== Association {i+1} ===")
                        key_print = response['associations'][i]['association_name']
                        print(f"Association Name: {key_print}")
                        for key, value in response['associations'][i].items():
                            key_print = key.replace('_', ' ').capitalize()
                            if key_print == "Association name":
                                continue
                            print(f"{key_print}: {value}")
                #print("Affiliated Association functionality is under construction.")
            elif sub_choice == '2':
                print("\n=== Your Association Events ===")
                response = get_personal_events(ALUMNI_ID)
                if response["status"] == "error":
                    print(f"Error: {response['message']}")
                else:
                    #print(response)
                    for i in range(len(response['events'])):
                        print(f"=== Event {i+1} ===")
                        for key, value in response['events'][i].items():
                            key_print = key.replace('_', ' ').capitalize()
                            #if key_print == "Association name":
                                #continue
                            print(f"{key_print}: {value}")
                #print("Association Events functionality is under construction.")
            elif sub_choice == '3':
                print("\n=== All Alumni Associations ===")
                response = get_all_associations()
                if response["status"] == "error":
                    print(f"Error: {response['message']}")
                else:
                    print(response)
                    for i in range(len(response['association_details'])):
                        print(f"=== Association {i+1} ===")
                        key_print = response['association_details'][i]['association_name']
                        print(f"Association Name: {key_print}")
                        for key, value in response['association_details'][i].items():
                            key_print = key.replace('_', ' ').capitalize()
                            if key_print == "Association name":
                                continue
                            print(f"{key_print}: {value}")
                #print("All Alumni Associations functionality is under construction.")
            elif sub_choice == '4':
                print("\n=== All Upcoming Events ===")
                response = get_all_upcoming_events()
                if response["status"] == "error":
                    print(f"Error: {response['message']}")
                else:
                    #print(response)
                    for i in range(len(response['events'])):
                        print(f"=== Event {i+1} ===")
                        key_print = response['events'][i]['event_name']
                        print(f"Event Name: {key_print}")
                        for key, value in response['events'][i].items():
                            key_print = key.replace('_', ' ').capitalize()
                            if key_print == "Event name":
                                continue
                            print(f"{key_print}: {value}")
                #print("All Upcoming Events functionality is under construction.")
            elif sub_choice == '5':
                print("\n=== Join an Alumni Association Event ===")
                print("Please contact the association that holds the event for details.")
            elif sub_choice == '6':
                print("\n=== Join an Alumni Association ===")
                print("Please contact the association for more information.")
            elif sub_choice == '7':
                print("\n=== I am a Cadre of the Alumni Association ===")
                print("1. Add a new member")
                print("2. Delete a member")
                print("3. Add an event")
                print("4. Delete an event")
                print("5. Add a participant to an event")
                print("6. Delete a participant from an event")
                print("7. Transfer the position of cadre")
                
                sub_choice = input("Enter your choice: ")
                
                if sub_choice == '1':
                    print("\n=== Add a New Member ===")
                    print("This functionality is under construction.")
                elif sub_choice == '2':
                    print("\n=== Delete a Member ===")
                    print("This functionality is under construction.")
                elif sub_choice == '3':
                    print("\n=== Add an Event ===")
                    print("This functionality is under construction.")
                elif sub_choice == '4':
                    print("\n=== Delete an Event ===")
                    print("This functionality is under construction.")
                elif sub_choice == '5':
                    print("\n=== Add a Participant to an Event ===")
                    print("This functionality is under construction.")
                elif sub_choice == '6':
                    print("\n=== Delete a Participant from an Event ===")
                    print("This functionality is under construction.")
                elif sub_choice == '7':
                    print("\n=== Transfer the Position of Cadre ===")
                    print("This functionality is under construction.")

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
    
def delete_achievement(title: str, date: str, alumnileader_id: str) -> bool:
    """
    Delete an achievement record on the server.

    Args:
        title (str): Title of the achievement to delete.
        date (str): Date of the achievement to delete.
        alumnileader_id (str): Alumnileader ID associated with the achievement.

    Returns:
        bool: True if the deletion was successful, False otherwise.
    """
    try:
        url = f"{BASE_URL}/delete_achievement"
        
        # Preparing the data to send in the body
        data = {
            "title": title,
            "date": date,
            "alumnileader_id": alumnileader_id
        }

        # Sending the DELETE request with the JSON body
        response = requests.delete(url, json=data)

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

def create_user(username: str, password: str, role: str, current_user: str):
    """
    向伺服器發送請求創建新用戶（僅限 Admin）。

    參數:
        username (str): 要創建的用戶名。
        password (str): 用戶的密碼。
        role (str): 用戶的角色（例如，"Admin" 或其他角色）。
        current_user (str): 發送請求的當前用戶名，該用戶必須擁有 Admin 權限。

    回傳:
        bool: 如果創建成功，返回 True；如果創建失敗，返回 False。
    """
    try:
        url = f"{BASE_URL}/create_user"

        # 構建請求的資料，包含 username, password, role, current_user
        data = {
            "username": username,
            "password": password,
            "role": role,
            "current_user": current_user
        }

        # 發送 POST 請求
        response = requests.post(url, json=data)

        # 根據伺服器回應的狀態碼處理結果
        if response.status_code == 201:
            print(f"用戶 {username} 創建成功。")
            return response.json()['message']
        elif response.status_code == 400:
            print(f"錯誤：{response.json()['message']}")
            return response.json()['message']
        elif response.status_code == 403:
            print(f"錯誤：{response.json()['message']}")
            return response.json()['message']
        elif response.status_code == 500:
            print(f"伺服器錯誤：{response.json()['message']}")
            return response.json()['message']
        else:
            print(f"發生了未知錯誤，狀態碼：{response.status_code}")
            return "Unknown error"

    except requests.RequestException as e:
        print(f"請求過程中發生錯誤：{e}")
        return False

def add_alumni(username:str, first_name: str, last_name: str, sex: str, address: str, graduation_year: int, user_id: int, phone: str) -> bool:
    """
    向伺服器發送請求新增校友記錄。

    參數:
        first_name (str): 校友的名字。
        last_name (str): 校友的姓氏。
        sex (str): 校友的性別（例如，"M" 或 "F"）。
        address (str): 校友的地址。
        graduation_year (int): 校友的畢業年份。
        user_id (int): 該校友對應的用戶 ID。
        phone (str): 校友的電話號碼。

    回傳:
        bool: 如果新增成功，返回 True；如果新增失敗，返回 False。
    """
    try:
        url = f"{BASE_URL}/add_alumni"

        # 構建請求的資料，包含校友資料
        data = {
            "alumni_id": username,
            "first_name": first_name,
            "last_name": last_name,
            "sex": sex,
            "address": address,
            "graduation_year": graduation_year,
            "user_id": user_id,
            "phone": phone
        }

        # 發送 POST 請求
        response = requests.post(url, json=data)

        # 根據伺服器回應的狀態碼處理結果
        if response.status_code == 201:
            print(f"校友 {first_name} {last_name} 新增成功。")
            return True
        elif response.status_code == 400:
            print(f"錯誤：{response.json()['message']}")
            return False
        elif response.status_code == 500:
            print(f"伺服器錯誤：{response.json()['message']}")
            return False
        else:
            print(f"發生了未知錯誤，狀態碼：{response.status_code}")
            return False

    except requests.RequestException as e:
        print(f"請求過程中發生錯誤：{e}")
        return False

def delete_user(user_id: int, username: str) -> bool:
    """
    向伺服器發送請求刪除用戶。

    參數:
        user_id (int): 要刪除的用戶 ID。
        username (str): 發送請求的用戶名。

    回傳:
        bool: 如果刪除成功，返回 True；如果刪除失敗，返回 False。
    """
    try:
        url = f"{BASE_URL}/delete_user/{user_id}"

        # 構建請求的資料，包含 username
        data = {
            "username": username
        }

        # 發送 DELETE 請求
        response = requests.delete(url, json=data)

        # 根據伺服器回應的狀態碼處理結果
        if response.status_code == 200:
            print("用戶刪除成功。")
            return True
        elif response.status_code == 400:
            print(f"錯誤：{response.json()['message']}")
            return False
        elif response.status_code == 403:
            print(f"錯誤：{response.json()['message']}")
            return False
        elif response.status_code == 500:
            print(f"伺服器錯誤：{response.json()['message']}")
            return False
        else:
            print(f"發生了未知錯誤，狀態碼：{response.status_code}")
            return False

    except requests.RequestException as e:
        print(f"請求過程中發生錯誤：{e}")
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
                # 用戶輸入區域
                username = input("輸入要創建的用戶名：")
                password = input("輸入密碼：")
                current_user = input("輸入當前用戶名（必須是 Admin）：")

                # 呼叫 create_user 函式
                user_id = create_user(username, password, "Alumni", current_user)
                print(user_id)
                if user_id:
                    # 用戶輸入區域
                    first_name = input("輸入校友的名字：")
                    last_name = input("輸入校友的姓氏：")
                    sex = input("輸入校友的性別（M/F）：")
                    address = input("輸入校友的地址：")
                    graduation_year = int(input("輸入校友的畢業年份："))
                    phone = input("輸入校友的電話號碼：")

                    # 呼叫 add_alumni 函式
                    add_alumni(username, first_name, last_name, sex, address, graduation_year, user_id, phone)
            elif alumni_choice == '2':
                pass
            elif alumni_choice == "3":
                # 用戶輸入區域
                user_id = int(input("輸入要刪除的用戶 ID："))
                username = input("輸入你的用戶名：")

                # 呼叫 delete_user 函式
                delete_user(user_id, username)
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
                # User input section
                alumnileader_id = input("Enter the alumnileader_id associated with the achievement: ")
                title = input("Enter the title of the achievement to delete: ")
                date = input("Enter the date of the achievement to delete: ")

                # Call the delete function
                delete_achievement(title, date, alumnileader_id)
                



    
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