import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from project_watchlist.models import Users, Content, FollowerList, Watchlist, ContentType

from mongoengine import connect
import os
from dotenv import load_dotenv
import bcrypt

#

# Populates the database with mock data
def populate(test_mode=False):

    if not test_mode:
        load_dotenv()
        connect(host=os.getenv("MONGODB_CONNECTION_STRING"), name="db")

    example_password = "password"
    salt = bcrypt.gensalt()
    example_hash = bcrypt.hashpw(example_password.encode('utf-8'), salt)
    users = [
        Users(username="johndoe", email="john.doe@gmail.com", password_hash=example_hash),
        Users(username="foobar", email="foobar@icloud.com", password_hash=example_hash),
        Users(username="elonmusk", email="presidentmusk@whatdidyoudothisweek.gov", password_hash=example_hash)
    ]
    for user in users:
        user.validate()
    Users.objects.insert(users)

    contents = [
        Content(name="Inception", content_type=ContentType.MOVIE),
        Content(name="Deadpool", content_type=ContentType.MOVIE),
        Content(name="Breaking Bad", content_type=ContentType.SERIES)
    ]
    for content in contents:
        content.validate()
    Content.objects.insert(contents)

    person = Users.objects(username="johndoe").first().person_id
    following = Users.objects(username="elonmusk").first().person_id

    new_follow = FollowerList(person_id=person, following_id=following)
    new_follow.save()

    #another following
    person = Users.objects(username="foobar").first().person_id
    following = Users.objects(username="elonmusk").first().person_id

    new_follow = FollowerList(person_id=person, following_id=following)
    new_follow.save()

    #third following
    person = Users.objects(username="elonmusk").first().person_id
    following = Users.objects(username="foobar").first().person_id

    new_follow = FollowerList(person_id=person, following_id=following)
    new_follow.save()


    #WatchlistPublic1
    person = Users.objects(username="elonmusk").first().person_id
    content = Content.objects(name="Breaking Bad").first().content_id
    new_entry = Watchlist(person_id=person, content_ids={content}, user_note="ok", public_entry=True)
    new_entry.save()

    #WatchlistPublic2
    person = Users.objects(username="elonmusk").first().person_id
    content = Content.objects(name="Inception").first().content_id
    content_2 = Content.objects(name="Deadpool").first().content_id
    new_entry = Watchlist(person_id=person, content_ids={content, content_2}, user_note="Not ok", public_entry=True)
    new_entry.save()

    #WatchlistPrivate1
    person = Users.objects(username="elonmusk").first().person_id
    content = Content.objects(name="Deadpool").first().content_id
    new_entry = Watchlist(person_id=person, content_ids={content}, user_note="Not ok", public_entry=False)
    new_entry.save()

    #WatchlistPrivate2
    person = Users.objects(username="johndoe").first().person_id
    content = Content.objects(name="Inception").first().content_id
    new_entry = Watchlist(person_id=person, content_ids={content}, user_note="Tesla Model SS", public_entry=False)
    new_entry.save()

if __name__=="__main__":
    print("populating...")
    populate()
