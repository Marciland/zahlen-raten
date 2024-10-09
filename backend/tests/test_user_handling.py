import pytest
from database import Player
from modules import User, register_user
from sqlalchemy.orm import Session

@pytest.mark.parametrize('username, password, valid', [
    ("username", "password", True),
    ("username", "", False),
    ("", "password", False)
])
def test_is_valid(username, password, valid):
    test_user = User(username, password)
    assert test_user.is_valid()[1] == valid

def test_failed_login(db_session: Session):
    test_user = User("not", "registered")
    assert test_user.login(db_session, "key")[1] == None

def test_register_user_and_login(db_session: Session):
    test_user = User("name", "password")
    assert register_user(db_session, test_user).status, "201 CREATED"
    assert register_user(db_session, test_user).status, "409 CONFLICT"
    assert test_user.login(db_session, "key")[0] == None
