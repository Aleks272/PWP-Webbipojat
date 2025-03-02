import pytest
import mongoengine
import json
from werkzeug.datastructures import Headers

from project_watchlist import create_app
from mockdata import populate

@pytest.fixture(scope="module")
def client():
    app = create_app(test_mode=True)
    app.testing = True
    # populate db
    populate(test_mode=True)
    with app.test_request_context():
        yield app.test_client()
    # Clean up after tests
    db = mongoengine.get_connection()
    db.drop_database('test_db')
    mongoengine.disconnect_all()

class TestAuthLogin():

    RESOURCE_URL = "/auth/login/"

    def test_login_with_valid_credentials(self, client):
        """
        Test that we can login with valid credentials and get an access token
        """
        data = {
            "username": "johndoe",
            "password": "password"
        }
        res = client.post(self.RESOURCE_URL, json=data)
        assert res.status_code == 200
        # check that we get the token
        response_body = json.loads(res.data)
        assert response_body["token"]

    def test_login_with_invalid_credentials(self, client):
        """
        Test that we cannot login with invalid credentials
        """
        data = {
            "username": "johndoe",
            "password": "wrongpassword"
        }
        res = client.post(self.RESOURCE_URL,
                          json=data)
        assert res.status_code == 401

    def test_login_with_unsupported_media_type(self, client):
        """
        Test that login fails with unsupported media type
        """
        res = client.post(self.RESOURCE_URL,
                          data="username=johndoe;password=password",
                          headers=Headers({
                            "Content-Type": "text"
                          }))
        assert res.status_code == 415

    def test_login_with_missing_fields(self, client):
        """
        Test that login fails with missing fields
        """
        data = {
            "username": "johndoe"
        }
        res = client.post(self.RESOURCE_URL, json=data)
        assert res.status_code == 400