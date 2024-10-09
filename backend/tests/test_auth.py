from modules import get_auth_token, get_payload, request_is_authorized, token_is_valid
import jwt
import requests


def test_get_auth_token():
    s = requests.Session()
    s.headers.update({ "Authorization": 'Bearer test_token' })
    assert get_auth_token(s) == "test_token"


def test_get_payload():
    key = "SECRET_KEY"
    test_payload = {'user_id': 123}
    token = jwt.encode(test_payload, key, algorithm='HS256')
    new_payload = get_payload(token, key)
    assert test_payload, new_payload


def token_is_valid():
    key = "SECRET_KEY"
    test_payload = {'user_id': 123}
    token = jwt.encode(test_payload, key, algorithm='HS256')
    assert token_is_valid(token, key)[1]


def test_request_is_authorized():
    key = "SECRET_KEY"
    test_payload = {'user_id': 123}
    token = jwt.encode(test_payload, key, algorithm='HS256')
    s = requests.Session()
    s.headers.update({ "Authorization": 'Bearer ' + token })
    assert request_is_authorized(s, key)[1] == True


def test_request_is_not_valid():
    key = "SECRET_KEY"
    test_payload = {'user_id': 123}
    token = jwt.encode(test_payload, key, algorithm='HS256')
    s = requests.Session()
    s.headers.update({ "Authorization": 'Bearer ' + token })
    assert request_is_authorized(s, "WRONG_KEY")[1] == False


def test_token_missing():
    key = "SECRET_KEY"
    s = requests.Session()
    assert request_is_authorized(s, key)[1] == False
