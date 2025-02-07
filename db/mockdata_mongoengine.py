from models_mongoengine import Users, Content, FollowerList, PublicList, PrivateList

users = [
    Users(username="John Doe").validate(),
    Users(username="Foo Bar").validate(),
    Users(username="Elon Musk").validate()
]
Users.objects.insert(users)

contents = [
    Content(name="Inception", content_type="movie").validate(),
    Content(name="Deadpool", content_type="movie").validate()
]

Content.objects.insert(contents)