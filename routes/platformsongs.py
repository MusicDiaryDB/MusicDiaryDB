from typing import Any
from flask import Blueprint
from helpers import handle_request, delete_resource_with_multiple_keys

bp = Blueprint("platformsongs", __name__)

# ============================
#  STREAMING PLATFORM SONGS ROUTES
# ============================


@bp.route("/platform_song/", methods=["POST"])
def create_platform_song() -> Any:
    return handle_request(
        "StreamingPlatformSongs", "create", ["streamingPlatformId", "songId"], None
    )


@bp.route("/platform_song/<int:platform_id>/<int:song_id>", methods=["GET"])
def get_platform_song(platform_id, song_id) -> Any:
    return handle_request(
        "StreamingPlatformSongs",
        "get",
        [],
        ["StreamingPlatformID", "SongID"],
        (platform_id, song_id),
    )


@bp.route("/platform_song/<int:platform_id>/<int:song_id>", methods=["DELETE"])
def delete_platform_song(platform_id, song_id) -> Any:
    return delete_resource_with_multiple_keys(
        "StreamingPlatformSongs",
        ["StreamingPlatformID", "SongID"],
        (platform_id, song_id),
    )
