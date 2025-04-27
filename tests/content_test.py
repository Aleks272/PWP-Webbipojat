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
        assert res.status_code == 204
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
        assert res.status_code == 204
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
