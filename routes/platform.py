from typing import Any
from flask import Blueprint
from helpers import handle_request

bp = Blueprint("platform", __name__)

# ============================
#     PLATFORM ROUTES
# ============================


@bp.route("/platform/", methods=["POST"])
def create_platform() -> Any:
    return handle_request(
        "StreamingPlatform", "create", ["name"], "StreamingPlatformID"
    )


@bp.route("/platform/<int:platform_id>", methods=["GET"])
def get_platform(platform_id) -> Any:
    return handle_request(
        "StreamingPlatform", "get", [], "StreamingPlatformID", platform_id
    )


@bp.route("/platform/<string:name>", methods=["GET"])
def get_platform_by_name(name) -> Any:
    return handle_request("StreamingPlatform", "get", [], "Name", name)


@bp.route("/platform/<int:platform_id>", methods=["PUT"])
def update_platform(platform_id) -> Any:
    return handle_request(
        "StreamingPlatform", "update", ["name"], "StreamingPlatformID", platform_id
    )


@bp.route("/platform/<int:platform_id>", methods=["DELETE"])
def delete_platform(platform_id) -> Any:
    return handle_request(
        "StreamingPlatform", "delete", [], "StreamingPlatformID", platform_id
    )
