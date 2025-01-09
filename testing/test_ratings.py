import pytest
import requests
import random
import string

ENDPOINTratings = "http://localhost:8000/api/v1/ratings/"
ENDPOINTlogin = "http://localhost:8000/api/v1/users/login/"
ENDPOINTsignup = "http://localhost:8000/api/v1/users/signup/"
ENDPOINTmovies = "http://localhost:8000/api/v1/movies/"
ENDPOINTdeleteuserrating = "http://localhost:8000/api/v1/ratings/destroy_user_rating/"

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

# Testing -------------------------------
def test_get_ratings_success():
    response = requests.get(ENDPOINTratings)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_rating_success():
    movie_name = setup_movie()
    token = login_not_auth()
    headers = {'Authorization': f'Token {token}'}
    response = requests.post(ENDPOINTratings, json={'stars': 5, 'movie': movie_name}, headers=headers)
    assert response.status_code == 201
    assert 'stars' in response.json()

def test_create_rating_missing_fields():
    movie_name = setup_movie()
    token = login_not_auth()
    headers = {'Authorization': f'Token {token}'}
    response = requests.post(ENDPOINTratings, json={'movie': movie_name}, headers=headers)
    assert response.status_code == 400
    assert response.json() == {'error': 'Stars and movie are required'}

def test_create_rating_invalid_stars():
    movie_name = setup_movie()
    token = login_not_auth()
    headers = {'Authorization': f'Token {token}'}
    response = requests.post(ENDPOINTratings, json={'stars': 6, 'movie': movie_name}, headers=headers)
    assert response.status_code == 400
    assert response.json() == {'error': 'Stars must be between 1 and 5'}

def test_create_rating_existing_rating():
    movie_name = setup_movie()
    token = login_not_auth()
    headers = {'Authorization': f'Token {token}'}
    response = requests.post(ENDPOINTratings, json={'stars': 5, 'movie': movie_name}, headers=headers)
    assert response.status_code == 201

    response = requests.post(ENDPOINTratings, json={'stars': 5, 'movie': movie_name}, headers=headers)
    assert response.status_code == 400
    assert response.json() == {'error': 'Rating already exists'}

def test_create_rating_movie_not_found():
    token = login_not_auth()
    headers = {'Authorization': f'Token {token}'}
    response = requests.post(ENDPOINTratings, json={'stars': 5, 'movie': 'Nonexistent'}, headers=headers)
    assert response.status_code == 404
    assert response.json() == {'error': 'Movie not found'}

def test_delete_rating_success():
    movie_name = setup_movie()
    token = login_not_auth()
    headers = {'Authorization': f'Token {token}'}
    response = requests.post(ENDPOINTratings, json={'stars': 5, 'movie': movie_name}, headers=headers)
    assert response.status_code == 201

    rating_id = response.json()['id']
    # Use the same token for deletion to ensure permissions
    response = requests.delete(f"{ENDPOINTratings}{rating_id}/", headers=headers)
    assert response.status_code == 200
    assert response.json() == {'message': 'Rating deleted!'}

def test_delete_rating_not_found():
    token = login_not_auth()
    headers = {'Authorization': f'Token {token}'}
    response = requests.delete(f"{ENDPOINTratings}9999/", headers=headers)
    assert response.status_code == 404
    assert response.json() == {'error': 'Rating not found'}

def test_delete_rating_wrong_user():
    movie_name = setup_movie()
    token = login_not_auth()
    headers = {'Authorization': f'Token {token}'}
    response = requests.post(ENDPOINTratings, json={'stars': 5, 'movie': movie_name}, headers=headers)
    assert response.status_code == 201

    newheaders = {'Authorization': f'Token {login_not_auth()}'}
    rating_id = response.json()['id']
    # Use the same other token for deletion to ensure permissions
    response = requests.delete(f"{ENDPOINTratings}{rating_id}/", headers=newheaders)
    assert response.status_code == 404
    assert response.json() == {'error': 'Wrong user'}

def test_delete_user_rating_success():
    movie_name = setup_movie()
    token = login_not_auth()
    headers = {'Authorization': f'Token {token}'}
    response = requests.post(ENDPOINTratings, json={'stars': 5, 'movie': movie_name}, headers=headers)
    assert response.status_code == 201
    rating_id = response.json()['id']

    authtoken = login_auth()
    authheaders = {'Authorization': f'Token {authtoken}'}
    response = requests.delete(ENDPOINTdeleteuserrating, json={'rating_id': rating_id}, headers=authheaders)
    assert response.status_code == 200
    assert response.json() == {'message': 'Rating deleted!'}

def test_update_rating_not_allowed():
    movie_name = setup_movie()
    token = login_auth()
    headers = {'Authorization': f'Token {token}'}
    response = requests.post(ENDPOINTratings, json={'stars': 5, 'movie': movie_name}, headers=headers)
    assert response.status_code == 201
    rating_id = response.json()['id']

    response = requests.put(f"{ENDPOINTratings}{rating_id}/", json={'stars': 4, 'movie': movie_name}, headers=headers)
    assert response.status_code == 405
    assert response.json() == {'error': 'Method not allowed'}

def test_update_no_login_user():
    movie_name = setup_movie()
    response = requests.post(ENDPOINTratings, json={'stars': 5, 'movie': movie_name})
    assert response.status_code == 401

def test_auth_for_all():
   
    response = requests.delete(ENDPOINTratings)
    assert response.status_code == 401
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}

    response = requests.delete(ENDPOINTdeleteuserrating)
    assert response.status_code == 401
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}

    response = requests.post(ENDPOINTdeleteuserrating)
    assert response.status_code == 401
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}

    response = requests.put(ENDPOINTratings)
    assert response.status_code == 401
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}

    response = requests.put(ENDPOINTratings + '1/')
    assert response.status_code == 401
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}

    notauth = login_not_auth()
    headers = {'Authorization': f'Token {notauth}'}
    response = requests.delete(ENDPOINTdeleteuserrating, headers=headers)
    assert response.status_code == 403
    assert response.json() == {'error': 'Staff access required'}


    