"""
This modules includes user-related resources
"""
from flask import Response, json, request, abort, jsonify
from flask_restful import Resource, url_for
from jsonschema import validate, ValidationError
from werkzeug.exceptions import UnsupportedMediaType, Unauthorized
import mongoengine
import bcrypt
from flask_jwt_extended import jwt_required, current_user

from project_watchlist.models import Users

class UserItem(Resource):
    """
    Resource class representing one user
    """
    def get(self, user):
        """
        api route: /api/users/<username/
        Get user details for user provided in URL (e.g. /api/users/johndoe/) )
        """
        return jsonify(user.to_json())
    @jwt_required()
    def put(self, user):
        """
        Update user details for user provided in URL (e.g. /api/users/johndoe/)
        """
        if not request.content_type == "application/json":
            raise UnsupportedMediaType
        if not current_user.person_id == user.person_id:
            raise Unauthorized
        try:
            validate(request.json, UserItem.json_schema())
            salt = bcrypt.gensalt()
            cleartext_password = request.json["password"]
            hashed_password = bcrypt.hashpw(cleartext_password.encode("utf-8"), salt)
            user.password_hash = hashed_password.decode("utf-8")
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
        except mongoengine.NotUniqueError:
            abort(400, "Database validation error")
    @jwt_required()
    def delete(self, user):
        """
        Delete user details for user provided in URL (e.g. /api/users/johndoe/)
        """
        if not current_user.person_id == user.person_id:
            raise Unauthorized
        user.delete()
        return Response(
            "User deleted",
            status=200,
            mimetype="application/json"
        )
    @staticmethod
    def json_schema():
        """
        JSON schema for user details
        """
        schema = {
            "type": "object",
            "required": ["username", "email", "password"]
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
        properties["password"] = {
            "description": "Password for user",
            "type": "string"
        }
        return schema

class UserCollection(Resource):
    """
    Resource class that represents a collection of users
    """
    def get(self):
        """
        api route: /api/users/
        Get all users in database
        """
        body = {"users": []}
        #pylint: disable=no-member
        for db_user in Users.objects():
            item = db_user.to_json()
            body["users"].append(item)

        return Response(json.dumps(body), 200, mimetype="application/json")
    def post(self):
        """
        Add new user to database
        """
        if not request.content_type == "application/json":
            raise UnsupportedMediaType
        try:
            validate(request.json, UserItem.json_schema())
            salt = bcrypt.gensalt()
            cleartext_password = request.json["password"]
            hashed_password = bcrypt.hashpw(cleartext_password.encode("utf-8"), salt)
            new_user = Users(
                username=request.json["username"],
                email=request.json["email"],
                password_hash=hashed_password
            )
            #pylint: disable=no-member
            Users.objects.insert(new_user)
            return Response(
                "New user added", 
                status=201,
                mimetype="application/json",
                headers={"Location": url_for(
                    "api.useritem",
                    user=new_user
                    )
                }
            )
        except ValidationError as e:
            abort(400, str(e))
        except mongoengine.NotUniqueError:
            abort(400, "User already exists")
