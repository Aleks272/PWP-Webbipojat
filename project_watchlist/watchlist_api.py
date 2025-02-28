from flask import Flask
from flask_restful import Api
from mongoengine import connect
import os
from dotenv import load_dotenv

load_dotenv()
connect(host=os.getenv("MONGODB_CONNECTION_STRING"), name="test_db")

app = Flask(__name__)
api = Api(app)

from project_watchlist.resources.user import UserItem, UserConverter, UserCollection
from project_watchlist.resources.watchlist import WatchlistCollection

app.url_map.converters["user"] = UserConverter
api.add_resource(UserItem, "/api/users/<user:user>/")
api.add_resource(UserCollection, "/api/users/")
api.add_resource(WatchlistCollection, "/api/users/<user:user>/watchlist/")
