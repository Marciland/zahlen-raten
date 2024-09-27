from json import dumps

from flask import Response


class JsonResponse(Response):
    def __init__(self, message: str, status: int, body: dict = None) -> None:
        if not body:
            body = {}  # do not make this default!
        body.update({'detail': message})
        super().__init__(dumps(body), status)
        self.headers['content-type'] = 'application/json'
