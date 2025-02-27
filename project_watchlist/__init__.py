from flask import Flask
from mongoengine import connect
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    connect(host=os.getenv("MONGODB_CONNECTION_STRING"), name="db")

    return app