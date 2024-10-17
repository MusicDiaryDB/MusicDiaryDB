from typing import Any
from flask import Flask, render_template
from helpers import (
    handle_request,
    delete_resource_with_multiple_keys,
    # update_resource_with_multiple_keys,
)

app = Flask(__name__)


# ============================
#         USER ROUTES
# ============================


@app.route("/user/", methods=["POST"])
def create_user() -> Any:
    return handle_request("User", "create", ["username", "visibility"], "UserID")


@app.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id) -> Any:
    return handle_request("User", "get", [], "UserID", user_id)


@app.route("/user/<int:user_id>", methods=["PUT"])
def update_user(user_id) -> Any:
    return handle_request(
        "User", "update", ["username", "visibility"], "UserID", user_id
    )


@app.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id) -> Any:
    return handle_request("User", "delete", [], "UserID", user_id)


# ============================
#     SONG ROUTES
# ============================


@app.route("/song/", methods=["POST"])
def create_song() -> Any:
    return handle_request(
        "Song", "create", ["name", "releaseDate", "albumId"], "SongID"
    )


@app.route("/song/<int:song_id>", methods=["GET"])
def get_song(song_id) -> Any:
    return handle_request("Song", "get", [], "SongID", song_id)


@app.route("/song/<int:song_id>", methods=["PUT"])
def update_song(song_id) -> Any:
    return handle_request(
        "Song", "update", ["name", "releaseDate", "albumId"], "SongID", song_id
    )


@app.route("/song/<int:song_id>", methods=["DELETE"])
def delete_song(song_id) -> Any:
    return handle_request("Song", "delete", [], "SongID", song_id)


# ============================
#     DIARY ENTRY ROUTES
# ============================


@app.route("/entry/", methods=["POST"])
def create_diary_entry() -> Any:
    return handle_request(
        "DiaryEntry",
        "create",
        ["date", "description", "visibility", "userId", "songId"],
        "EntryID",
    )


@app.route("/entry/<int:entry_id>", methods=["GET"])
def get_diary_entry(entry_id: int) -> Any:
    return handle_request("DiaryEntry", "get", [], "EntryID", entry_id)


@app.route("/entry/<int:entry_id>", methods=["PUT"])
def update_diary_entry(entry_id: int) -> Any:
    return handle_request(
        "DiaryEntry",
        "update",
        ["description", "visibility", "songId"],
        "EntryID",
        entry_id,
    )


@app.route("/entry/<int:entry_id>", methods=["DELETE"])
def delete_diary_entry(entry_id: int) -> Any:
    return handle_request("DiaryEntry", "delete", [], "EntryID", entry_id)


# ============================
#      DIARY REPORT ROUTES
# ============================


@app.route("/report/", methods=["POST"])
def create_diary_report() -> Any:
    return handle_request(
        "DiaryReport",
        "create",
        ["date", "description", "visibility", "userId"],
        "ReportID",
    )


@app.route("/report/<int:report_id>", methods=["GET"])
def get_diary_report(report_id: int) -> Any:
    return handle_request("DiaryReport", "get", [], "ReportID", report_id)


@app.route("/report/<int:report_id>", methods=["PUT"])
def update_diary_report(report_id: int) -> Any:
    return handle_request(
        "DiaryReport", "update", ["description", "visibility"], "ReportID", report_id
    )


@app.route("/report/<int:report_id>", methods=["DELETE"])
def delete_diary_report(report_id: int) -> Any:
    return handle_request("DiaryReport", "delete", [], "ReportID", report_id)


# ============================
#     ALBUM ROUTES
# ============================


@app.route("/album/", methods=["POST"])
def create_album() -> Any:
    return handle_request("Album", "create", ["name", "artistId"], "AlbumID")


@app.route("/album/<int:album_id>", methods=["GET"])
def get_album(album_id) -> Any:
    return handle_request("Album", "get", [], "AlbumID", album_id)


@app.route("/album/<int:album_id>", methods=["PUT"])
def update_album(album_id) -> Any:
    return handle_request("Album", "update", ["name", "artistId"], "AlbumID", album_id)


@app.route("/album/<int:album_id>", methods=["DELETE"])
def delete_album(album_id) -> Any:
    return handle_request("Album", "delete", [], "AlbumID", album_id)


# ============================
#     ARTIST ROUTES
# ============================


@app.route("/artist/", methods=["POST"])
def create_artist() -> Any:
    return handle_request("Artist", "create", ["name"], "ArtistID")


@app.route("/artist/<int:artist_id>", methods=["GET"])
def get_artist(artist_id) -> Any:
    return handle_request("Artist", "get", [], "ArtistID", artist_id)


@app.route("/artist/<int:artist_id>", methods=["PUT"])
def update_artist(artist_id) -> Any:
    return handle_request("Artist", "update", ["name"], "ArtistID", artist_id)


@app.route("/artist/<int:artist_id>", methods=["DELETE"])
def delete_artist(artist_id) -> Any:
    return handle_request("Artist", "delete", [], "ArtistID", artist_id)


# ============================
#     PLATFORM ROUTES
# ============================


@app.route("/platform/", methods=["POST"])
def create_platform() -> Any:
    return handle_request(
        "StreamingPlatform", "create", ["name"], "StreamingPlatformID"
    )


@app.route("/platform/<int:platform_id>", methods=["GET"])
def get_platform(platform_id) -> Any:
    return handle_request(
        "StreamingPlatform", "get", [], "StreamingPlatformID", platform_id
    )


@app.route("/platform/<int:platform_id>", methods=["PUT"])
def update_platform(platform_id) -> Any:
    return handle_request(
        "StreamingPlatform", "update", ["name"], "StreamingPlatformID", platform_id
    )


@app.route("/platform/<int:platform_id>", methods=["DELETE"])
def delete_platform(platform_id) -> Any:
    return handle_request(
        "StreamingPlatform", "delete", [], "StreamingPlatformID", platform_id
    )


# ============================
#       REVIEW ROUTES
# ============================


@app.route("/review/", methods=["POST"])
def create_review() -> Any:
    return handle_request(
        "Review", "create", ["contents", "visibility", "songId", "userId"], "ReviewID"
    )


@app.route("/review/<int:review_id>", methods=["GET"])
def get_review(review_id: int) -> Any:
    return handle_request("Review", "get", [], "ReviewID", review_id)


@app.route("/review/<int:review_id>", methods=["PUT"])
def update_review(review_id) -> Any:
    return handle_request(
        "Review", "update", ["contents", "visibility"], "ReviewID", review_id
    )


@app.route("/review/<int:review_id>", methods=["DELETE"])
def delete_review(review_id) -> Any:
    return handle_request("Review", "delete", [], "ReviewID", review_id)


# ============================
#    REPORT ENTRIES ROUTES
# ============================


@app.route("/report_entry/", methods=["POST"])
def create_report_entry() -> Any:
    return handle_request("ReportEntries", "create", ["reportId", "entryId"], None)


@app.route("/report_entry/<int:report_id>/<int:entry_id>", methods=["GET"])
def get_report_entry(report_id, entry_id) -> Any:
    return handle_request(
        "ReportEntries", "get", [], ["ReportID", "EntryID"], (report_id, entry_id)
    )


@app.route("/report_entry/<int:report_id>/<int:entry_id>", methods=["DELETE"])
def delete_report_entry(report_id, entry_id) -> Any:
    return delete_resource_with_multiple_keys(
        "ReportEntries", ["ReportID", "EntryID"], (report_id, entry_id)
    )


# ============================
#     USER FRIENDS ROUTES
# ============================


@app.route("/user_friend/", methods=["POST"])
def create_user_friend() -> Any:
    return handle_request("UserFriends", "create", ["userId", "friendUserId"], None)


@app.route("/user_friend/<int:user_id>/<int:friend_user_id>", methods=["GET"])
def get_user_friend(user_id, friend_user_id) -> Any:
    return handle_request(
        "UserFriends", "get", [], ["UserID", "FriendUserID"], (user_id, friend_user_id)
    )


@app.route("/user_friend/<int:user_id>/<int:friend_user_id>", methods=["DELETE"])
def delete_user_friend(user_id, friend_user_id) -> Any:
    return delete_resource_with_multiple_keys(
        "UserFriends", ["UserID", "FriendUserID"], (user_id, friend_user_id)
    )


# ============================
#  STREAMING PLATFORM SONGS ROUTES
# ============================


@app.route("/platform_song/", methods=["POST"])
def create_platform_song() -> Any:
    return handle_request(
        "StreamingPlatformSongs", "create", ["streamingPlatformId", "songId"], None
    )


@app.route("/platform_song/<int:platform_id>/<int:song_id>", methods=["GET"])
def get_platform_song(platform_id, song_id) -> Any:
    return handle_request(
        "StreamingPlatformSongs",
        "get",
        [],
        ["StreamingPlatformID", "SongID"],
        (platform_id, song_id),
    )


@app.route("/platform_song/<int:platform_id>/<int:song_id>", methods=["DELETE"])
def delete_platform_song(platform_id, song_id) -> Any:
    return delete_resource_with_multiple_keys(
        "StreamingPlatformSongs",
        ["StreamingPlatformID", "SongID"],
        (platform_id, song_id),
    )


@app.route("/")
def index() -> Any:
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
