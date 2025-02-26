from flask import Flask
from flask_restful import Api
from mongoengine import connect
import os
from dotenv import load_dotenv
from resources.user import UserItem

load_dotenv()
connect(host=os.getenv("MONGODB_CONNECTION_STRING"), name="db")

app = Flask(__name__)
api = Api(app)

app.url_map.converters["user"] = UserConverter
api.add_resource(UserItem, "/api/users/<user:user>/")