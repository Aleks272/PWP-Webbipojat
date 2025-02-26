from flask import Response, request, abort, url_for
from flask_restful import Resource
from jsonschema import validate, ValidationError
from werkzeug.exceptions import NotFound, Conflict, BadRequest, UnsupportedMediaType
from werkzeug.routing import BaseConverter
from models import Users
import mongoengine

class UserConverter(BaseConverter):

    def to_python(self, value):
        db_user = Users.objects(person_id=value).first()
        if db_user is None:
            raise NotFound
        return db_user

    def to_url(self, value):
        return str(value.person_id)

class UserItem(Resource):
    def get(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass

    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["username"]
        }
        properties = schema["properties"] = {}
        properties["username"] = {
            "description": "Username",
            "type": "string"
        }
        return schema

class UserCollection(Resource):
    def get(self):
        pass

    def post(self, user):
        if not request.json:
            abort(415, "unsupported media type")
        try:
            validate(request.json, UserItem.json_schema())
            new_User = Users(
                username=request.json["username"]
            )
            Users.objects.insert(new_User)
            return Response(
                "New user added", 
                status=201, 
                mimetype="application/json",
                headers={"Location": url_for(
                    "api.useritem", 
                    person_id=new_User.person_id
                    )
                }
            )
        except ValidationError as e:
            abort(400, str(e))
        except KeyError:
            abort(400, "Incomplete request - missing fields")
        except mongoengine.ValidationError:
            abort(400, "Database validation error")
