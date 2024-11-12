from typing import Any
from flask import Blueprint
from helpers import handle_request, execute_query, delete_resource_with_multiple_keys

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


@bp.route("/user_reviews/<int:user_id>", methods=["GET"])
def get_user_friends_public_reviews(user_id) -> Any:
    query = 'SELECT u."Username", s."Name" AS "songname", r."ReviewID", r."Contents" FROM "User" u JOIN "UserFriends" uf ON u."UserID" = uf."FriendUserID" JOIN "UserReviews" ur ON ur."UserID" = uf."FriendUserID"  JOIN "Review" r ON ur."ReviewID" = r."ReviewID" JOIN "Song" s ON r."SongID" = s."SongID" WHERE uf."UserID" = %s AND (r."Visibility" = \'Friends\' OR r."Visibility" = \'Public\')'
    friends_reviews = execute_query(query, (user_id,))
    return friends_reviews


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


@bp.route("/report_entry/<int:report_id>/<int:entry_id>", methods=["DELETE"])
def delete_report_entry(report_id, entry_id) -> Any:
    return delete_resource_with_multiple_keys(
        "ReportEntries", ["ReportID", "EntryID"], (report_id, entry_id)
    )
