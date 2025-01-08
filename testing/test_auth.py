import requests
import random
import string
import os
import pytest
"""
This module contains tests for user account functionalities including signup, login, and logout.
Modules:
    requests: To send HTTP requests.
Constants:
    ENDPOINTsignup (str): The endpoint URL for user signup.
    ENDPOINTlogin (str): The endpoint URL for user login.
    ENDPOINTlogout (str): The endpoint URL for user logout.
"""

ENDPOINTupdate_role = "http://localhost:8000/api/v1/users/update_role/"
ENDPOINTlogin = "http://localhost:8000/api/v1/users/login/"
ENDPOINTsignup = "http://localhost:8000/api/v1/users/signup/"



def generate_random_email():
    domains = ["example.com", "test.com", "sample.org"]
    letters = string.ascii_lowercase
    email = ''.join(random.choice(letters) for i in range(10)) + '@' + random.choice(domains)
    return email

def clear_tokens():
    response = requests.post("http://localhost:8000/api/v1/users/clear_token/")
    return response

# Testing -------------------------------

def test_update_role_success():
    admin_email = "jane_smith@example.com"
    admin_password = 'password456'

    login_response = requests.post(ENDPOINTlogin, data={'email': admin_email, 'password': admin_password})
    token = login_response.json()['token']

    assert login_response.status_code == 200
    email = generate_random_email()
    signup_response = requests.post(ENDPOINTsignup, data={'email': email, 'password': 'password123'})

    headers = {'Authorization': f'Token {token}'}
    response = requests.put(ENDPOINTupdate_role,data={'email': email, 'is_staff': 1},headers=headers)
    
    
    assert response.status_code == 200
    assert 'email' in response.json()
    
def test_update_role_user_not_found():
    admin_email = "jane_smith@example.com"
    admin_password = 'password456'

    login_response = requests.post(ENDPOINTlogin, data={'email': admin_email, 'password': admin_password})
    token = login_response.json()['token']

    email = generate_random_email()  # Generate an email that is not signed up
    headers = {'Authorization': f'Token {token}'}
    response = requests.put(ENDPOINTupdate_role, data={'email': email, 'is_staff': 1}, headers=headers)
    
    assert response.status_code == 404
    assert response.json() == {'error': 'User not found'}

def test_update_role_wrong_auth():
    email = generate_random_email()
    signup_response = requests.post(ENDPOINTsignup, data={'email': email, 'password': 'password123'})
    login_response = requests.post(ENDPOINTlogin, data={'email': email, 'password': 'password123'})
    token = login_response.json()['token']

    headers = {'Authorization': f'Token {token}'}

    response = requests.put(ENDPOINTupdate_role, data={'email': email, 'is_staff': 1}, headers=headers)

    assert response.status_code == 403
    assert response.json() == {'error': 'Superuser access required'}
    
def test_update_role_missing_token():
    
    email = generate_random_email()
    signup_response = requests.post(ENDPOINTsignup, data={'email': email, 'password': 'password123'})

    headers = {}  # No Authorization header
    response = requests.put(ENDPOINTupdate_role, data={'email': email, 'is_staff': 1}, headers=headers)

    assert response.status_code == 401
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}

def test_update_role_invalid_token():
    email = generate_random_email()
    signup_response = requests.post(ENDPOINTsignup, data={'email': email, 'password': 'password123'})

    headers = {'Authorization': 'Token invalidtoken'}  # Invalid token
    response = requests.put(ENDPOINTupdate_role, data={'email': email, 'is_staff': 1}, headers=headers)

    assert response.status_code == 401
    assert response.json() == {'detail': 'Invalid token.'}

 
