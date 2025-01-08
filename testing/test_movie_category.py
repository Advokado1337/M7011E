import pytest
import requests
import random
import string

ENDPOINTmoviecategory = "http://localhost:8000/api/v1/movie-categories/"
ENDPOINTlogin = "http://localhost:8000/api/v1/users/login/"
ENDPOINTsignup = "http://localhost:8000/api/v1/users/signup/"
ENDPOINTmovies = "http://localhost:8000/api/v1/movies/"
ENDPOINTcategories = "http://localhost:8000/api/v1/categories/"

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

def random_movie(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def setup_movie():
    token = login_auth()
    headers = {'Authorization': f'Token {token}'}
    response = requests.post(ENDPOINTmovies, json={'name': random_movie(7), 'description': 'A sample movie description', 'category': ['Comedy']}, headers=headers)
    assert response.status_code == 201
    return response.json()['name']

def setup_categories():
    categories = ['Action', 'Comedy', 'Drama']
    token = login_auth()
    headers = {'Authorization': f'Token {token}'}

    categories_server = requests.get("http://localhost:8000/api/v1/categories/").json()
    existing_categories = [category['category'] for category in categories_server]
    
    for category in categories:
        if category not in existing_categories:
            response = requests.post("http://localhost:8000/api/v1/categories/", json={'category': category}, headers=headers)
            assert response.status_code == 201, f"Failed to create category '{category}': {response.status_code} - {response.text}"
            assert 'category' in response.json()

def get_category_id():
    response = requests.get(ENDPOINTcategories)
    assert response.status_code == 200
    return response.json()[0]['id']

# Testing -------------------------------
def test_get_movie_categories_success():
    response = requests.get(ENDPOINTmoviecategory)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_movie_category_not_allowed():
    token = login_auth()
    headers = {'Authorization': f'Token {token}'}
    response = requests.post(ENDPOINTmoviecategory, json={'movie': 'Some Movie', 'category': 'Some Category'}, headers=headers)
    assert response.status_code == 405
    assert response.json() == {'error': 'Method not allowed'}

def test_update_movie_category_not_allowed():
    token = login_auth()
    headers = {'Authorization': f'Token {token}'}
    response = requests.put(f"{ENDPOINTmoviecategory}1/", json={'movie': 'Updated Movie', 'category': 'Updated Category'}, headers=headers)
    assert response.status_code == 405
    assert response.json() == {'error': 'Method not allowed'}

def test_delete_movie_category_not_allowed():
    token = login_auth()
    headers = {'Authorization': f'Token {token}'}
    response = requests.delete(f"{ENDPOINTmoviecategory}1/", headers=headers)
    assert response.status_code == 405
    assert response.json() == {'error': 'Method not allowed'}

