from models import Users, Content, FollowerList, Publiclist, Privatelist

# Example: Adding a user
new_user = Users(person_id=1, username="john_doe")
new_user.insert()

# Example: Adding content
new_content = Content(content_id=1, name="Inception", type="movie")
new_content.insert()

# Example: Adding a follower
new_follower = FollowerList(person_id=1, following_id=2)
new_follower.insert()

# Example: Adding to public list
new_publiclist = Publiclist(person_id=1, content_id=1, user_note="Great movie!")
new_publiclist.insert()

# Example: Adding to private list
new_privatelist = Privatelist(person_id=1, content_id=1, user_note="Watch again")
new_privatelist.insert()