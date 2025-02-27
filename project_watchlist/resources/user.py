from flask import Response, json, request, abort, url_for
from flask_restful import Resource
from jsonschema import validate, ValidationError
from werkzeug.exceptions import NotFound, Conflict, BadRequest, UnsupportedMediaType
from werkzeug.routing import BaseConverter
from project_watchlist.models import Users
import mongoengine
from project_watchlist.watchlist_api import api

class UserConverter(BaseConverter):

    def to_python(self, value):
        db_user = Users.objects(person_id=value).first()
        if db_user is None:
            raise NotFound
        return db_user

    def to_url(self, value):
        return str(value.person_id)

class UserItem(Resource):
    def get(self, username):
        db_user = Users.objects(username=username).first()
        if db_user is None:
            raise NotFound
        return Response(json.dumps({
                "username": db_user.username
            }),
            200,
            mimetype="application/json"
        )
    def put(self, username):
        if not request.json:
            raise UnsupportedMediaType
        try:
            validate(request.json, UserItem.json_schema())
            db_user = Users.objects(username=username).first()
            if db_user is None:
                raise NotFound
            db_user.username = request.json["username"]
            db_user.save()
            return Response(
                "User updated",
                status=200,
                mimetype="application/json"
            )
        except ValidationError as e:
            abort(400, str(e))
        except KeyError:
            abort(400, "Incomplete request - missing fields")
        except mongoengine.ValidationError:
            abort(400, "Database validation error")

    def delete(self, username):
        db_user = Users.objects(username=username).first()
        if db_user is None:
            raise NotFound
        db_user.delete()
        return Response(
            "User deleted",
            status=200,
            mimetype="application/json"
        )

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
        body = {"users": []}
        for db_user in Users.objects():
            item = {
                "username": db_user.username}
            body["users"].append(item)
            
        return Response(json.dumps(body), 200, mimetype="application/json")

    def post(self):
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
                headers={"Location": api.url_for(
                    UserItem,
                    user=new_User
                    )
                }
            )
        except ValidationError as e:
            abort(400, str(e))
        except KeyError:
            abort(400, "Incomplete request - missing fields")
        except mongoengine.ValidationError:
            abort(400, "Database validation error")
        except mongoengine.NotUniqueError:
            abort(400, "User already exists")
