from werkzeug.routing import BaseConverter
from werkzeug.exceptions import NotFound

from project_watchlist.models import Users, Content, Watchlist

class UserConverter(BaseConverter):
    # Fetch user item from database by username
    def to_python(self, value):
        db_user = Users.objects(username=value).first()
        if db_user is None:
            raise NotFound
        return db_user
    # Convert username to URL
    def to_url(self, value):
        return str(value.username)

class ContentConverter(BaseConverter):
    def to_python(self, value):
        db_content = Content.objects(content_id=int(value)).first()
        if db_content is None:
            raise NotFound
        return db_content
    
    def to_url(self, value):
        return str(value.content_id)

class WatchlistConverter(BaseConverter):
    def to_python(self, value):
        db_watchlist = Watchlist.objects(watchlist_id=value).first()
        if db_watchlist is None:
            raise NotFound
        return db_watchlist

    def to_url(self, value):
        return str(value.watchlist_id)