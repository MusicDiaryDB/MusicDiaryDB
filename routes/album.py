from typing import Any
from flask import Blueprint
from helpers import handle_request

bp = Blueprint("album", __name__)

# ============================
#     ALBUM ROUTES
# ============================


@bp.route("/album/", methods=["POST"])
def create_album() -> Any:
    return handle_request("Album", "create", ["name", "artistId"], "AlbumID")


@bp.route("/album/<int:album_id>", methods=["GET"])
def get_album(album_id) -> Any:
    return handle_request("Album", "get", [], "AlbumID", album_id)


@bp.route("/album/<string:name>", methods=["GET"])
def get_album_by_name(name) -> Any:
    return handle_request("Album", "get", [], "Name", name)


@bp.route("/album/<int:album_id>", methods=["PUT"])
def update_album(album_id) -> Any:
    return handle_request("Album", "update", ["name", "artistId"], "AlbumID", album_id)


@bp.route("/album/<int:album_id>", methods=["DELETE"])
def delete_album(album_id) -> Any:
    return handle_request("Album", "delete", [], "AlbumID", album_id)
