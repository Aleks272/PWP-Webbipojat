from flask import Response, request, abort, url_for
from flask_restful import Resource
from jsonschema import validate, ValidationError
from werkzeug.exceptions import NotFound, Conflict, BadRequest, UnsupportedMediaType
from werkzeug.routing import BaseConverter

class UserItem(Resource):
    def get(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


class UserCollection(Resource):
    def get(self):
        pass

    def post(self, user):
        if not request.json:
            abort(415, "unsupported media type")