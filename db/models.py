import os
from bunnet import Document, Indexed, init_bunnet
from pydantic import Field
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

class Users(Document):
    person_id: Indexed(int, unique=True)
    username: str = Field(unique=True)

client = MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))
init_bunnet(database=client.db_name, document_models=[Users])