from flask_restful import Resource
from werkzeug.routing import BaseConverter

class ContentConverter(BaseConverter):
    def to_python(self, value):
        db_content = Content.objects(content_id=content_id)
        if not db_content:
            raise NotFound
        return db_content
    
    def to_url(self, value):
        return str(value.content_id)

class ContentItem(Resource):

    def get(self, content):
        """
        Get content based on id
        """
    
    def post(self):
        """
        Create a new content entry
        """