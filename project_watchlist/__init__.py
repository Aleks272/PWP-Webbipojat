from flask import Flask
from mongoengine import connect
import os
from dotenv import load_dotenv

load_dotenv()

def create_app(test_mode=False):
    app = Flask(__name__)
    db_name = "db"
    if test_mode:
        db_name = "test_db"
    connect(host=os.getenv("MONGODB_CONNECTION_STRING"), name=db_name)

    from project_watchlist import watchlist_api
    from project_watchlist import resources
    from project_watchlist.utils import UserConverter, WatchlistConverter, ContentConverter
    app.url_map.converters["user"] = UserConverter
    app.url_map.converters["watchlist"] = WatchlistConverter
    app.url_map.converters["content"] = ContentConverter
    app.register_blueprint(watchlist_api.api_bp)
    return app
