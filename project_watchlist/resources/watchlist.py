from flask import Response, json, request, abort
from flask_restful import Resource
from jsonschema import validate, ValidationError
from werkzeug.exceptions import UnsupportedMediaType

from project_watchlist.models import Watchlist, Content
from project_watchlist.watchlist_api import api

def validate_content(given_ids):
    """
    Checks if all of the given content id's are present in database
    and that there are no duplicates in the list of given id's
    """
    on_list = []
    for content_id in given_ids:
        db_content = Content.objects(content_id=content_id)
        if not db_content:
            abort(400, f"Content with id {content_id} does not exist")
        if content_id in on_list:
            abort(400, f"Duplicate content id {content_id}")
        on_list.append(content_id)

class WatchlistItem(Resource):
    """
    A resource to interact with a single watchlist
    """
    def get(self, watchlist):
        """
        Get a watchlist by its id
        """
        return Response(
            json.dumps(watchlist.to_json()),
            200,
            mimetype="application/json"
        )

    def put(self, watchlist):
        """
        Modify a watchlist by giving the new data for the list in parameter watchlist.

        :param watchlist: the watchlist item to be modified
        :returns: a Response with status 200 and a success message 
        :raises UnsupportedMediaType: if the request was not JSON
        :raises HTTPException: if the request does not contain the needed fields
        """
        if not request.json:
            raise UnsupportedMediaType
        try:
            validate(request.json, WatchlistItem.json_schema())
            validate_content(request.json["content_ids"])
            watchlist.content_ids = request.json["content_ids"]
            watchlist.user_note = request.json["user_note"]
            watchlist.public_entry = request.json["public_entry"]
            watchlist.save()
            return Response(
                "Watchlist updated",
                status=200,
                mimetype="application/json"
            )
        except ValidationError as e:
            abort(400, str(e))

    def delete(self, watchlist):
        """
        Delete a given watchlist

        :param watchlist: the watchlist to be deleted
        :returns: a Response with status code 200 and a message
        """
        watchlist.delete()
        return Response(
            "Watchlist deleted",
            status=200,
            mimetype="application/json"
        )

    @staticmethod
    def json_schema():
        """
        Describes the JSON schema required for this Resource

        :returns: A dictionary containing the definion of the JSON schema
        """
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
    """
    A resource to interact with a collection of watchlists
    """
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
            raise UnsupportedMediaType
        try:
            validate(request.json, WatchlistItem.json_schema())

            #check that all content id's exist
            validate_content(request.json["content_ids"])
            
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
