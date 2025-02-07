import os
from enum import Enum
from bunnet import Document, Indexed, init_bunnet
from pydantic import Field
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

class Users(Document):
    person_id: Indexed[int] = Indexed(unique=True)
    username: str = Field(unique=True)

class ContentTypeEnum(str, Enum):
    movie: 'movie'
    series: 'series'

class Content(Document):
    content_id: Indexed[int] = Indexed(unique=True)
    name: str = Field(unique=True)
    type: ContentTypeEnum

class FollowerList(Document):
    person_id: Indexed[int] = Indexed(unique=True)
    FollowingId: Indexed[int] = Indexed(unique=True)

class Publiclist(Document):
    person_id: int = Field(index=True, unique=True)
    content_id: int = Field(index=True, unique=True)
    user_note: str = Field(unique=True)

class Privatelist(Document):
    person_id: int = Field(index=True, unique=True)
    content_id: int = Field(index=True, unique=True)
    user_note: str = Field(unique=True)

client = MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))
init_bunnet(database=client.db_name, document_models=[Users])
