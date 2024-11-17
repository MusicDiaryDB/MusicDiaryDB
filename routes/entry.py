from typing import Any
from flask import Blueprint
from helpers import execute_query_ret_result, handle_request

bp = Blueprint("entry", __name__)

# ============================
#     DIARY ENTRY ROUTES
# ============================


@bp.route("/entry/", methods=["POST"])
def create_diary_entry() -> Any:
    return handle_request(
        "DiaryEntry",
        "create",
        ["date", "description", "visibility", "userId", "songId"],
        "EntryID",
    )


@bp.route("/entry/<int:entry_id>", methods=["GET"])
def get_diary_entry(entry_id: int) -> Any:
    return handle_request("DiaryEntry", "get", [], "EntryID", entry_id)


@bp.route("/entry/<int:entry_id>", methods=["PUT"])
def update_diary_entry(entry_id: int) -> Any:
    return handle_request(
        "DiaryEntry",
        "update",
        ["description", "visibility", "songId"],
        "EntryID",
        entry_id,
    )


@bp.route("/entry/<int:entry_id>", methods=["DELETE"])
def delete_diary_entry(entry_id: int) -> Any:
    return handle_request("DiaryEntry", "delete", [], "EntryID", entry_id)


@bp.route("/entry/user/<int:user_id>", methods=["GET"])
def get_user_diary_entries(user_id: int) -> Any:
    query = """SELECT * FROM "DiaryEntry" WHERE "UserID" = '%s';"""
    return execute_query_ret_result(query, (user_id,))


@bp.route("/entry/friends/<int:user_id>", methods=["GET"])
def get_friends_diary_entries(user_id: int) -> Any:
    # Query to get the friends of the user
    friends_query = """SELECT "FriendID" FROM "UserFriends" WHERE "UserID" = '%s';"""
    friends_result = execute_query_ret_result(friends_query, (user_id,))

    if not friends_result:
        return {"message": "No friends found for this user."}, 404

    # Extract the friend IDs from the result
    friend_ids = [friend["FriendID"] for friend in friends_result]

    # Query to get the diary entries of each friend, filtered by visibility (Public or Friends)
    friends_entries_query = """
    SELECT * FROM "DiaryEntry"
    WHERE "UserID" = (%s)
    AND "Visibility" IN ('Public', 'Friends');
    """
    formatted_friend_ids = ",".join([str(friend_id) for friend_id in friend_ids])
    friends_entries_result = execute_query_ret_result(
        friends_entries_query % formatted_friend_ids, ()
    )
    print(friends_entries_result)
    return friends_entries_result


@bp.route("/entries/user/<int:user_id>", methods=["GET"])
def get_user_entries_song(user_id) -> Any:
    query = """
    SELECT
        de."EntryID",
        de."Date",
        de."Description",
        de."Visibility",
        de."UserID",
        s."Name" AS "SongName",
        al."Name" AS "AlbumName",
        ar."Name" AS "ArtistName"
    FROM
        "DiaryEntry" de
    INNER JOIN
        "Song" s ON de."SongID" = s."SongID"
    INNER JOIN
        "Album" al ON s."AlbumID" = al."AlbumID"
    INNER JOIN
        "Artist" ar ON al."ArtistID" = ar."ArtistID"
    WHERE
        de."UserID" = %s
    """
    return execute_query_ret_result(query, (user_id,))


@bp.route("/entries/all", methods=["GET"])
def ge_all_entries() -> Any:
    query = """SELECT * FROM "DiaryEntry"; """
    return execute_query_ret_result(query)
