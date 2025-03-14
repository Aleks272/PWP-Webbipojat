"""
Main module for watchlist API
"""
import os
from flask import Flask
from mongoengine import connect
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager

load_dotenv()

def create_app(test_mode=False):
    """
    Creates and returns the app instance
    """
    app = Flask(__name__)
    db_name = "db"
    if test_mode:
        db_name = "test_db"
    connect(host=os.getenv("MONGODB_CONNECTION_STRING"),
            name=db_name,
            uuidRepresentation="standard")
    # TODO: change this to something from .env
    app.config["JWT_SECRET_KEY"] = "secret"
    jwt_manager = JWTManager(app)

    from project_watchlist import watchlist_api
    from project_watchlist import auth
    from project_watchlist.utils import (UserConverter,
                                         WatchlistConverter,
                                         ContentConverter,
                                         jwt_user_identity_loader,
                                         jwt_user_lookup_loader)
    # register loaders for JWT
    jwt_manager.user_identity_loader(jwt_user_identity_loader)
    jwt_manager.user_lookup_loader(jwt_user_lookup_loader)
    # register converters
    app.url_map.converters["user"] = UserConverter
    app.url_map.converters["watchlist"] = WatchlistConverter
    app.url_map.converters["content"] = ContentConverter
    app.register_blueprint(watchlist_api.api_bp)
    app.register_blueprint(auth.auth_bp)
    return app
