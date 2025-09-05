# test_secure_api.py
import requests
import pytest
from config_loader import load_credentials, get_credential

# Base URL
URL_NAME = "https://api.yavshok.ru"

# Fixture to load credentials once for all tests
@pytest.fixture(scope="session")
def credentials():
    return load_credentials()

def test_login_correct(credentials):
    """Test correct login credentials"""
    url_login = f"{URL_NAME}/auth/login"

    login_json = {
        "email": credentials["correct_login"],
        "password": credentials["correct_password"]
    }

    response = requests.post(url_login, json=login_json)
    assert response.status_code == 200, (
        f"Expected code 200, got {response.status_code}"
    )
    
    # Optionally store the token for other tests if login is successful
    if response.status_code == 200:
        response_data = response.json()
        return response_data.get("token")  # Adjust based on actual response

def test_login_incorrect(credentials):
    """Test incorrect login credentials"""
    url_login = f"{URL_NAME}/auth/login"

    login_json = {
        "email": credentials["incorrect_login"],
        "password": credentials["correct_password"]  # Using correct password with wrong email
    }

    response = requests.post(url_login, json=login_json)
    assert response.status_code == 422, (
        f"Expected code 422, got {response.status_code}"
    )

def test_exist_corr(credentials):
    """Test existing email"""
    url_exist = f"{URL_NAME}/exist"

    credentials_json = {
        "email": credentials["correct_email"]
    }

    response = requests.post(url_exist, json=credentials_json)
    assert response.status_code == 200, (
        f"Expected 200, received {response.status_code}"
    )

    response_data = response.json()
    assert response_data["exist"] == True, (
        f"Expected 'exist' = True, got {response_data['exist']}"
    )

def test_exist_incorr(credentials):
    """Test non-existing email"""
    url_exist = f"{URL_NAME}/exist"

    credentials_json = {
        "email": credentials["incorrect_email"]
    }

    response = requests.post(url_exist, json=credentials_json)
    assert response.status_code == 200, (
        f"Expected 200, received {response.status_code}"
    )

    response_data = response.json()
    assert response_data["exist"] == False, (
        f"Expected 'exist' = False, got {response_data['exist']}"
    )

def test_modify_user_name_corr(credentials):
    """Test correct name modification with valid token"""
    url_update = f"{URL_NAME}/user/name"
    token = credentials["auth_token"]
    new_name = "Bingo"
    
    headers = {"Authorization": f"Bearer {token}"}
    name_json = {"name": new_name}
    
    response = requests.patch(url_update, json=name_json, headers=headers)
    assert response.status_code == 200, (
        f"Expected 200, received {response.status_code}"
    )

    data = response.json()
    assert data["user"]["name"] == new_name

def test_modify_user_name_empty(credentials):
    """Test name modification with empty name"""
    url_update = f"{URL_NAME}/user/name"
    token = credentials["auth_token"]
    new_name = ""
    
    headers = {"Authorization": f"Bearer {token}"}
    name_json = {"name": new_name}
    
    response = requests.patch(url_update, json=name_json, headers=headers)
    assert response.status_code == 422, (
        f"Expected 422, received {response.status_code}"
    )

# Optional: Dynamic token generation from login
def test_with_dynamic_token(credentials):
    """Example of getting token dynamically from login"""
    # First login to get fresh token
    url_login = f"{URL_NAME}/auth/login"
    login_json = {
        "email": credentials["correct_login"],
        "password": credentials["correct_password"]
    }
    
    login_response = requests.post(url_login, json=login_json)
    if login_response.status_code == 200:
        auth_data = login_response.json()
        dynamic_token = auth_data.get("token")  # Adjust based on actual response format
        
        # Use dynamic token in subsequent requests
        url_update = f"{URL_NAME}/user/name"
        headers = {"Authorization": f"Bearer {dynamic_token}"}
        name_json = {"name": "DynamicTest"}
        
        response = requests.patch(url_update, json=name_json, headers=headers)
        assert response.status_code == 200
