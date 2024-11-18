from typing import Any
from flask import Blueprint
from helpers import (
    execute_query_ret_result,
    handle_request,
    execute_query,
)

bp = Blueprint("review", __name__)

# ============================
#       REVIEW ROUTES
# ============================


@bp.route("/review/", methods=["POST"])
def create_review() -> Any:
    return handle_request(
        "Review", "create", ["contents", "visibility", "songId", "userId"], "ReviewID"
    )


@bp.route("/review/<int:review_id>", methods=["GET"])
def get_review(review_id: int) -> Any:
    return handle_request("Review", "get", [], "ReviewID", review_id)


@bp.route("/review/<int:review_id>", methods=["PUT"])
def update_review(review_id) -> Any:
    return handle_request(
        "Review", "update", ["contents", "visibility"], "ReviewID", review_id
    )


@bp.route("/review/<int:review_id>", methods=["DELETE"])
def delete_review(review_id) -> Any:
    return handle_request("Review", "delete", [], "ReviewID", review_id)


@bp.route("/review/user/<int:user_id>", methods=["GET"])
def get_user_reviews(user_id: int) -> Any:
    query = """SELECT * FROM "Review" WHERE "UserID" = '%s';"""
    return execute_query_ret_result(query, (user_id,))


@bp.route("/reviews/all", methods=["GET"])
def get_all_reviews() -> Any:
    query = """SELECT * FROM "Review";"""
    return execute_query_ret_result(query)


@bp.route("/user_reviews/<int:user_id>", methods=["GET"])
def get_user_friends_public_reviews(user_id) -> Any:
    query = """
    SELECT u."Username", s."Name" AS "songname", r."ReviewID", r."Contents"
    FROM "User" u
    JOIN "UserFriends" uf ON u."UserID" = uf."FriendUserID"
    JOIN "Review" r ON r."UserID" = uf."FriendUserID"
    JOIN "Song" s ON r."SongID" = s."SongID"
    WHERE uf."UserID" = 1 AND (r."Visibility" = 'Friends' OR r."Visibility" = 'Public')
    """
    print(f"Running query for user_id {user_id}: {query}")  # Debugging line
    friends_reviews = execute_query(query, (user_id,))
    print(friends_reviews)
    return friends_reviews


@bp.route("/review/song/<int:review_id>", methods=["GET"])
def get_review_song(review_id) -> Any:
    query = """
    SELECT
        s."Name" AS "SongName",
        a."Name" AS "AlbumName",
        ar."Name" AS "ArtistName",
        r."Visibility",
        r."Contents"
    FROM "Review" r
    JOIN "Song" s ON r."SongID" = s."SongID"
    JOIN "Album" a ON s."AlbumID" = a."AlbumID"
    JOIN "Artist" ar ON a."ArtistID" = ar."ArtistID"
    WHERE r."ReviewID" = %s;
    """
    return execute_query_ret_result(query, (review_id,))


@bp.route("/review/friends/<int:user_id>")
def get_friend_reviews(user_id) -> Any:
    query = """
    SELECT DISTINCT
        u."Username" AS FriendUsername,
        r."Contents" AS Contents,
        s."Name" AS SongName,
        r."ReviewID" as ReviewID
    FROM
        "UserFriends" uf
    INNER JOIN "User" u
        ON uf."FriendUserID" = u."UserID"
    INNER JOIN "Review" r
        ON u."UserID" = r."UserID"
    INNER JOIN "Song" s
        ON r."SongID" = s."SongID"
    WHERE
        uf."UserID" = %s
        AND (r."Visibility" = 'public' OR r."Visibility" = 'friend');
    """
    return execute_query_ret_result(query, (user_id,))
