import requests
import random
import string
"""
This module contains tests for user account functionalities including signup, login, and logout.
Modules:
    requests: To send HTTP requests.
Constants:
    ENDPOINTsignup (str): The endpoint URL for user signup.
    ENDPOINTlogin (str): The endpoint URL for user login.
    ENDPOINTlogout (str): The endpoint URL for user logout.
"""

ENDPOINTsignup = "http://localhost:8000/api/v1/users/signup/"
ENDPOINTlogin = "http://localhost:8000/api/v1/users/login/"
ENDPOINTlogout = "http://localhost:8000/api/v1/users/logout/"

def generate_random_email():
    domains = ["example.com", "test.com", "sample.org"]
    letters = string.ascii_lowercase
    email = ''.join(random.choice(letters) for i in range(10)) + '@' + random.choice(domains)
    return email




def test_signup_success():
    email = generate_random_email()

    response = requests.post(ENDPOINTsignup, data={'email': email, 'password': 'password123'})
    assert response.status_code == 201
    assert 'email' in response.json()

def test_signup_missing_fields():
    email = generate_random_email()

    response = requests.post(ENDPOINTsignup, data={'email': email})
    assert response.status_code == 400
    assert response.json() == {'error': 'Email and password are required'}

def test_signup_existing_email():
    email = generate_random_email()

    requests.post(ENDPOINTsignup, data={'email': email, 'password': 'password123'})
    response = requests.post(ENDPOINTsignup, data={'email': email, 'password': 'password123'})
    assert response.status_code == 400
    assert response.json() == {'error': 'Email already exists'}

def test_login_success():
    email = generate_random_email()
    requests.post(ENDPOINTsignup, data={'email': email, 'password': 'password123'})
    response = requests.post(ENDPOINTlogin, data={'email': email, 'password': 'password123'})
    assert response.status_code == 200
    assert 'token' in response.json()

def test_login_invalid_password():
    email = generate_random_email()

    requests.post(ENDPOINTsignup, data={'email': email, 'password': 'password123'})
    response = requests.post(ENDPOINTlogin, data={'email': email, 'password': 'wrongpassword'})
    assert response.status_code == 400
    assert response.json() == {'error': 'Invalid password'}

def test_login_user_not_found():
    response = requests.post(ENDPOINTlogin, data={'email': 'nonexistent@example.com', 'password': 'password123'})
    assert response.status_code == 404
    assert response.json() == {'error': 'User not found'}

def test_logout_success():
    email = generate_random_email()
    requests.post(ENDPOINTsignup, data={'email': email, 'password': 'password123'})
    login_response = requests.post(ENDPOINTlogin, data={'email': email, 'password': 'password123'})
    token = login_response.json()['token']

    headers = {'Authorization': f'Token {token}'}
    response = requests.post(ENDPOINTlogout, headers=headers)
    assert response.status_code == 200
    assert response.json() == {'message': 'Logout successful!'}

def test_logout_missing_token():
    response = requests.post(ENDPOINTlogout)
    assert response.status_code == 401
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}

