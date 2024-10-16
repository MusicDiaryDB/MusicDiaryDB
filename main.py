#
# NOTE: This file is a WIP, but should be easier to work with than the original main.py
# - it may or may not work correctly currently
#

from typing import Any
from flask import Flask, request, jsonify, render_template
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)


def create_connection():
    try:
        conn = psycopg2.connect(
            dbname="music_diary_db",
            user="admin",
            password="admin",
            host="127.0.0.1",
            port="5432",
        )
        print("Database connection successful")
        return conn
    except Exception as e:
        print(f"Error: {e}")
        return None


def execute_query(query, params=None, fetch_one=False):
    conn = create_connection()
    if conn is None:
        print("Failed to connect to database")
        return
    result = None
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            if query.strip().upper().startswith("SELECT"):
                result = cur.fetchone() if fetch_one else cur.fetchall()
            else:
                result = cur.rowcount
            conn.commit()
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()
    return result


def create_resource(table, params, primary_key):
    max_id_query = f'SELECT MAX("{primary_key}") FROM "{table}"'
    max_id_result = execute_query(max_id_query, fetch_one=True)

    max_id = None
    if isinstance(max_id_result, dict):
        max_id = max_id_result.get("max")
        print(f"Max ID = {max_id}")
    else:
        print("Failed to get max id result")

    # TODO: add handling of intermediary tables where max_id doesn't matter.
    # the seq name causes error if you try to run it in that case

    table_quoted = f'"{table}"'
    seq_name_query = f"SELECT pg_get_serial_sequence('{table_quoted}', '{primary_key}')"
    seq_name_result = execute_query(seq_name_query, fetch_one=True)

    seq_name = None
    if seq_name_result and isinstance(seq_name_result, list):
        seq_name = seq_name_result[0]["pg_get_serial_sequence"]
    elif isinstance(seq_name_result, dict):
        seq_name = seq_name_result["pg_get_serial_sequence"]
    else:
        print(f"No sequence found for table '{table}' and primary key '{primary_key}'")
    if seq_name is not None:
        setval_query = f"SELECT setval('{seq_name}', {max_id})"
        execute_query(setval_query)

    keys = ", ".join(
        [f'"{key[0].upper() + key[1:].replace("Id", "ID")}"' for key in params.keys()]
    )
    values = ", ".join(["%s" for _ in params.keys()])

    insert_query = (
        f'INSERT INTO "{table}" ({keys}) VALUES ({values}) RETURNING "{primary_key}"'
    )
    print(insert_query)

    return execute_query(insert_query, tuple(params.values()), fetch_one=True)


def update_resource(table, params, identifier, primary_key):
    set_clause = ", ".join(
        [
            f'"{key[0].upper() + key[1:].replace("Id", "ID")}" = %s'
            for key in params.keys()
        ]
    )
    query = f'UPDATE "{table}" SET {set_clause} WHERE "{primary_key}" = %s'
    return execute_query(query, tuple(params.values()) + (identifier,))


def delete_resource(table, identifier, primary_key):
    query = f'DELETE FROM "{table}" WHERE "{primary_key}" = %s'
    return execute_query(query, (identifier,))


def get_resource(table, identifier, primary_key):
    query = f'SELECT * FROM "{table}" WHERE "{primary_key}" = %s'
    return execute_query(query, (identifier,), fetch_one=True)


def handle_request(table, operation, required_fields, primary_key, identifier=None):
    print(
        f"Request recieved: {table}, {operation}, {required_fields}, {primary_key}, {identifier}"
    )

    data = request.form
    params = {field: data.get(field) for field in required_fields}

    if any(value is None for value in params.values()):
        return jsonify({"error": f"Missing fields: {params.values()}"}), 400

    if operation.lower() == "create":
        resource_id = create_resource(table, params, primary_key)
        if resource_id is None:
            return jsonify({"error": f"{table} creation failed"}), 500
        return jsonify(
            {"message": f"{table} created", f"{primary_key}": resource_id}
        ), 201

    elif operation.lower() == "update":
        result = update_resource(table, params, identifier, primary_key)
        if result is None or result == 0:
            return jsonify({"error": f"{table} update failed"}), 404
        return jsonify({"message": f"{table} updated"}), 200

    elif operation.lower() == "delete":
        result = delete_resource(table, identifier, primary_key)
        if result is None or result == 0:
            return jsonify({"error": f"{table} not found"}), 404
        return jsonify({"message": f"{table} deleted"}), 200


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


# POST /review/:songId - Create a review for a song
@app.route("/review/<int:song_id>", methods=["POST"])
def create_review(song_id) -> Any:
    data = request.form.to_dict()
    data["songId"] = song_id
    return handle_request(
        "Review", "create", ["contents", "visibility", "songId"], "ReviewID"
    )


# PUT /review/:reviewId - Update a review by its ID
@app.route("/review/<int:review_id>", methods=["PUT"])
def update_review(review_id) -> Any:
    return handle_request(
        "Review", "update", ["contents", "visibility"], "ReviewID", review_id
    )


# DELETE /review/:reviewId - Delete a review by its ID
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
    data = request.form
    new_user_id = data.get("new-userId")
    new_review_id = data.get("new-reviewId")
    query = """
    UPDATE "UserReviews"
    SET "UserID" = %s, "ReviewID" = %s
    WHERE "UserID" = %s and "ReviewID" = %s
    """
    conn = create_connection()
    if conn is None:
        print("Failed to connect to database")
        return
    try:
        cur = conn.cursor()
        cur.execute(query, (new_user_id, new_review_id, user_id, review_id))
        conn.commit()
        affected_rows = cur.rowcount
        cur.close()
        conn.close()
        if affected_rows > 0:
            return jsonify({"message": "User review updated successfully!"}), 200
        else:
            return jsonify(
                {
                    "error": "No rows updated. Check if the original UserID and ReviewID exist."
                }
            ), 404
    except Exception as e:
        print(f"Error updating UserReview: {str(e)}")
        return jsonify(
            {"error": "An error occurred while updating the user review."}
        ), 500


@app.route("/user_review/<int:user_id>/<int:review_id>", methods=["GET"])
def get_user_review(user_id, review_id) -> Any:
    return handle_request("UserReviews", "get", [], "UserID", (user_id, review_id))


@app.route("/user_review/<int:user_id>/<int:review_id>", methods=["DELETE"])
def delete_user_review(user_id, review_id) -> Any:
    query = 'DELETE FROM "UserReviews" WHERE "UserID" = %s and "ReviewID" = %s'
    print(
        execute_query(
            query,
            (
                user_id,
                review_id,
            ),
        )
    )
    return jsonify("{}")
    # return handle_request('UserReviews', 'delete', [], 'UserID', (user_id, review_id))


@app.route("/")
def index() -> Any:
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
