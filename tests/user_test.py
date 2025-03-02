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

class TestUserCollection(object):
    """
    Tests the user collection resource
    """
    RESOURCE_URL = "/api/users/"
    def test_get(self, client):
        """
        Test that we can GET a valid collection of users
        """
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

    def test_create_user(self, client):
        """
        Test that we can create a user with valid data
        """
        data = {
            "username": "new_user",
            "email": "example-email@example.com",
            "password": "password"
        }
        res = client.post(self.RESOURCE_URL, json=data)
        assert res.status_code == 201
        # ensure that the "Location"-header is set correctly
        assert res.headers["Location"] == f"{self.RESOURCE_URL}{data['username']}/"
        # check that the resource actually exists and it has correct values
        res = client.get(res.headers["Location"])
        assert res.status_code == 200
        response_body = json.loads(res.data)
        assert response_body["username"] == data["username"]
        assert response_body["email"] == data["email"]

    def test_create_user_with_existing_username(self, client):
        """
        Test that we cannot create a user with already taken username
        """
        data = {
            "username": "johndoe",
            "email":"johndoe@gmail.com",
            "password": "password"
        }
        res = client.post(self.RESOURCE_URL, json=data)
        assert res.status_code == 400

    def test_create_user_with_missing_fields(self, client):
        """
        Test that we cannot create a user with missing fields
        """
        data = {
            "username": "new_user2"
        }
        res = client.post(self.RESOURCE_URL, json=data)
        assert res.status_code == 400

    def test_create_user_with_unsupported_media_type(self, client):
        res = client.post(self.RESOURCE_URL,
                          data="test",
                          headers=Headers({"Content-Type":"text"}))
        assert res.status_code == 415

class TestUserItem(object):
    """
    Tests the user item resource
    """
    RESOURCE_URL = "/api/users/foobar/"
    WRONG_RESOURCE_URL = "/api/users/nonexistent/"

    def test_get_existing_user(self, client):
        """
        Test that we can GET an existing user
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
        res = client.get(self.WRONG_RESOURCE_URL)
        assert res.status_code == 404

    def test_modify_user_with_valid_data(self, client):
        """
        Testing that we can modify an
        existing user with valid data
        """
        data = {
            "username": "foobar",
            "email": "foobar@hotmail.com",
            "password": "password"
        }
        res = client.put(self.RESOURCE_URL,
                         json=data)
        # check that the status is correct
        assert res.status_code == 200
        # check that the the data is updated
        res = client.get(self.RESOURCE_URL)
        response_body = json.loads(res.data)
        assert response_body["email"] == data["email"]

    def test_modify_user_with_unsupported_media_type(self, client):
        """
        Testing that modification fails with invalid media type
        """
        res = client.put(self.RESOURCE_URL,
                         data="testdata",
                         headers=Headers({"Content-Type": "text"}))
        assert res.status_code == 415
    
    def test_modify_user_with_missing_fields(self, client):
        """
        Testing that modification fails with missing fields
        """
        data = {
            "username": "foobar"
        }
        res = client.put(self.RESOURCE_URL, json=data)
        assert res.status_code == 400
    
    def test_modify_user_with_existing_username(self, client):
        """
        Test that modification fails with already existing username
        """
        data = {
            "username": "johndoe",
            "email": "foobar@icloud.com",
            "password": "password"
        }
        res = client.put(self.RESOURCE_URL, json=data)
        assert res.status_code == 400

    def test_delete_nonexistent_user(self, client):
        res = client.delete(self.WRONG_RESOURCE_URL)
        assert res.status_code == 404
        
    def test_delete_existing_user(self, client):
        res = client.delete(self.RESOURCE_URL)
        assert res.status_code == 200
        # ensure that the user was deleted
        res = client.get(self.RESOURCE_URL)
        assert res.status_code == 404
