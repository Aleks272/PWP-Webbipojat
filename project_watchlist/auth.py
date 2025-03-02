"""
This module provides routes for user authentication with JWT
"""
from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from werkzeug.exceptions import BadRequest, UnsupportedMediaType
from project_watchlist.models import Users

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["POST"])
def login():
    if request.json is None:
        raise UnsupportedMediaType()
    try:
        username = request.json["username"]
        password = request.json["password"]
    except KeyError as ke:
        raise BadRequest("username and password required") from ke
