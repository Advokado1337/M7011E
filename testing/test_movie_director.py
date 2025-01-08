import pytest
import requests
import random
import string

ENDPOINTdirectors = "http://localhost:8000/api/v1/movie-directors/"
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

def random_name(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

# Testing -------------------------------
def test_get_directors_success():
    response = requests.get(ENDPOINTdirectors)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_director_success():
    token = login_auth()
    headers = {'Authorization': f'Token {token}'}
    response = requests.post(ENDPOINTdirectors, json={'firstname': random_name(5), 'surname': random_name(7)}, headers=headers)
    assert response.status_code == 201
    assert 'firstname' in response.json()
    assert 'surname' in response.json()

def test_create_director_missing_fields():
    token = login_auth()
    headers = {'Authorization': f'Token {token}'}
    response = requests.post(ENDPOINTdirectors, json={'firstname': random_name(5)}, headers=headers)
    assert response.status_code == 400
    assert response.json() == {'error': 'Firstname and surname are required'}

def test_create_director_existing_director():
    token = login_auth()
    headers = {'Authorization': f'Token {token}'}
    firstname = random_name(5)
    surname = random_name(7)
    response = requests.post(ENDPOINTdirectors, json={'firstname': firstname, 'surname': surname}, headers=headers)
    assert response.status_code == 201

    response = requests.post(ENDPOINTdirectors, json={'firstname': firstname, 'surname': surname}, headers=headers)
    assert response.status_code == 400
    assert response.json() == {'error': 'Director already exists'}

def test_delete_director_success():
    token = login_auth()
    headers = {'Authorization': f'Token {token}'}
    response = requests.post(ENDPOINTdirectors, json={'firstname': random_name(5), 'surname': random_name(7)}, headers=headers)
    assert response.status_code == 201
    director_id = response.json()['id']

    response = requests.delete(f"{ENDPOINTdirectors}{director_id}/", headers=headers)
    assert response.status_code == 200
    assert response.json() == {'message': 'Director deleted!'}

def test_delete_director_not_found():
    token = login_auth()
    headers = {'Authorization': f'Token {token}'}
    response = requests.delete(f"{ENDPOINTdirectors}9999/", headers=headers)
    assert response.status_code == 404
    assert response.json() == {'error': 'Director not found'}

def test_update_director_success():
    token = login_auth()
    headers = {'Authorization': f'Token {token}'}
    response = requests.post(ENDPOINTdirectors, json={'firstname': random_name(5), 'surname': random_name(7)}, headers=headers)
    assert response.status_code == 201
    director_id = response.json()['id']

    new_firstname = random_name(5)
    response = requests.put(f"{ENDPOINTdirectors}{director_id}/", json={'firstname': new_firstname}, headers=headers)
    assert response.status_code == 204

    response = requests.get(f"{ENDPOINTdirectors}{director_id}/", headers=headers)
    assert response.status_code == 200
    assert response.json()['firstname'] == new_firstname

def test_update_director_not_found():
    token = login_auth()
    headers = {'Authorization': f'Token {token}'}
    response = requests.put(f"{ENDPOINTdirectors}9999/", json={'firstname': random_name(5)}, headers=headers)
    assert response.status_code == 404
    assert response.json() == {'error': 'Director not found'}

