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