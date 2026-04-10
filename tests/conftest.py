import copy

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

initial_activities = copy.deepcopy(activities)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    activities.clear()
    activities.update(copy.deepcopy(initial_activities))
    yield
    activities.clear()
    activities.update(copy.deepcopy(initial_activities))
