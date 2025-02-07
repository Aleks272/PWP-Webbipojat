from models_mongoengine import Users, Content, FollowerList, PublicList, PrivateList

users = [
    Users(username="John Doe"),
    Users(username="Foo Bar"),
    Users(username="Elon Musk")
]
Users.objects.insert(users)

contents = [
    Content(name="Inception", content_type="movie"),
    Content(name="Deadpool", content_type="movie")
]

Content.objects.insert(contents)