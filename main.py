from typing import Any
from flask import Flask, render_template, jsonify
from helpers import execute_query
from helpers import (
    handle_request,
    delete_resource_with_multiple_keys,
    # update_resource_with_multiple_keys,
)
from flask_cors import CORS

app = Flask(__name__)
CORS(app)



# ============================
#  HTML LINKED FILES ROUTES
# ============================
@app.route("/graphs")
def graphs():
    return render_template("graph.html")

# ============================
#         USER ROUTES
# ============================


@app.route("/user/", methods=["POST"])
def create_user() -> Any:
    return handle_request("User", "create", ["username", "visibility"], "UserID")


@app.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id) -> Any:
    if (user_id == "all"):
        return handle_request("User", "get",[],"*","all")
    return handle_request("User", "get", [], "UserID", user_id)

@app.route("/user/<string:username>", methods=["GET"])
def get_user_by_username(username) -> Any:
    return handle_request("User", "get", [], "Username", username)


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

@app.route("/album/<string:name>", methods=["GET"])
def get_album_by_name(name) -> Any:
    return handle_request("Album", "get", [], "Name", name)

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

@app.route("/artist/<string:name>", methods=["GET"])
def get_artist_by_name(name) -> Any:
    return handle_request("Artist", "get", [], "Name", name)


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


# ============================
#  AGGREGATE REPORT ROUTES
# ============================

@app.route("/report/total_users", methods = ["GET"])
def total_users_reports():
    query = "SELECT COUNT(*) AS total_users FROM \"Users\";"
    result = execute_query(query, fetch_one=True)
    return jsonify(result)

@app.route("/report/avg_visibility_entries", methods = ["GET"])
def avg_visability_entries_report():
    query = """
    SELECT AVG(CASE WHEN \"Visibility\" = 'public' THEN 1 ELSE 0 END) AS avg_public_entries 
    FROM \"DiaryEntry\";
    """
    result = execute_query(query, fetch_one = True)
    return jsonify(result)

@app.route("/report/song_release_dates", methods=["GET"])
def song_release_dates_report():
    query = "SELECT MIN(\"ReleaseDate\") AS earliest_song, MAX(\"ReleaseDate\") AS latest_song FROM \"Song\";"
    result = execute_query(query, fetch_one=True)
    return jsonify(result)

@app.route("/report/reviews_per_song", methods = ["GET"])
def reviews_per_song_report():
    query = """
    SELECT \"SongID\", COUNT(*) AS total_reviews, AVG(CASE WHEN \"Visibility\" = 'public' THEN 1 ELSE 0 END) AS avg_rating
    FROM \"Review\"
    GROUP BY \"SongID\";
    """
    result = execute_query(query)
    return jsonify(result)

@app.route("/report/entries_by_date", methods = ["GET"])
def entries_by_date_report():
    query = """
    SELECT "Date", COUNT(*) AS entry_count
    FROM "DiaryEntry"
    GROUP BY "Date"
    ORDER BY "Date";
    """
    result = execute_query(query)
    return jsonify(result)

@app.route("/report/friend_counts", methods=["GET"])
def friend_counts_report():
    query = """
    SELECT "UserID", COUNT("FriendUserID") AS friend_count
    FROM "UserFriends"
    GROUP BY "UserID"
    """
    result = execute_query(query)
    return jsonify(result)

@app.route("/report/visibilty_count_entries", methods = ["GET"])
def visibility_count_entries_report():
    query = """
    SELECT "Visibility", COUNT(*) AS count
    FROM "DiaryEntry"
    GROUP BY "Visibility";
    """
    result = execute_query(query)
    return jsonify(result)

@app.route("/report/avg_rating_per_song", methods = ["GET"])
def avg_rating_per_song_report():
    query = """
    SELECT "SongID", AVG(CASE WHEN "Visibility" = 'public' THEN 1 ELSE 0 END) AS avg_rating
    FROM "Review"
    GROUP BY "SongID"
    """
    result = execute_query(query)
    return jsonify(result)
    
@app.route("/report/most_reviewed_songs", methods = ["GET"])
def most_reviewed_songs_report():
    query = """
    SELECT "SongID", COUNT(*) AS review_count
    FROM "Review"
    GROUP BY "SongID"
    ORDER BY review_count DESC
    LIMIT 5;
    """
    result = execute_query(query)
    return jsonify(result)

# ============================
#  AGGREGATE REPORT ROUTES
#  WITH SUBQUERIES AND JOINS
# ============================

@app.route("/report/songs_released_by_artist", methods = ["GET"])
def songs_released_by_artist_report():
    query = """
    SELECT a."ArtistID", a."Name",
    (SELECT COUNT(*) FROM "Song" s WHERE s."AlbumID" IN
    (SELECT "AlbumID" FROM "Album" WHERE "ArtistID" = a."ArtistID")) AS total_songs
    FROM "Artist" a;
    """
    result = execute_query(query)
    return jsonify(result)

@app.route("/report/avg_review_score_multiple_reviews", methods = ["GET"])
def avg_review_score_multiple_reviews_report():
    query = """
    SELECT "SongID", AVG("Rating") AS avg_rating
    FROM "Review"
    WHERE "SongID" IN (SELECT "SongID" FROM "Review" GROUP BY "SongID" HAVING COUNT(*) > 1)
    GROUP BY "SongID";    
    """
    result = execute_query(query)
    return jsonify(result)

@app.route("/report/users_with_most_entries", methods = ["GET"])
def users_with_most_entries_report():
    query = """
    SELECT u."UserID", u."Username", COUNT(d."EntryID") AS total_entries
    FROM "User" u
    LEFT JOIN "DiaryEntry" d ON u."UserID" = d."UserID"
    GROUP BY u."UserID", u."Username"
    ORDER BY total_entries DESC
    """
    result = execute_query(query)
    return jsonify(result)

# ============================
#  GRAPH FUNCTIONALITY ROUTES
# ============================

@app.route("/report/user_count_by_visibility", methods =["GET"])
def user_count_by_visibility_report():
    query ="""
    SELECT "Visibility", COUNT(DISTINCT "UserID) AS user_count
    FROM "DiaryEntry"
    GROUP BY "Visibility";
    """
    result = execute_query(query)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5400)
