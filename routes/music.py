from typing import Any
from flask import Blueprint
from helpers import execute_query_ret_result

bp = Blueprint("music", __name__)


# ============================
#     MUSIC ROUTES (combined song/album/artist)
# ============================


@bp.route("/music/all/songs", methods=["GET"])
def get_all_songs() -> Any:
    query = """
    SELECT
        s."SongID",
        a."AlbumID",
        ar."ArtistID",
        s."Name" AS "SongName",
        a."Name" AS "AlbumName",
        ar."Name" AS "ArtistName"
    FROM "Song" s
    JOIN "Album" a ON s."AlbumID" = a."AlbumID"
    JOIN "Artist" ar ON a."ArtistID" = ar."ArtistID";
    """
    return execute_query_ret_result(query)


@bp.route("/music/all/albums", methods=["GET"])
def get_all_albums() -> Any:
    query = """
    SELECT
        a."AlbumID",
        a."Name" AS "AlbumName",
        a."ArtistID",
        ar."Name" AS "ArtistName",
        COUNT(s."SongID") AS "SongCount"
    FROM "Album" a
    JOIN "Artist" ar ON a."ArtistID" = ar."ArtistID"
    LEFT JOIN "Song" s ON a."AlbumID" = s."AlbumID"
    GROUP BY a."AlbumID", ar."ArtistID";
    """
    return execute_query_ret_result(query)


@bp.route("/music/all/artists", methods=["GET"])
def get_all_artists() -> Any:
    query = """
    SELECT
        ar."ArtistID",
        ar."Name" AS "ArtistName",
        COUNT(a."AlbumID") AS "AlbumCount"
    FROM "Artist" ar
    LEFT JOIN "Album" a ON ar."ArtistID" = a."ArtistID"
    GROUP BY ar."ArtistID";
    """
    return execute_query_ret_result(query)
