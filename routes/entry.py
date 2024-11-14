from typing import Any
from flask import Blueprint
from helpers import handle_request

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
