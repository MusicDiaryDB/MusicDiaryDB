from typing import Any
from flask import Blueprint, jsonify, request
from helpers import execute_query_ret_result, handle_request

bp = Blueprint("song", __name__)


# ============================
#     SONG ROUTES
# ============================


@bp.route("/song/", methods=["POST"])
def create_song() -> Any:
    return handle_request("Song", "create", ["name", "albumId"], "SongID")


@bp.route("/song/<string:album_name>", methods=["POST"])
def create_song_by_album_name(album_name: str) -> Any:
    print(request)
    data = request.form
    song_name = data.get("name")

    if not song_name:
        return jsonify({"error": "Missing song name"}), 400

    album_query = """SELECT "AlbumID" FROM "Album" WHERE "Name" = %s"""
    res, _ = execute_query_ret_result(album_query, (album_name,))

    if not res:
        return jsonify({"error": f"Album '{album_name}' not found"}), 404

    album_id = res.get_json()["result"][0].get("AlbumID")

    query = """INSERT INTO "Song" ("Name", "AlbumID") VALUES (%s, %s)"""
    return execute_query_ret_result(query, (song_name, album_id))


@bp.route("/song/<int:song_id>", methods=["GET"])
def get_song(song_id) -> Any:
    return handle_request("Song", "get", [], "SongID", song_id)


@bp.route("/song/<string:name>", methods=["GET"])
def get_song_by_name(name) -> Any:
    return handle_request("Song", "get", [], "Name", name)


@bp.route("/song/<int:song_id>", methods=["PUT"])
def update_song(song_id) -> Any:
    return handle_request("Song", "update", ["name", "albumId"], "SongID", song_id)


@bp.route("/song/<int:song_id>", methods=["DELETE"])
def delete_song(song_id) -> Any:
    return handle_request("Song", "delete", [], "SongID", song_id)


@bp.route("/songs/<int:song_id>/reviews", methods=["GET"])
def get_reviews_for_song(song_id) -> Any:
    return handle_request("Review", "get", ["SongID"], "ReviewID", song_id)
