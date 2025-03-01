import json
import pytest
from project_watchlist import create_app

@pytest.fixture
def client():
    app = create_app(test_mode=True)
    app.testing = True
    test_client = app.test_client()

    yield test_client

class TestUserItem(object):
    """
    Tests the user item resource
    """
    RESOURCE_URL = "/api/users/foobar/"
    WRONG_RESOURCE_URL = "/api/users/nonexistent/"

    def test_get_existing_user(self, client):
        """
        Tests that we can GET an existing user
        """
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
        res = client.get(self.RESOURCE_URL)
        assert res.status_code == 404
