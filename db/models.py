from beanie import Document, Indexed

class Users(Document):
    person_id: Indexed(int, unique=True)
    username: str
