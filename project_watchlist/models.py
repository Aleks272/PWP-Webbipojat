import os
from mongoengine import Document, StringField, BooleanField, SequenceField, EnumField, IntField, connect, ValidationError
from enum import Enum
from dotenv import load_dotenv
load_dotenv()

connect(host=os.getenv("MONGODB_CONNECTION_STRING"), name="db")

class Users(Document):
    person_id = SequenceField()
    username = StringField(unique=True)

class ContentType(Enum):
    MOVIE = 'movie'
    SERIES = 'series'

class Content(Document):
    content_id = SequenceField()
    name = StringField(unique=True)
    content_type = EnumField(ContentType)

class FollowerList(Document):
    person_id = IntField()
    following_id = IntField()
    meta = {
        'indexes': [
            {'fields': ('person_id', 'following_id'), 'unique': True}
        ]
    }

class Watchlist(Document):
    user_note = StringField()
    public_entry = BooleanField()
    person_id = IntField()
    content_id = IntField()
    meta = {
        'indexes': [
            {'fields': ('person_id', 'content_id'), 'unique': True}
        ]
    }
