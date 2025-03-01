from flask import Flask
from mongoengine import connect
import os
from dotenv import load_dotenv

load_dotenv()

def create_app(test_mode=False):
    app = Flask(__name__)
    db_name = "db"
    if test_mode:
        db_name = "test-db"
    connect(host=os.getenv("MONGODB_CONNECTION_STRING"), name=db_name)

    return app