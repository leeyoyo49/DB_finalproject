# this is the terminal user interface for the client (alumni management system)
# it is a simple command line interface that allows the user to interact with the server
# and perform various operations such as adding, deleting, updating, and searching for alumni

import requests
import sys

BASE_URL = "http://localhost:5000"

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
    