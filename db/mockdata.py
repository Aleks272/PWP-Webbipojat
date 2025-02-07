from models import Users, Content, FollowerList, Publiclist, Privatelist

users = [
    Users(username="John Doe"),
    Users(username="Foo Bar"),
    Users(username="Elon Musk")
]
for user in users:
    user.insert()

content = [
    Content(content_id=1, name="Inception", type="movie"),
    Content(content_id=2, name="Deadpool", type="movie")
]
Content.insert_many(content)


# new_follower = FollowerList(person_id=1, following_id=3)
# new_follower.insert()

# new_publiclist = Publiclist(person_id=1, content_id=1, user_note="Great movie!")
# new_publiclist.insert()

# new_privatelist = Privatelist(person_id=3, content_id=1, user_note="LIT AF")
# new_privatelist.insert()
