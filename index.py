import requests
import pytest
import os

from dotenv import load_dotenv
# загружаем ключ
load_dotenv()

REGRES_KEY = os.getenv('YOUR_API_KEY')
# адрес API
BASE_URL = "https://reqres.in/api"

headers = {
    'Content-Type': 'application/json',
    'x-api-key': REGRES_KEY}

# создаем тестового пользователя
def test_create_user():
    response = requests.post(f'{BASE_URL}/users', json={'name': 'User', 'job': 'Evangelist'}, headers=headers)
    print(f'Status: {response.status_code}')
    print(f'Response: {response.text}')
    assert response.status_code == 201
    data = response.json() # увидеть, что вернули в json
    assert data['name'] == 'User'
    assert data['job'] == 'Evangelist'

def test_get_user_by_id():
    resp = requests.get(f'{BASE_URL}/users/7122', headers=headers)
    print(f'Status: {resp.status_code}')
    print(f'Response: {resp.text}')
    assert resp.status_code == 200

def test_create_user_missing_job_field():
    respo = requests.post(f'{BASE_URL}/users', json={'name': ''}, headers=headers)
    print(f'Status: {respo.status_code}')
    print(f'Response: {respo.text}')
    assert respo.status_code == 422

def test_create_user_missing_name_field():
    resp = requests.post(f'{BASE_URL}/users', json={'job': ''}, headers=headers)
    print(f'Status: {resp.status_code}')
    print(f'Response: {resp.text}')
    assert resp.status_code == 422
    #ReqRes does not validate like the real API but the first tests work fine

def test_wrong_api_key():
    wrong_headers = {
        'Content-Type': 'application/json',
        'x-api-key': 'wrong_api_key'
    }
    response = requests.post(f'{BASE_URL}/users', json={'name': 'User'}, headers=wrong_headers)
    with pytest.raises(Exception) as e:
        response.raise_for_status()
    print(f'Error is: {e.value}')