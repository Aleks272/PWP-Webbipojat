"""
This module contains the definitions for database models.
"""
from enum import Enum
from mongoengine import (Document,
                         StringField,
                         BooleanField,
                         SequenceField,
                         EnumField,
                         IntField,
                         ListField)

class Users(Document):
    """
    A Document that represents an API user
    """
    person_id = SequenceField()
    username = StringField(unique=True)
    email = StringField(unique=True)
    password_hash = StringField()

    def to_json(self):
        """
        Transforms this object into a JSON-ready dictionary

        :returns: a dictionary with key-value pairs representing the fields and their values
        """
        return {
                "username": self.username,
                "email": self.email,
                "person_id": self.person_id
            }

class ContentType(Enum):
    """
    Enum that defines the type of a Content item
    """
    MOVIE = 'movie'
    SERIES = 'series'

class Content(Document):
    """
    A Document that represents a piece of Content (movie or series)
    """
    content_id = SequenceField()
    name = StringField(unique=True)
    content_type = EnumField(ContentType)

    def to_json(self):
        """
        Transforms this object into a JSON-ready dictionary

        :returns: a dictionary with key-value pairs representing the fields and their values
        """
        return {
            "content_id": self.content_id,
            "name": self.name,
            "content_type": self.content_type.name
        }

class FollowerList(Document):
    """
    A Document that keeps track of who follows who
    """
    person_id = IntField()
    following_id = IntField()
    meta = {
        'indexes': [
            {'fields': ('person_id', 'following_id'), 'unique': True}
        ]
    }

class Watchlist(Document):
    """
    A Document that represents a list of Content items, which belongs to a single user
    """
    watchlist_id = SequenceField()
    user_note = StringField()
    public_entry = BooleanField()
    person_id = IntField()
    content_ids = ListField(IntField())

    def to_json(self):
        """
        Transforms this object into a JSON-ready dictionary

        :returns: a dictionary with key-value pairs representing the fields and their values
        """
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
