from flask import Response, json, request, abort, url_for
from flask_restful import Resource
from jsonschema import validate, ValidationError
from werkzeug.exceptions import NotFound, Conflict, BadRequest, UnsupportedMediaType
from werkzeug.routing import BaseConverter

from project_watchlist.models import Watchlist, Users, Content

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
            raise NotFound("User not found")
        
        person_id = user.person_id
        watchlist_entries = Watchlist.objects(person_id=person_id)

        user_content_ids = []
        for entry in watchlist_entries:
            user_content_ids.append(entry.content_id)

        user_content = Content.objects(content_id__in=user_content_ids)

        watchlist = []
        for content in user_content:
            watchlist.append(
                {
                    "content": content.name,
                    "content_type": content.content_type
                }
            )

        response_body = {
            "user": user.username,
            "Watchlist": watchlist
        }
        return Response(json.dumps(response_body), 200, mimetype="application/json")

    def post(self):
        pass