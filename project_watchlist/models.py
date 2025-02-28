import json
from mongoengine import Document, StringField, BooleanField, SequenceField, EnumField, IntField, ValidationError, ListField
from enum import Enum

class Users(Document):
    person_id = SequenceField()
    username = StringField(unique=True)
    email = StringField(unique=True)

    def to_json(self):
        return json.dumps(
            {
                "username": self.username,
                "email": self.email,
                "person_id": self.person_id
            }
        )

class ContentType(Enum):
    MOVIE = 'movie'
    SERIES = 'series'

class Content(Document):
    content_id = SequenceField()
    name = StringField(unique=True)
    content_type = EnumField(ContentType)

    def to_json(self):
        return {
            "content_id": self.content_id,
            "name": self.name,
            "content_type": self.content_type.name
        }

class FollowerList(Document):
    person_id = IntField()
    following_id = IntField()
    meta = {
        'indexes': [
            {'fields': ('person_id', 'following_id'), 'unique': True}
        ]
    }

class Watchlist(Document):
    watchlist_id = SequenceField()
    user_note = StringField()
    public_entry = BooleanField()
    person_id = IntField()
    content_ids = ListField(IntField())

    def to_json(self):
        doc = {
            "watchlist_id": self.watchlist_id,
            "user_note": self.user_note,
            "person_id": self.person_id,
            "content": []
        }
        for content_id in self.content_ids:
            content = Content.objects(content_id=content_id).first()
            doc["content"].append(content.to_json())
        return doc
