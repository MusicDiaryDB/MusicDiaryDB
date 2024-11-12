from flask import Blueprint, jsonify
from helpers import execute_query

bp = Blueprint("aggregate", __name__)

# ============================
#  AGGREGATE REPORT ROUTES
# ============================


@bp.route("/report/total_users", methods=["GET"])
def total_users_reports():
    query = 'SELECT COUNT(*) AS total_users FROM "Users";'
    result = execute_query(query, fetch_one=True)
    return jsonify(result)


@bp.route("/report/avg_visibility_entries", methods=["GET"])
def avg_visability_entries_report():
    query = """
    SELECT AVG(CASE WHEN \"Visibility\" = 'public' THEN 1 ELSE 0 END) AS avg_public_entries
    FROM \"DiaryEntry\";
    """
    result = execute_query(query, fetch_one=True)
    return jsonify(result)


@bp.route("/report/reviews_per_song", methods=["GET"])
def reviews_per_song_report():
    query = """
    SELECT \"SongID\", COUNT(*) AS total_reviews, AVG(CASE WHEN \"Visibility\" = 'public' THEN 1 ELSE 0 END) AS avg_rating
    FROM \"Review\"
    GROUP BY \"SongID\";
    """
    result = execute_query(query)
    return jsonify(result)


@bp.route("/report/entries_by_date", methods=["GET"])
def entries_by_date_report():
    query = """
    SELECT "Date", COUNT(*) AS entry_count
    FROM "DiaryEntry"
    GROUP BY "Date"
    ORDER BY "Date";
    """
    result = execute_query(query)
    return jsonify(result)


@bp.route("/report/friend_counts", methods=["GET"])
def friend_counts_report():
    query = """
    SELECT "UserID", COUNT("FriendUserID") AS friend_count
    FROM "UserFriends"
    GROUP BY "UserID"
    """
    result = execute_query(query)
    return jsonify(result)


@bp.route("/report/visibilty_count_entries", methods=["GET"])
def visibility_count_entries_report():
    query = """
    SELECT "Visibility", COUNT(*) AS count
    FROM "DiaryEntry"
    GROUP BY "Visibility";
    """
    result = execute_query(query)
    return jsonify(result)


@bp.route("/report/avg_rating_per_song", methods=["GET"])
def avg_rating_per_song_report():
    query = """
    SELECT "SongID", AVG(CASE WHEN "Visibility" = 'public' THEN 1 ELSE 0 END) AS avg_rating
    FROM "Review"
    GROUP BY "SongID"
    """
    result = execute_query(query)
    return jsonify(result)


@bp.route("/report/most_reviewed_songs", methods=["GET"])
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


@bp.route("/report/songs_released_by_artist", methods=["GET"])
def songs_released_by_artist_report():
    query = """
    SELECT a."ArtistID", a."Name",
    (SELECT COUNT(*) FROM "Song" s WHERE s."AlbumID" IN
    (SELECT "AlbumID" FROM "Album" WHERE "ArtistID" = a."ArtistID")) AS total_songs
    FROM "Artist" a;
    """
    result = execute_query(query)
    return jsonify(result)


@bp.route("/report/avg_review_score_multiple_reviews", methods=["GET"])
def avg_review_score_multiple_reviews_report():
    query = """
    SELECT "SongID", AVG("Rating") AS avg_rating
    FROM "Review"
    WHERE "SongID" IN (SELECT "SongID" FROM "Review" GROUP BY "SongID" HAVING COUNT(*) > 1)
    GROUP BY "SongID";
    """
    result = execute_query(query)
    return jsonify(result)


@bp.route("/report/users_with_most_entries", methods=["GET"])
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


@bp.route("/report/user_count_by_visibility", methods=["GET"])
def user_count_by_visibility_report():
    query = """
    SELECT "Visibility", COUNT(DISTINCT "UserID") AS user_count
    FROM "DiaryEntry"
    GROUP BY "Visibility";
    """
    result = execute_query(query)
    return jsonify(result)
