import pytest
import requests
import random
import string

ENDPOINTcategories = "http://localhost:8000/api/v1/categories/"
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

def random_category(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

# Testing -------------------------------
def test_get_categories_success():
    response = requests.get(ENDPOINTcategories)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_category_success():
    token = login_auth()
    headers = {'Authorization': f'Token {token}'}
    response = requests.post(ENDPOINTcategories, json={'category': random_category(7)}, headers=headers)
    assert response.status_code == 201
    assert 'category' in response.json()

def test_create_category_missing_fields():
    token = login_auth()
    headers = {'Authorization': f'Token {token}'}
    response = requests.post(ENDPOINTcategories, json={}, headers=headers)
    assert response.status_code == 400
    assert response.json() == {'error': 'Category is required'}

def test_create_category_existing_category():
    token = login_auth()
    headers = {'Authorization': f'Token {token}'}
    category_name = random_category(7)
    response = requests.post(ENDPOINTcategories, json={'category': category_name}, headers=headers)
    assert response.status_code == 201

    response = requests.post(ENDPOINTcategories, json={'category': category_name}, headers=headers)
    assert response.status_code == 400
    assert response.json() == {'error': 'Category already exists'}

def test_delete_category_success():
    token = login_auth()
    headers = {'Authorization': f'Token {token}'}
    response = requests.post(ENDPOINTcategories, json={'category': random_category(7)}, headers=headers)
    assert response.status_code == 201
    category_id = response.json()['id']

    response = requests.delete(f"{ENDPOINTcategories}{category_id}/", headers=headers)
    assert response.status_code == 200
    assert response.json() == {'message': 'Category deleted!'}

def test_delete_category_not_found():
    token = login_auth()
    headers = {'Authorization': f'Token {token}'}
    response = requests.delete(f"{ENDPOINTcategories}9999/", headers=headers)
    assert response.status_code == 404
    assert response.json() == {'error': 'Category not found'}

def test_update_category_success():
    token = login_auth()
    headers = {'Authorization': f'Token {token}'}
    response = requests.post(ENDPOINTcategories, json={'category': random_category(7)}, headers=headers)
    assert response.status_code == 201
    category_id = response.json()['id']

    new_category_name = random_category(7)
    response = requests.put(f"{ENDPOINTcategories}{category_id}/", json={'category': new_category_name}, headers=headers)
    assert response.status_code == 200
    assert response.json() == {'message': 'Category updated!'}

def test_update_category_not_found():
    token = login_auth()
    headers = {'Authorization': f'Token {token}'}
    response = requests.put(f"{ENDPOINTcategories}9999/", json={'category': random_category(7)}, headers=headers)
    assert response.status_code == 404
    assert response.json() == {'error': 'Category not found'}


