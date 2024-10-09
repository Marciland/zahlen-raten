from modules import get_auth_token, get_payload, request_is_authorized, token_is_valid
import jwt
from flask import Request
from werkzeug.test import EnvironBuilder
import pytest


def test_get_auth_token():
    token = "test_token"
    env = EnvironBuilder(headers={'Authorization': 'Bearer ' + token})
    request = Request(env.get_environ())
    assert get_auth_token(request) == "test_token"


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


@pytest.mark.parametrize('test_key, valid', [
    ("SECRET_KEY", True),
    ("WRONG_KEY", False)
])
def test_request_is_authorized(test_key, valid):
    key = "SECRET_KEY"
    payload = {'user_id': 123}
    token = jwt.encode(payload, key, algorithm='HS256')
    env = EnvironBuilder(headers={'Authorization': 'Bearer ' + token})
    request = Request(env.get_environ())
    assert request_is_authorized(request, test_key)[1] == valid


def test_token_missing():
    key = "SECRET_KEY"
    env = EnvironBuilder(headers={'Missing': 'Token'})
    request = Request(env.get_environ())
    assert request_is_authorized(request, key)[1] == False
