import datetime
from zeep import Client
from credentials import EMPLOYEE_EMAIL, QUINYX_APP_PASSWORD, API_TOKEN
import requests

# Quinyx API Configuration
QUINYX_URL = "https://user-api-rc.quinyx.com/v2/users/shifts" 
def get_shifts(API_TOKEN):
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_TOKEN}"
    }

    response = requests.get(QUINYX_URL, headers=headers)
    if response.status_code == 200:
        users = response.json()
        for user in users:
            print(f"User ID: {user['id']}, Name: {user['name']}")
    else:
        print(f"Failed to retrieve users: {response.status_code}")

def get_token(email, password):
    url = "https://user-api-rc.quinyx.com/v2/oauth/token"
    body = {
        "grantType": "password",
        "username": email,
        "password": password
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    #set content type to application/json
    response = requests.post(url, data=body, headers=headers)
    if response.status_code == 200:
        return response.json()["token"]
    else:
        print(f"Failed to retrieve token: {response.status_code}")
        return None

def refresh_token(refreshToken):
    url = "https://user-api-rc.quinyx.com/v2/oauth/token"
    body = {
        "grantType": "refresh_Token",
        "refreshToken": refreshToken
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    response = requests.post(url, json=body, headers=headers)
    if response.status_code == 200:
        return response.json()["token"]
    else:
        print(f"Failed to refresh token: {response.status_code}")
        return None    
    
if __name__ == "__main__":
    # get_shifts()
    # token = get_token(EMPLOYEE_EMAIL, QUINYX_APP_PASSWORD)
    # print(token)
    RT = "ODRjYTRjNjctMGNlOS00MThiLTg3YjItNDMxNDEwMjc4MGRkX3FzMw=="
    # token = refresh_token(RT)
    # print(token)
    # get_shifts(API_TOKEN)