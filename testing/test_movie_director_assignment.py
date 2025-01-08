import pytest
import requests
import random
import string

ENDPOINTdirector_assignment = "http://localhost:8000/api/v1/movie-director-assignments/"
ENDPOINTlogin = "http://localhost:8000/api/v1/users/login/"
ENDPOINTsignup = "http://localhost:8000/api/v1/users/signup/"
ENDPOINTmovies = "http://localhost:8000/api/v1/movies/"
ENDPOINTdirectors = "http://localhost:8000/api/v1/movie-directors/"


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

def setup_director():
    token = login_auth()
    headers = {'Authorization': f'Token {token}'}
    firstname = random_movie(5)
    surname = random_movie(7)
    response = requests.post(ENDPOINTdirectors, json={'firstname': firstname, 'surname': surname}, headers=headers)
    assert response.status_code == 201
    return response.json()['id']

# Testing -------------------------------
def test_get_director_assignments_success():
    response = requests.get(ENDPOINTdirector_assignment)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_director_assignment_not_allowed():
    movie_name = setup_movie()
    director_name = setup_director()
    token = login_auth()
    headers = {'Authorization': f'Token {token}'}
    response = requests.post(ENDPOINTdirector_assignment, json={'movie': movie_name, 'director': director_name}, headers=headers)
    assert response.status_code == 405
    assert response.json() == {'error': 'Method not allowed'}

def test_update_director_assignment_not_allowed():
    movie_name = setup_movie()
    director_name = setup_director()
    token = login_auth()
    headers = {'Authorization': f'Token {token}'}
    response = requests.post(ENDPOINTdirector_assignment, json={'movie': movie_name, 'director': director_name}, headers=headers)
    assert response.status_code == 405

    assignment_id = response.json().get('id', 1)
    response = requests.put(f"{ENDPOINTdirector_assignment}{assignment_id}/", json={'movie': movie_name, 'director': director_name}, headers=headers)
    assert response.status_code == 405
    assert response.json() == {'error': 'Method not allowed'}

def test_delete_director_assignment_not_allowed():
    movie_name = setup_movie()
    director_name = setup_director()
    token = login_auth()
    headers = {'Authorization': f'Token {token}'}
    response = requests.post(ENDPOINTdirector_assignment, json={'movie': movie_name, 'director': director_name}, headers=headers)
    assert response.status_code == 405

    assignment_id = response.json().get('id', 1)
    response = requests.delete(f"{ENDPOINTdirector_assignment}{assignment_id}/", headers=headers)
    assert response.status_code == 405
    assert response.json() == {'error': 'Method not allowed'}

