from mongoengine import Document, StringField, SequenceField, EnumField, IntField, connect
from enum import Enum

class Users(Document):
    person_id = SequenceField()
    username = StringField(unique=True)

class ContentType(Enum):
    movie = "movie"
    series = "series"

class Content(Document):
    content_id = SequenceField()
    name = StringField(unique=True)
    content_type = EnumField(ContentType, default=ContentType.movie)

class FollowerList(Document):
    person_id = IntField()
    following_id = IntField()
    meta = {
        'indexes': [
            {'fields': ('person_id', 'following_id'), 'unique': True}
        ]
    }

class PublicList(Document):
    user_note = StringField()
    person_id = IntField()
    content_id = IntField()
    meta = {
        'indexes': [
            {'fields': ('person_id', 'content_id'), 'unique': True}
        ]
    }

class PrivateList(Document):
    user_note = StringField()
    person_id = IntField()
    content_id = IntField()
    meta = {
        'indexes': [
            {'fields': ('person_id', 'content_id'), 'unique': True}
        ]
    }
