from typing import Any
from flask import Flask, request, render_template
from helpers import (
    handle_request,
    delete_resource_with_multiple_keys,
    update_resource_with_multiple_keys,
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
    return handle_request("Song", "create", ["name", "releaseDate"], "SongID")


@app.route("/song/<int:song_id>", methods=["GET"])
def get_song(song_id) -> Any:
    return handle_request("Song", "get", [], "SongID", song_id)


@app.route("/song/<int:song_id>", methods=["PUT"])
def update_song(song_id) -> Any:
    return handle_request("Song", "update", ["name", "releaseDate"], "SongID", song_id)


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
        ["date", "description", "visibility", "userId"],
        "EntryID",
    )


@app.route("/entry/<int:entry_id>", methods=["PUT"])
def update_diary_entry(entry_id: int) -> Any:
    return handle_request(
        "DiaryEntry", "update", ["description", "visibility"], "EntryID", entry_id
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
    return handle_request("Album", "create", ["name"], "AlbumID")


@app.route("/album/<int:album_id>", methods=["GET"])
def get_album(album_id) -> Any:
    return handle_request("Album", "get", [], "AlbumID", album_id)


@app.route("/album/<int:album_id>", methods=["PUT"])
def update_album(album_id) -> Any:
    return handle_request("Album", "update", ["name"], "AlbumID", album_id)


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
        "Review", "create", ["contents", "visibility", "songId"], "ReviewID"
    )


@app.route("/review/<int:review_id>", methods=["PUT"])
def update_review(review_id) -> Any:
    return handle_request(
        "Review", "update", ["contents", "visibility"], "ReviewID", review_id
    )


@app.route("/review/<int:review_id>", methods=["DELETE"])
def delete_review(review_id) -> Any:
    return handle_request("Review", "delete", [], "ReviewID", review_id)


# ============================
#     USER REVIEWS ROUTES
# ============================


@app.route("/user_review/", methods=["POST"])
def create_user_review() -> Any:
    return handle_request("UserReviews", "create", ["userId", "reviewId"], "UserID")


@app.route("/user_review/<int:user_id>/<int:review_id>", methods=["PUT"])
def update_user_review(user_id, review_id) -> Any:
    return update_resource_with_multiple_keys(
        "UserReviews", request.form, ["UserID", "ReviewID"], (user_id, review_id)
    )


@app.route("/user_review/<int:user_id>/<int:review_id>", methods=["GET"])
def get_user_review(user_id, review_id) -> Any:
    return handle_request("UserReviews", "get", [], "UserID", (user_id, review_id))


@app.route("/user_review/<int:user_id>/<int:review_id>", methods=["DELETE"])
def delete_user_review(user_id, review_id) -> Any:
    return delete_resource_with_multiple_keys(
        "UserReviews", ["UserID", "ReviewID"], (user_id, review_id)
    )


# ============================
#     ARTIST ALBUM ROUTES
# ============================


@app.route("/artist_album/", methods=["POST"])
def create_artist_album() -> Any:
    return handle_request("ArtistAlbums", "create", ["artistId", "albumId"], None)


@app.route("/artist_album/<int:artist_id>/<int:album_id>", methods=["PUT"])
def update_artist_album(artist_id, album_id) -> Any:
    return update_resource_with_multiple_keys(
        "ArtistAlbums",
        request.form,
        ["ArtistID", "AlbumID"],
        (artist_id, album_id),
    )


@app.route("/artist_album/<int:artist_id>/<int:album_id>", methods=["DELETE"])
def delete_artist_album(artist_id, album_id) -> Any:
    return delete_resource_with_multiple_keys(
        "ArtistAlbums", ["ArtistID", "AlbumID"], (artist_id, album_id)
    )


@app.route("/")
def index() -> Any:
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
