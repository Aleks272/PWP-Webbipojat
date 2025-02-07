import os
from enum import Enum
from bunnet import Document, init_bunnet, before_event, Insert
from pydantic import Field
from pymongo import MongoClient
from typing import Optional
from dotenv import load_dotenv
load_dotenv()

class Counter(Document):
    collection_name: str
    amount: int

def get_next_index(collection):
    counter = Counter.find_one(Counter.collection_name==collection).run()
    if counter:
        counter.amount += 1
        counter.save()
    else:
        counter = Counter(collection_name=collection, amount=1)
        counter.insert()
    return counter.amount

class Users(Document):
    person_id: Optional[int] = Field(index=True, unique=True, default=None)
    username: str = Field(unique=True)

    class Settings:
        collection = "users"

    @before_event(Insert)
    def set_id(self):
        self.person_id = get_next_index("users")


class ContentTypeEnum(str, Enum):
    movie = "movie"
    series = "series"

class Content(Document):
    content_id: int = Field(index=True, unique=True)
    name: str = Field(unique=True)
    type: ContentTypeEnum

class FollowerList(Document):
    person_id: int = Field(index=True, unique=True)
    following_id: int = Field(index=True, unique=True)

class Publiclist(Document):
    person_id: int = Field(index=True, unique=True)
    content_id: int = Field(index=True, unique=True)
    user_note: str = Field(unique=False)

class Privatelist(Document):
    person_id: int = Field(index=True, unique=True)
    content_id: int = Field(index=True, unique=True)
    user_note: str = Field(unique=False)

client = MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))
init_bunnet(database=client.db_name, document_models=[Users, Content, FollowerList, Publiclist, Privatelist, Counter])
