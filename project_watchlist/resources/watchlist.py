from flask import Response, json, request, abort, url_for
from flask_restful import Resource
from jsonschema import validate, ValidationError
from werkzeug.exceptions import NotFound, Conflict, BadRequest, UnsupportedMediaType
from werkzeug.routing import BaseConverter
import mongoengine

from project_watchlist.models import Watchlist, Users, Content
from project_watchlist.watchlist_api import api

class WatchlistConverter(BaseConverter):
    def to_python(self, value):
        db_watchlist = Watchlist.objects(watchlist_id=value).first()
        if db_watchlist is None:
            raise NotFound
        return db_watchlist

    def to_url(self, value):
        return str(value.watchlist_id)

class WatchlistItem(Resource):
    def get(self, watchlist):
        """
        Get a watchlist by its id
        """
        return Response(
            json.dumps(watchlist.to_json()),
            200,
            mimetype="application/json"
        )

    def put(self):
        pass

    def delete(self):
        pass

    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["content_ids",
                         "user_note",
                         "public_entry"]
        }
        properties = schema["properties"] = {}
        properties["watchlist_id"] = {
            "description": "The id of this watchlist",
            "type": "number"
        }
        properties["person_id"] = {
            "description": "The id of the person who owns this watchlist",
            "type": "number",
        }
        properties["content_ids"] = {
            "description": "id's of the content belonging to this list",
            "type": "array",
            "items": {
                "type": "number"
            }
        }
        properties["user_note"] = {
            "description": "Note entered by user",
            "type": "string"
        }
        properties["public_entry"] = {
            "description": "Specifies whether or not this list is public",
            "type": "boolean"
        }
        return schema

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
        """
        Create a new watchlist for the user
        """
        if not request.json:
            abort(415, "unsupported media type")
        try:
            validate(request.json, WatchlistItem.json_schema())

            #check that all content id's exist
            for content_id in request.json["content_ids"]:
                db_content = Content.objects(content_id=content_id)
                if not db_content:
                    abort(400, f"Content with id {content_id} does not exist")
            
            new_watchlist = Watchlist(
                user_note=request.json["user_note"],
                public_entry=request.json["public_entry"],
                person_id=user.person_id,
                content_ids=request.json["content_ids"]
                )
            Watchlist.objects.insert(new_watchlist)
            return Response(
                "New watchlist added", 
                status=201, 
                mimetype="application/json",
                headers={"Location": api.url_for(
                    WatchlistItem,
                    watchlist=new_watchlist
                    )
                }
            )
        except ValidationError as e:
            abort(400, str(e))
        except KeyError:
            abort(400, "Incomplete request - missing fields")
        except mongoengine.ValidationError:
            abort(400, "Database validation error")