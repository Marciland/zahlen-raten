import os


def pytest_terminal_summary():
    '''
    Merges coverage to a single xml for coverage gutters.
    '''
    os.system('python -m coverage xml')
