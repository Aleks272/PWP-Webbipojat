import json
import pytest
from werkzeug.datastructures import Headers
from project_watchlist import create_app
import mongoengine
from mockdata import populate
from flask_jwt_extended import create_access_token
from project_watchlist.models import Users


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

class TestPublicWatchListCollection(object):
    """
    Tests WatchlistCollection-resource
    """
    RESOURCE_URL = "/api/users/elonmusk/watchlists/public/"

    def test_get(self, client):
        res = client.get(self.RESOURCE_URL)
        assert res.status_code == 200
        response_body = json.loads(res.data)
        watchlists = response_body["watchlists"]
        # there should be content inside watchlists
        assert len(watchlists) > 0
    
    def test_post_with_valid_data_and_headers(self, client):
        """
        Create a watchlist with valid data and authorization
        """
        data = {
            "user_note": "test note",
            "public_entry": True,
            "content_ids": [1,2]
        }
        user = Users.objects(username="elonmusk").first()
        access_token = create_access_token(user)
        headers = Headers({
            "Authorization": f"Bearer {access_token}"
        })
        res = client.post(self.RESOURCE_URL, json=data, headers=headers)
        assert res.status_code == 201
        #check that there is a valid location-header
        assert res.headers["Location"]
        # check that the resource actually exists
        res = client.get(res.headers["Location"])
        assert res.status_code == 200

    def test_post_with_valid_data_and_invalid_headers(self, client):
        """
        Create a watchlist with valid data and invalid authorization
        """
        data = {
            "user_note": "test note",
            "public_entry": True,
            "content_ids": [1,2]
        }
        user = Users.objects(username="johndoe").first()
        access_token = create_access_token(user)
        headers = Headers({
            "Authorization": f"Bearer {access_token}"
        })
        res = client.post(self.RESOURCE_URL, json=data, headers=headers)
        assert res.status_code == 401

    def test_post_with_missing_fields(self, client):
        """
        Test that POSTing fails with missing fields
        """
        data = {
            "user_note": "test note",
            "public_entry": True
        }
        user = Users.objects(username="elonmusk").first()
        access_token = create_access_token(user)
        headers = Headers({
            "Authorization": f"Bearer {access_token}"
        })
        res = client.post(self.RESOURCE_URL, json=data, headers=headers)
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
        user = Users.objects(username="elonmusk").first()
        access_token = create_access_token(user)
        headers = Headers({
            "Authorization": f"Bearer {access_token}"
        })
        res = client.post(self.RESOURCE_URL, json=data, headers=headers)
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
        user = Users.objects(username="elonmusk").first()
        access_token = create_access_token(user)
        headers = Headers({
            "Authorization": f"Bearer {access_token}"
        })
        res = client.post(self.RESOURCE_URL, json=data, headers=headers)
        assert res.status_code == 400

    def test_post_with_unsupported_media_type(self, client):
        """
        Test that POST with wrong media type results in error
        """
        user = Users.objects(username="elonmusk").first()
        access_token = create_access_token(user)
        headers = Headers({
            "Content-Type":"text",
            "Authorization": f"Bearer {access_token}"
        })
        res = client.post(self.RESOURCE_URL,
                          data="test",
                          headers=headers)
        assert res.status_code == 415

class TestPrivateWatchListCollection(object):
    """
    Tests PrivateWatchlistCollection-resource
    """
    RESOURCE_URL = "/api/users/elonmusk/watchlists/private/"

    def test_get_valid_authorization(self, client):
        """
        Test that we can GET watchlists with valid authorization
        """
        user = Users.objects(username="elonmusk").first()
        access_token = create_access_token(user)
        headers = Headers({
            "Content-Type":"text",
            "Authorization": f"Bearer {access_token}"
        })
        res = client.get(self.RESOURCE_URL, headers=headers)
        assert res.status_code == 200
        response_body = json.loads(res.data)
        watchlists = response_body["watchlists"]
        # there should be content inside watchlists
        assert len(watchlists) > 0
    
    def test_get_invalid_authorization(self, client):
        """
        Test that we cannot GET watchlists with invalid authorization
        """
        user = Users.objects(username="johndoe").first()
        access_token = create_access_token(user)
        headers = Headers({
            "Content-Type":"text",
            "Authorization": f"Bearer {access_token}"
        })
        res = client.get(self.RESOURCE_URL, headers=headers)
        assert res.status_code == 401

    def test_post_with_valid_data_and_headers(self, client):
        """
        Create a watchlist with valid data and authorization
        """
        data = {
            "user_note": "test note",
            "public_entry": True,
            "content_ids": [1,2]
        }
        user = Users.objects(username="elonmusk").first()
        access_token = create_access_token(user)
        headers = Headers({
            "Authorization": f"Bearer {access_token}"
        })
        res = client.post(self.RESOURCE_URL, json=data, headers=headers)
        assert res.status_code == 201
        #check that there is a valid location-header
        assert res.headers["Location"]
        # check that the resource actually exists
        res = client.get(res.headers["Location"])
        assert res.status_code == 200

    def test_post_with_valid_data_and_invalid_headers(self, client):
        """
        Create a watchlist with valid data and invalid authorization
        """
        data = {
            "user_note": "test note",
            "public_entry": True,
            "content_ids": [1,2]
        }
        user = Users.objects(username="johndoe").first()
        access_token = create_access_token(user)
        headers = Headers({
            "Authorization": f"Bearer {access_token}"
        })
        res = client.post(self.RESOURCE_URL, json=data, headers=headers)
        assert res.status_code == 401

    def test_post_with_missing_fields(self, client):
        """
        Test that POSTing fails with missing fields
        """
        data = {
            "user_note": "test note",
            "public_entry": True
        }
        user = Users.objects(username="elonmusk").first()
        access_token = create_access_token(user)
        headers = Headers({
            "Authorization": f"Bearer {access_token}"
        })
        res = client.post(self.RESOURCE_URL, json=data, headers=headers)
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
        user = Users.objects(username="elonmusk").first()
        access_token = create_access_token(user)
        headers = Headers({
            "Authorization": f"Bearer {access_token}"
        })
        res = client.post(self.RESOURCE_URL, json=data, headers=headers)
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
        user = Users.objects(username="elonmusk").first()
        access_token = create_access_token(user)
        headers = Headers({
            "Authorization": f"Bearer {access_token}"
        })
        res = client.post(self.RESOURCE_URL, json=data, headers=headers)
        assert res.status_code == 400

    def test_post_with_unsupported_media_type(self, client):
        """
        Test that POST with wrong media type results in error
        """
        user = Users.objects(username="elonmusk").first()
        access_token = create_access_token(user)
        headers = Headers({
            "Content-Type":"text",
            "Authorization": f"Bearer {access_token}"
        })
        res = client.post(self.RESOURCE_URL,
                          data="test",
                          headers=headers)
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
        assert res.status_code == 204
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
        assert res.status_code == 204
        # check that the resource is gone
        res = client.get(self.RESOURCE_URL)
        assert res.status_code == 404

    def test_delete_nonexistent_watchlist(self, client):
        """
        Check that we cannot delete nonexistent list
        """
        res = client.delete(self.WRONG_RESOURCE_URL)
        assert res.status_code == 404
