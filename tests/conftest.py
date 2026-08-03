"""Shared fixtures for backend API tests."""

from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app

BASE_ACTIVITIES = deepcopy(activities)


@pytest.fixture
def client():
    """Provide a client for interacting with the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities_state():
    """Keep in-memory activity data isolated between tests."""
    activities.clear()
    activities.update(deepcopy(BASE_ACTIVITIES))
    yield
    activities.clear()
    activities.update(deepcopy(BASE_ACTIVITIES))