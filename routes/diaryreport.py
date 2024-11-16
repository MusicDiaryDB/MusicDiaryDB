from typing import Any
from flask import Blueprint, Response
from helpers import (
    delete_resource_with_multiple_keys,
    execute_query_ret_result,
    handle_request,
)

bp = Blueprint("diary_report", __name__)


# ============================
#      DIARY REPORT ROUTES
# ============================


@bp.route("/report/", methods=["POST"])
def create_diary_report() -> Any:
    return handle_request(
        "DiaryReport",
        "create",
        ["date", "description", "visibility", "userId"],
        "ReportID",
    )


@bp.route("/report/<int:report_id>", methods=["GET"])
def get_diary_report(report_id: int) -> Any:
    return handle_request("DiaryReport", "get", [], "ReportID", report_id)


@bp.route("/report/<int:report_id>", methods=["PUT"])
def update_diary_report(report_id: int) -> Any:
    return handle_request(
        "DiaryReport", "update", ["description", "visibility"], "ReportID", report_id
    )


@bp.route("/report/<int:report_id>", methods=["DELETE"])
def delete_diary_report(report_id: int) -> Any:
    return handle_request("DiaryReport", "delete", [], "ReportID", report_id)


@bp.route("/report/user/<int:user_id>", methods=["GET"])
def get_user_diary_reports(user_id: int) -> Any:
    query = """SELECT * FROM "DiaryReport" WHERE "UserID" = '%s';"""
    return execute_query_ret_result(query, (user_id,))


@bp.route("/report/friends/<int:user_id>", methods=["GET"])
def get_friends_diary_reports(user_id: int) -> Any:
    # Fetch the user's friends from UserFriends table
    query = """SELECT "FriendUserID" FROM "UserFriends" WHERE "UserID" = %s"""
    friends, status = execute_query_ret_result(query, (user_id,))

    # If no friends, return an empty list
    if not friends or not isinstance(friends, list):
        return {"message": "No friends found."}, status

    # Fetch diary reports for each friend
    friend_reports = {}
    for friend in friends:
        friend_id = friend.get("FriendUserID")
        if not friend_id:
            continue

        report_query = """SELECT * FROM "DiaryReport" WHERE "UserID" = %s"""
        reports, report_status = execute_query_ret_result(report_query, (friend_id,))
        if report_status == 200:
            friend_reports[friend_id] = reports

    return friend_reports, 200


@bp.route("/report/songs/<int:report_id>", methods=["GET"])
def get_report_song_names(report_id) -> Any:
    query = """
    SELECT DISTINCT s."Name", de.*
    FROM "Song" s
    JOIN "DiaryEntry" de ON s."SongID" = de."SongID"
    JOIN "ReportEntries" re ON de."EntryID" = re."EntryID"
    WHERE re."ReportID" = %s;
    """
    return execute_query_ret_result(query, (report_id,))


# ============================
#    REPORT ENTRIES ROUTES
# ============================


@bp.route("/report_entry/", methods=["POST"])
def create_report_entry() -> Any:
    return handle_request("ReportEntries", "create", ["reportId", "entryId"], None)


@bp.route("/report_entry/<int:report_id>/<int:entry_id>", methods=["GET"])
def get_report_entry(report_id, entry_id) -> Any:
    return handle_request(
        "ReportEntries", "get", [], ["ReportID", "EntryID"], (report_id, entry_id)
    )


@bp.route("/report_entry/by_report/<int:report_id>")
def get_report_entry_by_report(report_id) -> tuple[Response, Any]:
    query = """
    SELECT * FROM "ReportEntries" WHERE "ReportID" = '%s'
    """
    return execute_query_ret_result(query, (report_id,))


@bp.route("/report_entry/<int:report_id>/<int:entry_id>", methods=["DELETE"])
def delete_report_entry(report_id, entry_id) -> Any:
    return delete_resource_with_multiple_keys(
        "ReportEntries", ["ReportID", "EntryID"], (report_id, entry_id)
    )
