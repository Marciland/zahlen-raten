from flask import Request
from jwt import decode
from jwt.exceptions import (DecodeError, ExpiredSignatureError,
                            InvalidSignatureError)

from .response import JsonResponse


def get_auth_token(request: Request) -> str:
    return request.headers.get('Authorization').split(' ')[1]


def get_payload(token: str, key: str) -> dict:
    return decode(jwt=token,
                  key=key,
                  algorithms=['HS256'])


def token_is_valid(token: str, key: str) -> tuple[JsonResponse, bool]:
    try:
        get_payload(token, key)
    except (InvalidSignatureError, ExpiredSignatureError, DecodeError):
        return JsonResponse('Invalid token!', 401), False
    return None, True


def request_is_authorized(request: Request, key: str) -> tuple[JsonResponse, bool]:
    try:
        token = get_auth_token(request)
    except Exception:
        return JsonResponse('Missing token!', 401), False
    return token_is_valid(token, key)
