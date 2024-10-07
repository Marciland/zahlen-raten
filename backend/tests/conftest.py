import os

import pytest
from database import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


def pytest_terminal_summary():
    '''
    Merges coverage to a single xml for coverage gutters.
    '''
    os.system('python -m coverage xml')


@pytest.fixture(scope='session')
def db_session():
    engine = create_engine('sqlite:///database/test.db')
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    Base.metadata.drop_all(engine)
