"""
Resource classes for handling different types of content (movies/series)
"""
from flask import Response, json, request, abort, jsonify
from flask_restful import Resource, url_for
from jsonschema import validate, ValidationError
from werkzeug.exceptions import UnsupportedMediaType
import mongoengine

from project_watchlist.models import Content, ContentType, Watchlist

class ContentItem(Resource):
    """
    A resource to interact with a single Content item
    """
    def get(self, content):
        """
        Get content based on id
        """
        return jsonify(content.to_json())

    def put(self, content):
        """
        Update existing content
        """
        if not request.content_type == "application/json":
            raise UnsupportedMediaType
        try:
            validate(request.json, ContentItem.json_schema())
            content.name = request.json["name"]
            content.content_type = ContentType[request.json["content_type"]]
            content.save()
            return Response(status=204)
        
        except ValidationError as e:
            abort(400, str(e))

    def delete(self, content):
        """
        Delete content
        """
        # need to make sure that the content does not remain in any watchlist
        # first, we get all our existing watchlists
        #pylint: disable=no-member
        watchlists = Watchlist.objects()
        # then we loop through all the watchlists
        for watchlist in watchlists:
            # and all the content id's in that list:
            for content_id in watchlist.content_ids:
                # if this content id is the one being removed:
                if content_id == content.content_id:
                    # remove it from the watchlist and save it
                    watchlist.content_ids.remove(content_id)
                    watchlist.save()
        content.delete()
        return Response(status=204)

    @staticmethod
    def json_schema():
        """
        Describes the JSON schema for this resource

        :returns: a dictionary that contains the definition for the JSON schema
        """
        schema = {
            "type": "object",
            "required": ["name", "content_type"]
        }
        properties = schema["properties"] = {}
        properties["name"] = {
            "description": "Name of movie or series",
            "type": "string"
        }
        properties["content_type"] = {
            "description": "Type of content (MOVIE or SERIES)",
            "type": "string",
            "enum": [t.name for t in ContentType]
        }
        return schema

class ContentCollection(Resource):
    """
    A resource to interact with a collection of Content items
    """
    def get(self):
        """
        Get all content
        """
        body = {"content": []}
        #pylint: disable=no-member
        for db_content in Content.objects():
            item = db_content.to_json()
            body["content"].append(item)

        return Response(json.dumps(body), 200, mimetype="application/json")

    def post(self):
        """
        Create a new content entry
        """
        if not request.content_type == "application/json":
            raise UnsupportedMediaType
        try:
            validate(request.json, ContentItem.json_schema())

            # Convert string to enum value
            content_type = ContentType[request.json["content_type"]]

            new_content = Content(
                name=request.json["name"],
                content_type=content_type
            )
            #pylint: disable=no-member
            Content.objects.insert(new_content)
            return Response(
                "New content added", 
                status=201,
                mimetype="application/json",
                headers={"Location": url_for(
                    "api.contentitem",
                    content=new_content
                    )
                }
            )
        except ValidationError as e:
            abort(400, str(e))
        except mongoengine.NotUniqueError:
            abort(400, "Content with this name already exists")
