import json
import pytest
from werkzeug.datastructures import Headers
from project_watchlist import create_app
import mongoengine
from mockdata import populate

@pytest.fixture(scope="session")
def client():
    app = create_app(test_mode=True)
    app.testing = True
    # populate db
    populate(test_mode=True)
    yield app.test_client()
    # Clean up after tests
    db = mongoengine.get_connection()
    db.drop_database('test_db')

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
            "email": "foobar@icloud.com"
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

class TestWatchListCollection(object):
    """
    Tests WatchlistCollection-resource
    """

    RESOURCE_URL = "/api/users/johndoe/watchlists/"

    def test_get(self, client):
        res = client.get(self.RESOURCE_URL)
        assert res.status_code == 200
        response_body = json.loads(res.data)
        watchlists = response_body["watchlists"]
        # there should be content inside watchlists
        assert len(watchlists) > 0
    
    def test_post_with_valid_data(self, client):
        """
        Create a watchlist with valid data
        """
        data = {
            "user_note": "test note",
            "public_entry": True,
            "content_ids": [1,2]
        }
        res = client.post(self.RESOURCE_URL, json=data)
        assert res.status_code == 201
        #check that there is a valid location-header
        assert res.headers["Location"]
        # check that the resource actually exists
        res = client.get(res.headers["Location"])
        assert res.status_code == 200

    def test_post_with_missing_fields(self, client):
        """
        Test that POSTing fails with missing fields
        """
        data = {
            "user_note": "test note",
            "public_entry": True
        }
        res = client.post(self.RESOURCE_URL, json=data)
        assert res.status_code == 400

    def test_post_with_duplicate_content(self, client):
        """
        Test that watchlist cannot be created with duplicate content id's
        """
        data = {
            "user_note": "test note",
            "public_entry": True,
            "content_ids": [1,2,2]
        }
        res = client.post(self.RESOURCE_URL, json=data)
        assert res.status_code == 400

    def test_post_with_nonexistent_content(self, client):
        """
        Test that we cannot create a watchlist with content id that does not exist
        """
        data = {
            "user_note": "test note",
            "public_entry": True,
            "content_ids": [1,100]
        }
        res = client.post(self.RESOURCE_URL, json=data)
        assert res.status_code == 400

    def test_post_with_unsupported_media_type(self, client):
        res = client.post(self.RESOURCE_URL,
                          data="test",
                          headers=Headers({"Content-Type":"text"}))
        assert res.status_code == 415

class TestWatchListItem(object):

    RESOURCE_URL = "/api/watchlists/1/"
    WRONG_RESOURCE_URL = "/api/watchlists/100/"

    def test_get_existing_watchlist(self, client):
        """
        Get an existing watchlist
        """
        res = client.get(self.RESOURCE_URL)
        assert res.status_code == 200
        # check that the watchlist contains needed properties
        response_body = json.loads(res.data)
        assert response_body["watchlist_id"]
        assert response_body["user_note"]
        assert response_body["person_id"]
        assert response_body["content"]
        # check that there is content
        assert len(response_body["content"]) > 0

    def test_get_nonexistent_watchlist(self, client):
        """
        Test that GETting a nonexisten watchlist gives error
        """
        res = client.get(self.WRONG_RESOURCE_URL)
        assert res.status_code == 404

    def test_put_with_valid_data(self, client):
        """
        Check that we can modify list with valid data
        """
        data = {
            "content_ids": [1],
            "user_note": "modified note",
            "public_entry": True
        }
        res = client.put(self.RESOURCE_URL, json=data)
        assert res.status_code == 200
        # check that the note changed
        res = client.get(self.RESOURCE_URL)
        response_body = json.loads(res.data)
        assert response_body["user_note"] == data["user_note"]

    def test_put_with_missing_fields(self, client):
        """
        Check that we cannot modify list with missing fields
        """
        data = {
            "content_ids": [1],
            "public_entry": True
        }
        res = client.put(self.RESOURCE_URL, json=data)
        assert res.status_code == 400

    def test_put_with_unsupported_media_type(self, client):
        """
        Check that we get correct error for non-JSON request
        """
        res = client.put(self.RESOURCE_URL,
                         data="testdata",
                         headers=Headers({"Content-Type":"text"}))
        assert res.status_code == 415

    def test_put_with_nonexistent_content(self, client):
        """
        Test that we cannot modify a list to contain nonexistent content
        """
        data = {
            "content_ids": [1, 100],
            "public_entry": True,
            "user_note": "ok"
        }
        res = client.put(self.RESOURCE_URL, json=data)
        assert res.status_code == 400

    def test_put_with_duplicate_content(self, client):
        """
        Test that we cannot modify a list to contain duplicate entries
        """
        data = {
            "content_ids": [1, 1],
            "public_entry": True,
            "user_note": "ok"
        }
        res = client.put(self.RESOURCE_URL, json=data)
        assert res.status_code == 400

    def test_delete_existing_watchlist(self, client):
        """
        Check that we can delete an existing list
        """
        res = client.delete(self.RESOURCE_URL)
        assert res.status_code == 200
        # check that the resource is gone
        res = client.get(self.RESOURCE_URL)
        assert res.status_code == 404

    def test_delete_nonexistent_watchlist(self, client):
        """
        Check that we cannot delete nonexistent list
        """
        res = client.delete(self.WRONG_RESOURCE_URL)
        assert res.status_code == 404

class TestContentItem():
    """
    Tests for content item resource
    """

    RESOURCE_URL = "/api/content/1/"
    WRONG_RESOURCE_URL = "/api/content/100/"

    def test_get_existing_content(self, client):
        """
        Test that we can get an existing content
        """
        res = client.get(self.RESOURCE_URL)
        assert res.status_code == 200
        response_body = json.loads(res.data)
        assert response_body["content_id"] == 1
        assert response_body["name"] == "Inception"
        assert response_body["content_type"] == "MOVIE"
    
    def test_get_nonexistent_content(self, client):
        """
        Test that we cannot get nonexistent content
        """
        res = client.get(self.WRONG_RESOURCE_URL)
        assert res.status_code == 404
    
    def test_put_with_valid_data(self, client):
        """
        Test that we can update content with valid data
        """
        data = {
            "name": "Titanic",
            "content_type": "MOVIE"
        }
        res = client.put(self.RESOURCE_URL, json=data)
        assert res.status_code == 200
        # check that the content changed
        res = client.get(self.RESOURCE_URL)
        response_body = json.loads(res.data)
        assert response_body["name"] == data["name"]
        assert response_body["content_type"] == data["content_type"]

    def test_put_with_missing_fields(self, client):
        """
        Test that we cannot update content with missing fields
        """
        data = {
            "name": "Titanic"
        }
        res = client.put(self.RESOURCE_URL, json=data)
        assert res.status_code == 400

    def test_put_with_unsupported_media_type(self, client):
        """
        Test that we get proper error for unsupported media type
        """
        res = client.put(self.RESOURCE_URL,
                         data="test",
                         headers=Headers({"Content-Type": "text"}))
        assert res.status_code == 415

    def test_delete_existing_content(self, client):
        """
        Test that we can delete existing content
        """
        res = client.delete(self.RESOURCE_URL)
        assert res.status_code == 200
        # check that the resource is deleted
        res = client.get(self.RESOURCE_URL)
        assert res.status_code == 404
    
    def test_delete_nonexistent_content(self, client):
        """
        Test that we get error when deleting nonexistent content
        """
        res = client.delete(self.WRONG_RESOURCE_URL)
        assert res.status_code == 404

class TestContentCollection():
    """
    Tests for content collection resource
    """

    RESOURCE_URL = "/api/content/"

    def test_get_content(self, client):
        """
        Tests that we can get all content
        """
        res = client.get(self.RESOURCE_URL)
        assert res.status_code == 200
        response_body = json.loads(res.data)
        # check that we have content
        assert len(response_body["content"]) > 0

    def test_post_with_valid_data(self, client):
        """
        Test that we can create new content with valid data
        """
        data = {
            "name": "Jurassic Park",
            "content_type": "MOVIE"
        }
        res = client.post(self.RESOURCE_URL, json=data)
        assert res.status_code == 201
        # check that headers set correctly
        assert res.headers["Location"]
        # check that the resource is created
        res = client.get(res.headers["Location"])
        assert res.status_code == 200

    def test_post_with_missing_fields(self, client):
        """
        Check that we cannot create content with missing fields
        """
        data = {
            "name": "Jurassic Park"
        }
        res = client.post(self.RESOURCE_URL, json=data)
        assert res.status_code == 400

    def test_post_with_unsupported_media_type(self, client):
        """
        Test that we get proper error when using unsupported media type
        """
        res = client.post(self.RESOURCE_URL,
                          data="test",
                          headers=Headers({"Content-Type": "text"}))
        assert res.status_code == 415

    def test_post_with_existing_content_name(self, client):
        """
        Test that cannot create content with existing name
        """
        data = {
            "name": "Deadpool",
            "content_type": "MOVIE"
        }
        res = client.post(self.RESOURCE_URL, json=data)
        assert res.status_code == 400
