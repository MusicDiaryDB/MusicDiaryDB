from typing import Any
from flask import Blueprint
from helpers import handle_request

bp = Blueprint("artist", __name__)

# ============================
#     ARTIST ROUTES
# ============================


@bp.route("/artist/", methods=["POST"])
def create_artist() -> Any:
    return handle_request("Artist", "create", ["name"], "ArtistID")


@bp.route("/artist/<int:artist_id>", methods=["GET"])
def get_artist(artist_id) -> Any:
    return handle_request("Artist", "get", [], "ArtistID", artist_id)


@bp.route("/artist/<string:name>", methods=["GET"])
def get_artist_by_name(name) -> Any:
    return handle_request("Artist", "get", [], "Name", name)


@bp.route("/artist/<int:artist_id>", methods=["PUT"])
def update_artist(artist_id) -> Any:
    return handle_request("Artist", "update", ["name"], "ArtistID", artist_id)


@bp.route("/artist/<int:artist_id>", methods=["DELETE"])
def delete_artist(artist_id) -> Any:
    return handle_request("Artist", "delete", [], "ArtistID", artist_id)
