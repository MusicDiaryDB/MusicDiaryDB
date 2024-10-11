from flask import Flask, request, jsonify, render_template
import psycopg2
from psycopg2.extras import RealDictCursor

# Database configuration
db_config = {
    'dbname': 'music_diary_db',
    'user': 'admin',
    'password': 'admin',
    'host': '127.0.0.1',
    'port': '5432'
}

app = Flask(__name__)


def create_connection():
    try:
        conn = psycopg2.connect(**db_config)
        print("Database connection successful")
        return conn
    except Exception as e:
        print(f"Error: {e}")
        return None


def execute_query(query, params=None, fetch_one=False):
    conn = create_connection()
    result = None
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            # If SELECT statement, fetch results
            if query.strip().upper().startswith("SELECT"):
                if fetch_one:
                    result = cur.fetchone()
                else:
                    result = cur.fetchall()
            else:
                # For INSERT, UPDATE, DELETE return the row count
                result = cur.rowcount
            conn.commit()
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        if conn:  # Ensure the connection is closed only if it was created
            conn.close()
    return result

# ============================
#         USER ROUTES
# ============================


# POST /user/ - Create a new user
@app.route('/user/', methods=['POST'])
def create_user():
    data = request.form
    username = data.get('username')
    visibility = data.get('visibility')

    if not username or not visibility:
        return jsonify({"error": "Missing fields"}), 400

    existing_user_query = 'SELECT * FROM "User" WHERE "Username" = %s'
    existing_user = execute_query(
        existing_user_query, (username,), fetch_one=True)

    if existing_user:
        return jsonify({"error": "Username already exists"}), 400

    query = """
        INSERT INTO "User" ("Username", "Visibility")
        VALUES (%s, %s) RETURNING "UserID"
    """

    user_id = execute_query(query, (username, visibility), fetch_one=True)

    if user_id is None:
        return jsonify({"error": "User creation failed"}), 500

    return jsonify({"message": "User created", "UserID": user_id}), 201


# DELETE /user/:userId - Delete user by UserID
@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    print(f"Deleting user with ID: {user_id}")

    query = 'DELETE FROM "User" WHERE "UserID" = %s'
    result = execute_query(query, (user_id,))

    if result is None or result == 0:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "User deleted"}), 200


# PUT /user/:userId - Update user
@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.form
    username = data.get('username')
    visibility = data.get('visibility')

    if not username or not visibility:
        return jsonify({"error": "Missing fields"}), 400

    # Check if the user exists before updating
    existing_user_query = 'SELECT * FROM "User" WHERE "UserID" = %s'
    existing_user = execute_query(
        existing_user_query, (user_id,), fetch_one=True)

    if not existing_user:
        return jsonify({"error": "User not found"}), 404

    query = '''
        UPDATE "User"
        SET "Username" = %s, "Visibility" = %s
        WHERE "UserID" = %s
    '''
    result = execute_query(query, (username, visibility, user_id))

    # Check if any rows were updated
    if result is None or result == 0:  # No rows affected
        return jsonify({"error": "User update failed"}), 500

    return jsonify({"message": "User updated"}), 200


# GET /user/:userId - Get user by UserID
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    query = 'SELECT * FROM "User" WHERE "UserID" = %s'
    user = execute_query(query, (user_id,), fetch_one=True)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user), 200


# ============================
#     DIARY ENTRY ROUTES
# ============================

# POST /entry/ - Create a new diary entry
@app.route('/entry/', methods=['POST'])
def create_diary_entry():
    data = request.form
    date = data.get('date')  # Get the date from the form data
    description = data.get('description')  # Get the description
    visibility = data.get('visibility')  # Get the visibility
    user_id = data.get('userId')  # Get the user ID

    # Validate required fields
    if not date or not visibility or not user_id:
        return jsonify({"error": "Missing fields"}), 400

    # Check if a diary entry already exists for this date and user
    existing_entry_query = '''
        SELECT * FROM "DiaryEntry" WHERE "Date" = %s AND "UserID" = %s
    '''
    existing_entry = execute_query(
        existing_entry_query, (date, user_id), fetch_one=True)

    if existing_entry:
        return jsonify({"error": "Diary entry for this date already exists"}), 400

    query = '''
        INSERT INTO "DiaryEntry" ("Date", "Description", "Visibility", "UserID")
        VALUES (%s, %s, %s, %s) RETURNING "EntryID"
    '''
    entry_id = execute_query(
        query, (date, description, visibility, user_id), fetch_one=True)

    if entry_id is None:
        return jsonify({"error": "Diary entry creation failed"}), 500

    return jsonify({"message": "Diary entry created", "EntryID": entry_id}), 201


# PUT /entry/<int:entry_id> - Update a diary entry
@app.route('/entry/<int:entry_id>', methods=['PUT'])
def update_diary_entry(entry_id):
    data = request.form
    description = data.get('description')  # Get the description
    visibility = data.get('visibility')  # Get the visibility

    # Validate required fields
    if not visibility:
        return jsonify({"error": "Missing fields"}), 400

    # Update query
    query = '''
        UPDATE "DiaryEntry"
        SET "Description" = %s, "Visibility" = %s
        WHERE "EntryID" = %s
    '''
    result = execute_query(query, (description, visibility, entry_id))

    if result is None or result == 0:
        return jsonify({"error": "Diary entry not found"}), 404

    return jsonify({"message": "Diary entry updated", "EntryID": entry_id}), 200


# DELETE /entry/:entryId - Delete diary entry
@app.route('/entry/<int:entry_id>', methods=['DELETE'])
def delete_diary_entry(entry_id):
    query = 'DELETE FROM "DiaryEntry" WHERE "EntryID" = %s'

    res = execute_query(query, (entry_id,))
    if not res:
        return jsonify({"error": f"Entry {entry_id} not found"}), 404

    return jsonify({"message": "Diary entry deleted"}), 200


# ============================
#      DIARY REPORT ROUTES
# ============================

@app.route('/report/', methods=['POST'])
def create_diary_report():
    data = request.form
    date = data.get('date')
    description = data.get('description')
    visibility = data.get('visibility')
    user_id = data.get('userId')

    if not date or not visibility or not user_id:
        return jsonify({"error": "Missing fields"}), 400

    existing_entry_query = '''
        SELECT * FROM "DiaryReport" WHERE "Date" = %s AND "UserID" = %s
    '''
    existing_entry = execute_query(
        existing_entry_query, (date, user_id), fetch_one=True)

    if existing_entry:
        return jsonify({"error": "Diary report for this date already exists"}), 400

    query = '''
        INSERT INTO "DiaryReport" ("Date", "Description", "Visibility", "UserID")
        VALUES (%s, %s, %s, %s) RETURNING "ReportID"
    '''
    report_id = execute_query(
        query, (date, description, visibility, user_id), fetch_one=True)

    if report_id is None:
        return jsonify({"error": "Diary report creation failed"}), 500

    return jsonify({"message": "Diary report created", "ReportId": report_id}), 201


@app.route('/report/<int:report_id>', methods=['PUT'])
def update_diary_report(report_id):
    data = request.form
    description = data.get('description')
    visibility = data.get('visibility')

    if not visibility:
        return jsonify({"error": "Missing fields"}), 400

    query = '''
        UPDATE "DiaryReport"
        SET "Description" = %s, "Visibility" = %s
        WHERE "ReportID" = %s
    '''
    result = execute_query(query, (description, visibility, report_id))

    if result is None or result == 0:
        return jsonify({"error": "Diary report not found"}), 404

    return jsonify({"message": "Diary report updated", "ReportID": report_id}), 200


# DELETE /report/:reportId - Delete a report
@app.route('/report/<int:report_id>', methods=['DELETE'])
def delete_report(report_id):
    query = 'DELETE FROM "DiaryReport" WHERE "ReportID" = %s'
    result = execute_query(query, (report_id,))

    if not result:
        return jsonify({"error": "Report not found"}), 404

    return jsonify({"message": "Report deleted"}), 200


# ============================
#       REVIEW ROUTES
# ============================

# POST /review/:songId - Create a review for a song
@app.route('/review/<int:song_id>', methods=['POST'])
def create_review(song_id):
    data = request.form
    contents = data.get('contents')
    visibility = data.get('visibility')

    if not contents or not visibility:
        return jsonify({"error": "Missing fields"}), 400

    existing_review_query = 'SELECT * FROM "Review" WHERE "SongID" = %s'
    existing_user = execute_query(
        existing_review_query, (song_id,), fetch_one=True)

    if existing_user:
        return jsonify({"error": "Review for song already exists"}), 400

    query = '''
        INSERT INTO "Review" ("Contents", "Visibility", "SongID")
        VALUES (%s, %s, %s) RETURNING "ReviewID"
    '''
    review_id = execute_query(
        query, (contents, visibility, song_id), fetch_one=True)

    return jsonify({"message": "Review created", "ReviewID": review_id}), 201


@app.route('/review/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    data = request.form
    contents = data.get('contents')  # Get the description
    visibility = data.get('visibility')  # Get the visibility

    # Validate required fields
    if not visibility or not contents:
        return jsonify({"error": "Missing fields"}), 400

    # Update query
    query = '''
        UPDATE "Review"
        SET "Contents" = %s, "Visibility" = %s
        WHERE "ReviewID" = %s
    '''
    result = execute_query(query, (contents, visibility, review_id))

    if result is None or result == 0:
        return jsonify({"error": "Diary entry not found"}), 404

    return jsonify({"message": "Diary entry updated", "ReviewId": review_id}), 200


@app.route('/review/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    query = 'DELETE FROM "Review" WHERE "ReviewID" = %s'
    existing_review = execute_query(query, (review_id,))

    if not existing_review:
        return jsonify({"error": f"Review {review_id} not found"}), 404

    return jsonify({"message": "Review deleted"}), 200


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
