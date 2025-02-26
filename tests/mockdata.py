from models import Users, Content, FollowerList, PublicList, PrivateList, ContentType

users = [
    Users(username="John Doe"),
    Users(username="Foo Bar"),
    Users(username="Elon Musk")
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

person = Users.objects(username="John Doe").first().person_id
following = Users.objects(username="Elon Musk").first().person_id

new_follow = FollowerList(person_id=person, following_id=following)
new_follow.save()

#another following
person = Users.objects(username="Foo Bar").first().person_id
following = Users.objects(username="Elon Musk").first().person_id

new_follow = FollowerList(person_id=person, following_id=following)
new_follow.save()

#third following
person = Users.objects(username="Elon Musk").first().person_id
following = Users.objects(username="Foo Bar").first().person_id

new_follow = FollowerList(person_id=person, following_id=following)
new_follow.save()

#PublicList
person = Users.objects(username="Elon Musk").first().person_id
content = Content.objects(name="Breaking Bad").first().content_id
new_entry = PublicList(person_id=person, content_id=content, user_note="ok")
new_entry.save()

#PublicList2
person = Users.objects(username="Elon Musk").first().person_id
content = Content.objects(name="Inception").first().content_id
new_entry = PublicList(person_id=person, content_id=content, user_note="Not ok")
new_entry.save()

#PrivateList
person = Users.objects(username="Elon Musk").first().person_id
content = Content.objects(name="Deadpool").first().content_id
new_entry = PrivateList(person_id=person, content_id=content, user_note="Not ok")
new_entry.save()

#PrivateList2
person = Users.objects(username="Elon Musk").first().person_id
content = Content.objects(name="Inception").first().content_id
new_entry = PrivateList(person_id=person, content_id=content, user_note="Tesla Model SS")
new_entry.save()
