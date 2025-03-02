"""
This module provides routes for user authentication with JWT
"""
from flask import Blueprint, request, Response
from flask_jwt_extended import create_access_token
from werkzeug.exceptions import BadRequest, UnsupportedMediaType, Unauthorized, NotFound
import bcrypt
import json
from project_watchlist.models import Users

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login/", methods=["POST"])
def login():
    """
    A function that checks the user's credentials and creates an access token if
    the credentials are correct

    :returns: a Response object containing an access token
    :raises UnsupportedMediaType: if the request was not in JSON format
    :raises KeyError: if fields 'username' or 'password' were missing from the request
    :raises Unauthorized: if the user's credentials were wrong
    :raises NotFound: if the user does not exist
    """
    if request.json is None:
        raise UnsupportedMediaType()
    try:
        username = request.json["username"]
        given_password = request.json["password"]
        db_user = Users.objects(username=username).first()
        if db_user is None:
            raise NotFound(f"The user {username} does not exist")
        # convert given password to bytes and compare to hash in db
        if bcrypt.checkpw(given_password.encode("utf-8"), db_user.password_hash.encode("utf-8")):
            # checkpw returns true, hashes match
            jwt = create_access_token(db_user)
            return Response(json.dumps(
                {
                    "token": jwt
                }),
                status=200,
                mimetype="application/json"
            )
        # checkpw returns false, wrong password
        raise Unauthorized("wrong password")

    except KeyError as ke:
        raise BadRequest("username and password required") from ke
