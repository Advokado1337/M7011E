import requests
import random
import string
import os
import pytest
"""
This module contains tests for movies functionalities including get, add, delete and update (CRUD).
Modules:
    requests: To send HTTP requests.
Constants:
    ENDPOINTmovies (str): The endpoint URL for movies.
"""

ENDPOINTmovies = "http://localhost:8000/api/v1/movies/"
ENDPOINTlogin = "http://localhost:8000/api/v1/users/login/"
ENDPOINTsignup = "http://localhost:8000/api/v1/users/signup/"


#Helper functions -------------------------------

def generate_random_email():
    domains = ["example.com", "test.com", "sample.org"]
    letters = string.ascii_lowercase
    email = ''.join(random.choice(letters) for i in range(10)) + '@' + random.choice(domains)
    return email

def clear_tokens():
    response = requests.post("http://localhost:8000/api/v1/users/clear_token/")
    return response

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

# Testing -------------------------------

def test_get_movies_success():
    response = requests.get(ENDPOINTmovies)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_specific_movie_success():
    response = requests.get(ENDPOINTmovies)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    data = response.json()
    movie_id = response.json()[0]['id']
    response = requests.get(f"{ENDPOINTmovies}{movie_id}/")
    assert response.status_code == 200

    movie_name = data[0]['name']
    print(movie_name)
    assert response.json()['name'] == movie_name

def test_add_movie_success():
    token = login_auth()
    headers = {'Authorization': f'Token {token}'}

    response = requests.post(ENDPOINTmovies, json={'name': random_movie(7), 'description': 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.', 'category': ['Comedy']}, headers=headers)
    assert response.status_code == 201
    assert 'name' in response.json()

def test_add_movie_missing_fields():
    token = login_auth()
    headers = {'Authorization': f'Token {token}'}

    response = requests.post(ENDPOINTmovies, json={'name': 'The Godfather'}, headers=headers)
    assert response.status_code == 400
    assert response.json() == {'error': 'Name, description, and category are required'}

def test_add_movie_wrong_auth():
    token = login_not_auth()
    headers = {'Authorization': f'Token {token}'}
    
    response = requests.post(ENDPOINTmovies, json={'name': 'The Godfather', 'description': 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.', 'category': ['Comedy']}, headers=headers)
    assert response.status_code == 403
    assert response.json() == {'error': 'Staff access required'}

    
