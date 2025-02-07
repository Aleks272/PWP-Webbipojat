from mongoengine import Document, StringField, SequenceField, EnumField, connect
from enum import Enum

class Users(Document):
    person_id: SequenceField()
    username: StringField(unique=True)

class ContentType(Enum):
    movie = "movie"
    series = "series"

class Content(Document):
    content_id: SequenceField()
    name: StringField(unique=True)
    content_type: EnumField(ContentType, default=ContentType.movie)
