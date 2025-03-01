import json
import pytest
from project_watchlist import create_app

@pytest.fixture
def client():
    app = create_app(test_mode=True)
    app.testing = True
    yield app.test_client()

class TestUserItem(object):
    """
    Tests the user item resource
    """
    RESOURCE_URL = "/api/users/foobar/"
    WRONG_RESOURCE_URL = "/api/users/nonexistent/"

    def test_get_existing_user(self, client):
        res = client.get(self.RESOURCE_URL)
        assert res.status_code == 200
        response_body = json.loads(res.data)
        assert "username" in response_body
        assert "email" in response_body
        assert "person_id" in response_body

    def test_get_nonexistent_user(self, client):
        """
        Test that GETting a nonexistent user returns 404
        """
        res = client.get(self.WRONG_RESOURCE_URL)
        assert res.status_code == 404

class TestUserCollection(object):
    """
    Tests the user collection resource
    """
    RESOURCE_URL = "/api/users/"
    def test_get(self, client):
        res = client.get(self.RESOURCE_URL)
        assert res.status_code == 200
        users = json.loads(res.data)
        # check that users-property exists
        assert "users" in users
        # check that every user has required properties
        for user in users["users"]:
            assert "username" in user
            assert "email" in user
            assert "person_id" in user

class TestWatchListCollection(object):
    """
    Tests WatchlistCollection-resource
    """

    RESOURCE_URL = "/api/users/foobar/watchlists/"

    def test_get(self, client):
        res = client.get(self.RESOURCE_URL)
        assert res.status_code == 200
