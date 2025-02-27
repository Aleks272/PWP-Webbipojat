from flask import Response, json, request, abort, url_for
from flask_restful import Resource
from jsonschema import validate, ValidationError
from werkzeug.exceptions import NotFound, Conflict, BadRequest, UnsupportedMediaType
from werkzeug.routing import BaseConverter
from project_watchlist.models import Users
import mongoengine
from project_watchlist.watchlist_api import api

class UserConverter(BaseConverter):
    # Fetch user item from database by username
    def to_python(self, value):
        db_user = Users.objects(username=value).first()
        if db_user is None:
            raise NotFound
        return db_user
    # Convert username to URL
    def to_url(self, value):
        return str(value.username)

class UserItem(Resource):
    # api route: /api/users/<username/
    # Get user details for user provided in URL (e.g. /api/users/johndoe/) )
    def get(self, user):
        return Response(
            json.dumps(user.to_json()),
            200,
            mimetype="application/json"
        )
    # Update user details for user provided in URL (e.g. /api/users/johndoe/)
    def put(self, user):
        if not request.json:
            raise UnsupportedMediaType
        try:
            validate(request.json, UserItem.json_schema())
            user.username = request.json["username"]
            user.email = request.json["email"]
            user.save()
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

    # Delete user details for user provided in URL (e.g. /api/users/johndoe/)
    def delete(self, user):
        user.delete()
        return Response(
            "User deleted",
            status=200,
            mimetype="application/json"
        )
    # JSON schema for user details
    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["username", "email"]
        }
        properties = schema["properties"] = {}
        properties["username"] = {
            "description": "Username",
            "type": "string",
            "pattern": "^[^\\s]*$" # No whitespace allowed
        }
        properties["email"] = {
            "description": "Email",
            "type": "string",
            "pattern": "^[^\\s]*$" # No whitespace allowed
        }
        return schema

class UserCollection(Resource):
    # api route: /api/users/
    # Get all users in database
    def get(self):
        body = {"users": []}
        for db_user in Users.objects():
            item = db_user.to_json()
            body["users"].append(item)
            
        return Response(json.dumps(body), 200, mimetype="application/json")
    # Add new user to database
    def post(self):
        if not request.json:
            abort(415, "unsupported media type")
        try:
            validate(request.json, UserItem.json_schema())

            new_User = Users(
                username=request.json["username"],
                email=request.json["email"]

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
