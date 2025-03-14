from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

from project_watchlist.resources.user import UserItem, UserCollection
from project_watchlist.resources.watchlist import WatchlistItem, PrivateWatchlistCollection, PublicWatchlistCollection
from project_watchlist.resources.content import ContentItem, ContentCollection

api.add_resource(UserItem, "/users/<user:user>/")
api.add_resource(UserCollection, "/users/")
api.add_resource(PrivateWatchlistCollection, "/users/<user:user>/watchlists/private/")
api.add_resource(PublicWatchlistCollection, "/users/<user:user>/watchlists/public/")
api.add_resource(WatchlistItem, "/watchlists/<watchlist:watchlist>/")
api.add_resource(ContentItem, "/content/<content:content>/")
api.add_resource(ContentCollection, "/content/")
