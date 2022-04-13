import json
import os


def setup_environment_variables():
    with open(os.path.join(os.path.dirname(__file__), "env.json")) as file:
        for key, value in json.load(file).items():
            os.environ[key] = value


def pytest_sessionstart():
    setup_environment_variables()
