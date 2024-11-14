from typing import Any
from flask import Blueprint, request, jsonify
from helpers import execute_query_ret_result, handle_request

bp = Blueprint("album", __name__)

# ============================
#     ALBUM ROUTES
# ============================


@bp.route("/album/", methods=["POST"])
def create_album() -> Any:
    return handle_request("Album", "create", ["name", "artistId"], "AlbumID")


@bp.route("/album/<string:artist_name>", methods=["POST"])
def create_album_by_artist_name(artist_name) -> Any:
    data = request.form
    album_name = data.get("name")

    if not album_name:
        return jsonify({"error": "Missing album name"}), 400

    artist_query = """SELECT "ArtistID" FROM "Artist" WHERE "Name" = %s"""
    res, _ = execute_query_ret_result(artist_query, (artist_name,))

    if not res:
        return jsonify({"error": f"Artist '{artist_name}' not found"}), 404
    artist_id = res.get_json()["result"][0].get("ArtistID")

    query = """INSERT INTO "Album" ("Name", "ArtistID") VALUES (%s, %s)"""
    return execute_query_ret_result(query, (album_name, artist_id))


@bp.route("/album/<int:album_id>", methods=["GET"])
def get_album(album_id) -> Any:
    return handle_request("Album", "get", [], "AlbumID", album_id)


@bp.route("/album/<string:name>", methods=["GET"])
def get_album_by_name(name) -> Any:
    res, status = handle_request("Album", "get", [], "Name", name)
    if res is not None:
        print(res.get_json()["ArtistID"])
    return res, status


@bp.route("/album/<int:album_id>", methods=["PUT"])
def update_album(album_id) -> Any:
    return handle_request("Album", "update", ["name", "artistId"], "AlbumID", album_id)


@bp.route("/album/<int:album_id>", methods=["DELETE"])
def delete_album(album_id) -> Any:
    return handle_request("Album", "delete", [], "AlbumID", album_id)
