"""
This module defines resources for watchlist
"""
from flask import Response, json, request, abort
from flask_restful import Resource, url_for
from jsonschema import validate, ValidationError
from werkzeug.exceptions import UnsupportedMediaType, Unauthorized
from flask_jwt_extended import current_user, jwt_required

from project_watchlist.models import Watchlist, Content

def validate_content(given_ids):
    """
    Checks if all of the given content id's are present in database
    and that there are no duplicates in the list of given id's
    """
    on_list = []
    for content_id in given_ids:
        #pylint: disable=no-member
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
        if request.content_type != "application/json":
            raise UnsupportedMediaType
        try:
            validate(request.json, WatchlistItem.json_schema())
            validate_content(request.json["content_ids"])
            watchlist.content_ids = request.json["content_ids"]
            watchlist.user_note = request.json["user_note"]
            watchlist.public_entry = request.json["public_entry"]
            watchlist.save()
            return Response(status=204)
        except ValidationError as e:
            abort(400, str(e))

    def delete(self, watchlist):
        """
        Delete a given watchlist

        :param watchlist: the watchlist to be deleted
        :returns: a Response with status code 200 and a message
        """
        watchlist.delete()
        return Response(status=204)

    @staticmethod
    def json_schema():
        """
        Describes the JSON schema required for this Resource

        :returns: A dictionary containing the definion of the JSON schema
        """
        schema = {
            "type": "object",
            "required": ["content_ids",
                         "user_note"]
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
        return schema

class PublicWatchlistCollection(Resource):
    """
    A resource class for interacting with public watchlists of the user
    """
    def get(self, user):
        """
        Get all user's public watchlists
        """
        person_id = user.person_id
        # get all lists with user's id
        #pylint: disable=no-member
        watchlists = Watchlist.objects(person_id=person_id, public_entry=True)
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

    @jwt_required()
    def post(self, user):
        """
        Create a new public watchlist for the user
        """
        if request.content_type != "application/json":
            raise UnsupportedMediaType
        if not user.person_id == current_user.person_id:
            raise Unauthorized("Your are not authorized to create lists for this user")
        try:
            validate(request.json, WatchlistItem.json_schema())

            #check that all content id's exist
            validate_content(request.json["content_ids"])

            new_watchlist = Watchlist(
                user_note=request.json["user_note"],
                public_entry=True,
                person_id=user.person_id,
                content_ids=request.json["content_ids"]
                )
            #pylint: disable=no-member
            Watchlist.objects.insert(new_watchlist)
            return Response(
                "New watchlist added", 
                status=201,
                mimetype="application/json",
                headers={"Location": url_for(
                    "api.watchlistitem",
                    watchlist=new_watchlist
                    )
                }
            )
        except ValidationError as e:
            abort(400, str(e))

class PrivateWatchlistCollection(Resource):
    """
    Resource class for interacting with private watchlists
    """
    @jwt_required()
    def get(self, user):
        """
        Get private watchlists for the user

        :returns: a Response with user's private watchlists
        :raises: Unauthorized if the authenticated user is not the same as
                 the owner of these watchlists
        """
        # if identified user is the same as the user in the URL...
        if current_user.person_id == user.person_id:
            # we can return all private watchlists for that user
            #pylint: disable=no-member
            private_watchlists = Watchlist.objects(person_id=user.person_id, public_entry=False)
            response = {
                "watchlists": []
            }
            for private_watchlist in private_watchlists:
                response["watchlists"].append(private_watchlist.to_json())
            return Response(json.dumps(response),
                        200,
                        mimetype="application/json")
        # if the user is wrong, respond with Unauthorized
        raise Unauthorized("You are not authorized to view these watchlists")

    @jwt_required()
    def post(self, user):
        """
        Create a new private watchlist for the user
        """
        if request.content_type != "application/json":
            raise UnsupportedMediaType
        if not user.person_id == current_user.person_id:
            raise Unauthorized("Your are not authorized to create lists for this user")
        try:
            validate(request.json, WatchlistItem.json_schema())

            #check that all content id's exist
            validate_content(request.json["content_ids"])

            new_watchlist = Watchlist(
                user_note=request.json["user_note"],
                public_entry=False,
                person_id=user.person_id,
                content_ids=request.json["content_ids"]
                )
            #pylint: disable=no-member
            Watchlist.objects.insert(new_watchlist)
            return Response(
                "New watchlist added", 
                status=201,
                mimetype="application/json",
                headers={"Location": url_for(
                    "api.watchlistitem",
                    watchlist=new_watchlist
                    )
                }
            )
        except ValidationError as e:
            abort(400, str(e))
