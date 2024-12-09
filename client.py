# this is the terminal user interface for the client (alumni management system)
# it is a simple command line interface that allows the user to interact with the server
# and perform various operations such as adding, deleting, updating, and searching for alumni

import requests
import json
import sys

BASE_URL = "http://localhost:5001"

# global variable to store the user's role
ROLE = None
USER_ID = None
USER_NAME = None
ALUMNI_ID = None
CADRE_LIST = []


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
            return (
                response.json().get("role"),
                response.json().get("user_id"),
                response.json().get("username"),
            )

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
        "job_description": job_description,
    }

    try:
        response = requests.post(
            f"{BASE_URL}/add_career_history/{alumni_id}", json=career_data
        )
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

        # print(response.json())

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
    """
    Fetches all events that is held by the association that the alumni is affiliated with.
    Args:
        alumni_id (int): Alumni ID.

    Returns:
        dict: JSON response containing event details or an error message.
    """
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
    """
    Fetches all associations that are registered in the system.

    Returns:
        dict: JSON response containing association details or an error message.
    """
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
    """
    Fetches all upcoming events that are registered in the system.

    Returns:
        dict: JSON response containing event details or an error message.
    """
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


def is_association_cadre(alumni_id):
    """
    Check if the alumni is a cadre of any association.
    Args:
        alumni_id (int): Alumni ID.
    Returns:
        dict: JSON response containing association details or an error message.
    """
    try:
        # Construct the full URL for the API endpoint
        url = f"{BASE_URL}/is_association_cadre/{alumni_id}"

        # Send a GET request to the API
        response = requests.get(url)

        if response.status_code == 200:
            print("Association cadre status retrieved successfully:")
            return response.json()
        elif response.status_code == 404:
            print("Association cadre status not found.")
            return response.json()
        else:
            print(f"Unexpected error occurred. Status code: {response.status_code}")
            return {"status": "error", "message": "Unexpected error occurred."}
    except requests.RequestException as e:
        print("Error while fetching association cadre status:", e)
        return {"status": "error", "message": str(e)}

def add_event(association_id):
    """
    Function to interact with the server and add an event.
    """

    # User input for event details
    event_name = input("Enter event name: ")
    date = input("Enter event date (YYYY-MM-DD): ")
    description = input("Enter event description: ")
    location = input("Enter event location: ")

    event_data = {
        "association_id": association_id,
        "event_name": event_name,
        "date": date,
        "description": description,
        "location": location
    }

    try:
        response = requests.post(f"{BASE_URL}/create_event/{association_id}", json=event_data)  # 4 is a placeholder for association_id
        response_data = response.json()

        if response.status_code == 201:
            print(f"Success: {response_data.get('message')}")
        else:
            print(f"Error: {response_data.get('message')} (Status Code: {response.status_code})")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        
# we have: @app.route('/add_member_to_association/<int:association_id>/<string:alumni_id>', methods=['POST'])
def add_member(association_id, alumni_id):
    """
    Add a member to an association.
    Args:
        association_id (int): Association ID.
        alumni_id (int): Alumni ID.
    Returns:
        dict: JSON response containing success message or an error message.
    """
    url = f"{BASE_URL}/add_member_to_association/{association_id}/{alumni_id}"
    try:
        response = requests.post(url)
        if response.status_code == 201:
            # print("Member added successfully.")
            return response.json()
        elif response.status_code == 404:
            # print("Association or alumni not found.")
            return response.json()
        else:
            print(f"Unexpected error occurred. Status code: {response.status_code}")
            return {"status": "error", "message": "Unexpected error occurred."}
    except requests.RequestException as e:
        print("Error while adding member to association:", e)
        return {"status": "error", "message": str(e)}
    
# we have @app.route('/remove_member_from_association/<int:association_id>/<int:alumni_id>', methods=['DELETE'])
def remove_member(association_id, alumni_id):
    """
    Remove a member from an association.
    Args:
        association_id (int): Association ID.
        alumni_id (int): Alumni ID.
    Returns:
        dict: JSON response containing success message or an error message.
    """
    url = f"{BASE_URL}/remove_member_from_association/{association_id}/{alumni_id}"
    try:
        response = requests.delete(url)
        if response.status_code == 200:
            # print("Member removed successfully.")
            return response.json()
        elif response.status_code == 404:
            # print("Association or alumni not found.")
            return response.json()
        else:
            print(f"Unexpected error occurred. Status code: {response.status_code}")
            return {"status": "error", "message": "Unexpected error occurred."}
    except requests.RequestException as e:
        print("Error while removing member from association:", e)
        return {"status": "error", "message": str(e)}


def list_association_members(association_id):
    """
    List all the members of an association.
    Args:
        alumni_id (int): Alumni ID.
    Returns:
        dict: JSON response containing association details or an error message.
    """
    try:
        # Construct the full URL for the API endpoint
        url = f"{BASE_URL}/get_association_members/{association_id}"

        # Send a GET request to the API
        response = requests.get(url)

        if response.status_code == 200:
            print("Association members retrieved successfully:")
            return response.json()
        elif response.status_code == 404:
            print("Association members not found.")
            return response.json()
        else:
            print(f"Unexpected error occurred. Status code: {response.status_code}")
            return {"status": "error", "message": "Unexpected error occurred."}
    except requests.RequestException as e:
        print("Error while fetching association members:", e)
        return {"status": "error", "message": str(e)}
    
def end_cadre(association_id, alumni_id):
    """
    End the cadre position of an alumni in an association.
    Args:
        association_id (int): Association ID.
        alumni_id (int): Alumni ID.
    Returns:
        dict: JSON response containing success message or an error message.
    """
    print("Are you sure you want to end the cadre position? (y/n)")
    choice = input("Enter your choice: ")
    if choice.lower() != "y":
        print("Ending cadre position cancelled.")
        return {"status": "cancelled", "message": "Ending cadre position cancelled."}
    url = f"{BASE_URL}/end_cadre/{association_id}/{alumni_id}"
    try:
        response = requests.post(url)
        if response.status_code == 201:
            # print("Cadre position ended successfully.")
            return response.json()
        elif response.status_code == 404:
            # print("Association or alumni not found.")
            return response.json()
        else:
            print(f"Unexpected error occurred. Status code: {response.status_code}")
            return {"status": "error", "message": "Unexpected error occurred."}
    except requests.RequestException as e:
        print("Error while ending cadre position:", e)
        return {"status": "error", "message": str(e)}
    
def delete_event(association_id):
    """
    Function to interact with the server and delete an event.
    """
    #print("\n=== Delete an Event ===")

    # User input for event details to delete
    event_name = input("Enter event name: ")
    date = input("Enter event date (YYYY-MM-DD): ")

    event_data = {
        "event_name": event_name,
        "date": date
    }

    try:
        response = requests.delete(f"{BASE_URL}/delete_event", json=event_data)  # 4 is a placeholder for association_id
        response_data = response.json()

        if response.status_code == 200:
            print(f"Success: {response_data.get('message')}")
        else:
            print(f"Error: {response_data.get('message')} (Status Code: {response.status_code})")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        
def add_event_participant():
    """
    Function to interact with the server and add a participant to an event.
    """
    print("\n=== Add Event Participant ===")

    # User input for event participant details
    alumni_id = input("Enter the participant's alumni ID: ")
    event_name = input("Enter event name: ")
    date = input("Enter event date (YYYY-MM-DD): ")

    participant_data = {
        "alumni_id": alumni_id,
        "event_name": event_name,
        "date": date
    }

    try:
        response = requests.post(f"{BASE_URL}/add_event_participant", json=participant_data)
        response_data = response.json()

        if response.status_code == 201:
            print(f"Success: {response_data.get('message')} (If the input in correct, the participant has been added to the event)")
        else:
            print(f"Error: {response_data.get('message')} (Status Code: {response.status_code})")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        
def remove_event_participant():
    """
    Function to interact with the server and remove a participant from an event.
    """
    print("\n=== Remove Event Participant ===")

    # User input for event participant details
    alumni_id = input("Enter the alumni ID: ")
    event_name = input("Enter event name: ")
    date = input("Enter event date (YYYY-MM-DD): ")

    participant_data = {
        "alumni_id": alumni_id,
        "event_name": event_name,
        "date": date
    }

    try:
        response = requests.delete(f"{BASE_URL}/remove_event_participant", json=participant_data)
        response_data = response.json()

        if response.status_code == 200:
            print(f"Success: {response_data.get('message')}")
        else:
            print(f"Error: {response_data.get('message')} (Status Code: {response.status_code})")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")    

def add_cadre_to_association(association_id):
    """
    Function to interact with the server and add a user as a cadre to an association.
    """
    print("\n=== Add Other Cadre to Association ===")

    # User input for cadre details
    alumni_id = input("Enter the new cadre's alumni ID: ")
    pos = input("Enter the position of the cadre: ")

    cadre_data = {
        "alumni_id": alumni_id,
        "association_id": int(association_id),  # Ensure it's an integer
        "position": pos
    }

    try:
        response = requests.post(f"{BASE_URL}/add_cadre_to_association/{alumni_id}/{association_id}/{pos}", json=cadre_data)
        response_data = response.json()

        if response.status_code == 201:
            print(f"Success: {response_data.get('message')}")
        else:
            print(f"Error: {response_data.get('message')} (Status Code: {response.status_code})")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        
def get_donation(alumni_id):
    """
    Fetches alumni donation information from the server.

    Args:
        alumni_id (string): ID of the alumni to retrieve.

    Returns:
        dict: The response JSON containing alumni donation details or error message.
    """
    try:
        # Construct the request URL
        url = f"{BASE_URL}/get_alumni_donations/{alumni_id}"

        # Send a GET request to the server
        response = requests.get(url)

        # Check the status code and handle response
        if response.status_code == 200:
            print("Alumni donation details retrieved successfully:")
            return response.json()
        elif response.status_code == 404:
            print("Alumni not found.")
            return response.json()
        else:
            print(f"Unexpected error occurred. Status code: {response.status_code}")
            return {"status": "error", "message": "Unexpected error occurred."}
    except requests.RequestException as e:
        # Handle any request exceptions (e.g., network issues)
        print("Error while fetching alumni donation details:", e)
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
                    alumni_info = alumni_details["alumni_details"]

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
                            key_print = key.replace("_", " ").capitalize()
                            if key_print == "Alumni id":
                                key_print = "Alumni ID (User Name)"
                            print(f"{key_print}: {value}")
                degree_details = get_degree(ALUMNI_ID)
                if degree_details["status"] == "error":
                    print(f"Error: {degree_details['message']}")
                # Print the response in a formatted way
                alumni_info = degree_details["degree"]
                print("=== Degree Information ===")
                for key, value in alumni_info.items():
                    key_print = key.replace("_", " ").capitalize()
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
                alumni_info = career_details["career_paths"]
                for i in range(len(alumni_info)):
                    print(f"=== Job {i+1} ===")
                    for key, value in alumni_info[i].items():
                        key_print = key.replace("_", " ").capitalize()
                        if key_print == "Alumni id":
                            continue
                            key_print = "Alumni ID (User Name)"
                        if key_print == "End date":
                            print_later = (
                                f"{key_print}: {value if value else 'Present'}"
                            )
                            continue
                        print(f"{key_print}: {value}")
                    print(print_later)

            elif sub_choice == "2":
                print("\n=== Edit Career ===")
                # 這裡可以實現編輯事業資料功能
                print("Edit Career functionality is under construction.")

        elif choice == "3":
            print("\n=== Your Past Achievements ===")
            
            #print("Achievements functionality is under construction.")

        elif choice == "4":
            print("\n=== Donation ===")
            donation_details = get_donation(ALUMNI_ID)
            if donation_details["status"] == "error":
                print(f"Error: {donation_details['message']}")
            else:
                print(donation_details)
            #print("Donation functionality is under construction.")

        elif choice == "5":
            print("\n=== Alumni Association ===")
            print("1. View your affiliated association")
            print("2. View your association events")
            print("3. View all alumni associations")
            print("4. View all upcoming events")
            print("5. Join an alumni association event")
            print("6. Join an alumni association")
            print("7. I am a cadre of the alumni association")
            
            sub_choice = input("Enter your choice: ")

            if sub_choice == "1":
                print("\n=== Your Affiliated Association ===")
                response = get_personal_association(ALUMNI_ID)
                if response["status"] == "error":
                    print(f"Error: {response['message']}")
                else:
                    # print(response)
                    for i in range(len(response["associations"])):
                        print(f"=== Association {i+1} ===")
                        key_print = response["associations"][i]["association_name"]
                        print(f"Association Name: {key_print}")
                        for key, value in response["associations"][i].items():
                            key_print = key.replace("_", " ").capitalize()
                            if key_print == "Association name":
                                continue
                            print(f"{key_print}: {value}")
                # print("Affiliated Association functionality is under construction.")
            elif sub_choice == "2":
                print("\n=== Your Association Events ===")
                response = get_personal_events(ALUMNI_ID)
                if response["status"] == "error":
                    print(f"Error: {response['message']}")
                else:
                    # print(response)
                    for i in range(len(response["events"])):
                        print(f"=== Event {i+1} ===")
                        for key, value in response["events"][i].items():
                            key_print = key.replace("_", " ").capitalize()
                            # if key_print == "Association name":
                            # continue
                            print(f"{key_print}: {value}")
                # print("Association Events functionality is under construction.")
            elif sub_choice == "3":
                print("\n=== All Alumni Associations ===")
                response = get_all_associations()
                if response["status"] == "error":
                    print(f"Error: {response['message']}")
                else:
                    print(response)
                    for i in range(len(response["association_details"])):
                        print(f"=== Association {i+1} ===")
                        key_print = response["association_details"][i][
                            "association_name"
                        ]
                        print(f"Association Name: {key_print}")
                        for key, value in response["association_details"][i].items():
                            key_print = key.replace("_", " ").capitalize()
                            if key_print == "Association name":
                                continue
                            print(f"{key_print}: {value}")
                # print("All Alumni Associations functionality is under construction.")
            elif sub_choice == "4":
                print("\n=== All Upcoming Events ===")
                response = get_all_upcoming_events()
                if response["status"] == "error":
                    print(f"Error: {response['message']}")
                else:
                    # print(response)
                    for i in range(len(response["events"])):
                        print(f"=== Event {i+1} ===")
                        key_print = response["events"][i]["event_name"]
                        print(f"Event Name: {key_print}")
                        for key, value in response["events"][i].items():
                            key_print = key.replace("_", " ").capitalize()
                            if key_print == "Event name":
                                continue
                            print(f"{key_print}: {value}")
                # print("All Upcoming Events functionality is under construction.")
            elif sub_choice == "5":
                print("\n=== Join an Alumni Association Event ===")
                print(
                    "Please contact the association that holds the event for details."
                )
            elif sub_choice == "6":
                print("\n=== Join an Alumni Association ===")
                print("Please contact the association for more information.")
            elif sub_choice == "7":
                # print("\n=== I am a Cadre of the Alumni Association ===")

                # check if the alumni is a cadre of any association
                response = is_association_cadre(ALUMNI_ID)
                if response["status"] == "error":
                    print(f"Error: {response['message']}")
                else:
                    # print(response)
                    if len(response["associations"]) == 0:
                        print("You are not a cadre of any association.")
                    else:
                        print("=== You are a cadre of the following associations ===")
                        for i in range(len(response["associations"])):
                            print(f"=== Association {i+1} ===")
                            key_print = response["associations"][i]["association_name"]
                            print(f"Association Name: {key_print}")
                            for key, value in response["associations"][i].items():
                                key_print = key.replace("_", " ").capitalize()
                                if key_print == "Association id":
                                    CADRE_LIST.append(int(value))
                                if key_print == "Association name":
                                    continue
                                print(f"{key_print}: {value}")
                        print(
                            "Which organization do you want to log in as a cadre for? (Please enter the Association ID)"
                        )

                        association_id = input("Enter the Association ID: ")
                        if int(association_id) not in CADRE_LIST:
                            print("You are not a cadre of this association.")
                        else:
                            print("\nWhat do you want to do?")
                            print("1. View Member List")
                            print("2. Add a new member")
                            print("3. Delete a member")
                            print("4. Add an event")
                            print("5. Delete an event")
                            print("6. Add a participant to an event")
                            print("7. Delete a participant from an event")
                            print("8. Add another alumni the Position of Cadre")
                            print("9. Exit Cadre Position")
                            sub_choice = input("Enter your choice: ")
                            if sub_choice == "1":
                                print("\n=== View Member List ===")
                                response = list_association_members(association_id)
                                if response["status"] == "error":
                                    print(f"Error: {response['message']}")
                                else:
                                    # print(response)
                                    # Extract keys from the first member dynamically
                                    keys = list(response["members"][0].keys())
                                    keys_print = [
                                        key.replace("_", " ").capitalize()
                                        for key in keys
                                        if key != "association_id"
                                    ]

                                    # Print dynamic table header
                                    header = " | ".join(
                                        [f"{key:<20}" for key in keys_print]
                                    )
                                    print(header)
                                    print("-" * len(header))

                                    # Print each member's details
                                    for member in response["members"]:
                                        row = " | ".join(
                                            [
                                                f"{str(member[key]):<20}"
                                                for key in keys
                                                if key != "association_id"
                                            ]
                                        )
                                        print(row)
                                # print("This functionality is under construction.")
                            elif sub_choice == "2":
                                print("\n=== Add a New Member ===")
                                added_member_id = input(
                                    "Enter the Alumni ID of the new member: "
                                )
                                response = add_member(association_id, added_member_id)
                                if response["status"] == "error":
                                    print(
                                        f"Failed to add member {added_member_id}: {response['message']}"
                                    )
                                else:
                                    print(response["message"])
                                # print("This functionality is under construction.")
                            elif sub_choice == "3":
                                print("\n=== Delete a Member ===")
                                deleted_member_id = input("Enter the Alumni ID to delete: ")
                                response = remove_member(association_id, deleted_member_id)
                                if response["status"] == "error":
                                    print(
                                        f"Failed to delete member {deleted_member_id}: {response['message']}"
                                    )
                                else:
                                    print(response["message"])
                                # print("This functionality is under construction.")
                            elif sub_choice == "4":
                                print("\n=== Add an Event ===")
                                add_event(association_id)
                                # print("This functionality is under construction.")
                            elif sub_choice == "5":
                                print("\n=== Delete an Event ===")
                                delete_event(association_id)
                                #print("This functionality is under construction.")
                            elif sub_choice == "6":
                                print("\n=== Add a Participant to an Event ===")
                                add_event_participant()
                                #print("This functionality is under construction.")
                            elif sub_choice == "7":
                                print("\n=== Delete a Participant from an Event ===")
                                remove_event_participant()
                                #print("This functionality is under construction.")
                            elif sub_choice == "8":
                                print(
                                    "\n=== Add another alumni the Position of Cadre ==="
                                )
                                add_cadre_to_association(association_id)
                                #print("This functionality is under construction.")
                            elif sub_choice == "9":
                                print("\n=== Exit Cadre Position ===")
                                response = end_cadre(association_id, ALUMNI_ID)
                                if response["status"] == "error":
                                    print(f"Error: {response['message']}")
                                else:
                                    print(response["message"])
                                #print("This functionality is under construction.")
                                
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

        elif choice == "4":  # Exit the program
            print("Exiting the program. Goodbye!")
            break
        else:  # Handle invalid input
            print("Invalid choice. Please select a valid option.")
            continue

if __name__ == "__main__":
    main()
