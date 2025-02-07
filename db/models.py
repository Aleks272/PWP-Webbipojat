from beanie import Document, Indexed
from pydantic import Field

class Users(Document):
    person_id: Indexed(int, unique=True)
    username: str = Field(unique=True)
