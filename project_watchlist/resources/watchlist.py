from flask import Response, request, abort, url_for
from flask_restful import Resource
from jsonschema import validate, ValidationError
from werkzeug.exceptions import NotFound, Conflict, BadRequest, UnsupportedMediaType
from werkzeug.routing import BaseConverter

from project_watchlist.models import Watchlist, Users

class WatchlistItem(Resource):
    def get(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


class WatchlistCollection(Resource):
    def get(self, user):
        if user is None:
            raise NotFound
        person_id = user.person_id

    def post(self):
        pass