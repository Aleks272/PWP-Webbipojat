from flask import Response, json, request, abort, url_for
from flask_restful import Resource
from jsonschema import validate, ValidationError
from werkzeug.exceptions import NotFound, Conflict, BadRequest, UnsupportedMediaType
from werkzeug.routing import BaseConverter

from project_watchlist.models import Watchlist, Users, Content

class WatchlistConverter(BaseConverter):
    def to_python(self, value):
        db_watchlist = Content.objects(content_id=value).first()
        if db_watchlist is None:
            raise NotFound
        return db_watchlist

    def to_url(self, value):
        return str(value.watchlist_id)

class WatchlistItem(Resource):
    def get(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass

    @staticmethod
    def json_schema():
        pass

class WatchlistCollection(Resource):

    def get(self, user):
        """
        Get all user's watchlists
        """
        person_id = user.person_id
        # get all lists with user's id
        watchlists = Watchlist.objects(person_id=person_id)
        response = {
            "watchlists": []
        }
        # Constructing the response, run through all lists
        for watchlist in watchlists:
            # Transforming the list to JSON and adding to response
            response["watchlists"].append(watchlist.to_json())
        return Response(json.dumps(response),
                        200, 
                        mimetype="application/json")

    def post(self, user):
        if not request.json:
            abort(415, "unsupported media type")
        if user is None:
            abort(400, "User not found")
        