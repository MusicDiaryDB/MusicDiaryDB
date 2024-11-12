from typing import Any
from flask import Blueprint
from helpers import handle_request

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
