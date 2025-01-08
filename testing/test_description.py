import pytest
import requests
import random
import string

ENDPOINTdescriptions = "http://localhost:8000/api/v1/descriptions/"
ENDPOINTlogin = "http://localhost:8000/api/v1/users/login/"
ENDPOINTsignup = "http://localhost:8000/api/v1/users/signup/"

def generate_random_email():
    domains = ["example.com", "test.com", "sample.org"]
    letters = string.ascii_lowercase
    email = ''.join(random.choice(letters) for i in range(10)) + '@' + random.choice(domains)
    return email

def login_auth():
    admin_email = "jane_smith@example.com"
    admin_password = 'password456'

    login_response = requests.post(ENDPOINTlogin, data={'email': admin_email, 'password': admin_password})
    token = login_response.json()['token']
    assert login_response.status_code == 200
    return token

def login_not_auth():
    email = generate_random_email()
    signup_response = requests.post(ENDPOINTsignup, data={'email': email, 'password': 'password123'})
    login_response = requests.post(ENDPOINTlogin, data={'email': email, 'password': 'password123'})
    token = login_response.json()['token']
    assert login_response.status_code == 200
    return token

def random_description(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

# Testing -------------------------------
def test_get_descriptions_success():
    response = requests.get(ENDPOINTdescriptions)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_description_not_allowed():
    token = login_auth()
    headers = {'Authorization': f'Token {token}'}
    response = requests.post(ENDPOINTdescriptions, json={'description': random_description(20)}, headers=headers)
    assert response.status_code == 405
    assert response.json() == {'error': 'Method not allowed'}

def test_update_description_success():
    token = login_auth()
    headers = {'Authorization': f'Token {token}'}
    description_id = 1  # Assuming a description with ID 1 exists
    new_description = random_description(20)
    response = requests.put(f"{ENDPOINTdescriptions}{description_id}/", json={'description': new_description}, headers=headers)
    assert response.status_code == 204

def test_update_description_not_found():
    token = login_auth()
    headers = {'Authorization': f'Token {token}'}
    response = requests.put(f"{ENDPOINTdescriptions}9999/", json={'description': random_description(20)}, headers=headers)
    assert response.status_code == 404
    assert response.json() == {'error': 'Description not found'}

def test_update_description_missing_fields():
    token = login_auth()
    headers = {'Authorization': f'Token {token}'}
    description_id = 1  # Assuming a description with ID 1 exists
    response = requests.put(f"{ENDPOINTdescriptions}{description_id}/", json={}, headers=headers)
    assert response.status_code == 400
    assert response.json() == {'error': 'Description is required'}

def test_delete_description_not_allowed():
    token = login_auth()
    headers = {'Authorization': f'Token {token}'}
    description_id = 1  # Assuming a description with ID 1 exists
    response = requests.delete(f"{ENDPOINTdescriptions}{description_id}/", headers=headers)
    assert response.status_code == 405
    assert response.json() == {'error': 'Method not allowed'}
