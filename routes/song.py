from typing import Any
from flask import Blueprint
from helpers import handle_request

bp = Blueprint("song", __name__)


# ============================
#     SONG ROUTES
# ============================


@bp.route("/song/", methods=["POST"])
def create_song() -> Any:
    return handle_request("Song", "create", ["name", "albumId"], "SongID")


@bp.route("/song/<int:song_id>", methods=["GET"])
def get_song(song_id) -> Any:
    return handle_request("Song", "get", [], "SongID", song_id)


@bp.route("/song/<int:song_id>", methods=["PUT"])
def update_song(song_id) -> Any:
    return handle_request("Song", "update", ["name", "albumId"], "SongID", song_id)


@bp.route("/song/<int:song_id>", methods=["DELETE"])
def delete_song(song_id) -> Any:
    return handle_request("Song", "delete", [], "SongID", song_id)


@bp.route("/songs/<int:song_id>/reviews", methods=["GET"])
def get_reviews_for_song(song_id) -> Any:
    return handle_request("Review", "get", ["SongID"], "ReviewID", song_id)
