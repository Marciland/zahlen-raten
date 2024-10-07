from modules import get_auth_token, get_payload, request_is_authorized, token_is_valid
from flask import Request
import jwt


def test_get_auth_token():
    # request.headers.get('Authorization').split(' ')[1]
    assert True


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
    assert token_is_valid(token, key)
