from typing import Any
from flask import Blueprint
from helpers import (
    delete_resource_with_multiple_keys,
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
