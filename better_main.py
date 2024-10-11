#
# NOTE: This file is a WIP, but should be easier to work with than the original main.py
# - it may or may not work correctly currently
#

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


def create_resource(table, params):
    keys = ', '.join([f'"{key.capitalize()}"' for key in params.keys()])
    values = ', '.join(['%s' if 'id' not in key.lower()
                       else '%s' for key in params.keys()])
    query = f'INSERT INTO "{table}" ({keys}) VALUES ({values}) RETURNING "{
        table}ID"'
    return execute_query(query, tuple(params.values()), fetch_one=True)


def update_resource(table, params, identifier):
    set_clause = ', '.join(
        [f'"{key.capitalize()}" = %s' for key in params.keys()])
    query = f'UPDATE "{table}" SET {set_clause} WHERE "{table}ID" = %s'
    return execute_query(query, tuple(params.values()) + (identifier,))


def delete_resource(table, identifier):
    query = f'DELETE FROM "{table}" WHERE "{table}ID" = %s'
    return execute_query(query, (identifier,))


def get_resource(table, identifier):
    query = f'SELECT * FROM "{table}" WHERE "{table}ID" = %s'
    return execute_query(query, (identifier,), fetch_one=True)


# Reusable function for parameter extraction, validation, and response handling
def handle_request(table, operation, required_fields, identifier=None):
    # Extract and validate parameters
    data = request.form
    params = {field: data.get(field) for field in required_fields}

    if any(value is None for value in params.values()):
        return jsonify({"error": "Missing fields"}), 400

    # Perform the requested operation
    if operation.lower() == 'create':
        resource_id = create_resource(table, params)
        if resource_id is None:
            return jsonify({"error": f"{table} creation failed"}), 500
        return jsonify({"message": f"{table} created", f"{table[:-1].capitalize()}ID": resource_id}), 201

    elif operation.lower() == 'update':
        result = update_resource(table, params, identifier)
        if result is None or result == 0:
            return jsonify({"error": f"{table} update failed"}), 404
        return jsonify({"message": f"{table} updated"}), 200

    elif operation.lower() == 'delete':
        result = delete_resource(table, identifier)
        if result is None or result == 0:
            return jsonify({"error": f"{table} not found"}), 404
        return jsonify({"message": f"{table} deleted"}), 200

# ============================
#         USER ROUTES
# ============================


@app.route('/user/', methods=['POST'])
def create_user():
    return handle_request('User', 'create', ['username', 'visibility'])


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = get_resource('User', user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200


@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    return handle_request('User', 'update', ['username', 'visibility'], user_id)


@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return handle_request('User', 'delete', [], user_id)

# ============================
#     DIARY ENTRY ROUTES
# ============================


@app.route('/entry/', methods=['POST'])
def create_diary_entry():
    return handle_request('DiaryEntry', 'create', ['date', 'description', 'visibility', 'userId'])


@app.route('/entry/<int:entry_id>', methods=['GET'])
def get_diary_entry(entry_id):
    entry = get_resource('DiaryEntry', entry_id)
    if not entry:
        return jsonify({"error": "Diary entry not found"}), 404
    return jsonify(entry), 200


@app.route('/entry/<int:entry_id>', methods=['PUT'])
def update_diary_entry(entry_id):
    return handle_request('DiaryEntry', 'update', ['description', 'visibility'], entry_id)


@app.route('/entry/<int:entry_id>', methods=['DELETE'])
def delete_diary_entry(entry_id):
    return handle_request('DiaryEntry', 'delete', [], entry_id)

# ============================
#      DIARY REPORT ROUTES
# ============================


@app.route('/report/', methods=['POST'])
def create_diary_report():
    return handle_request('DiaryReport', 'create', ['date', 'description', 'visibility', 'userId'])


@app.route('/report/<int:report_id>', methods=['GET'])
def get_diary_report(report_id):
    report = get_resource('DiaryReport', report_id)
    if not report:
        return jsonify({"error": "Diary report not found"}), 404
    return jsonify(report), 200


@app.route('/report/<int:report_id>', methods=['PUT'])
def update_diary_report(report_id):
    return handle_request('DiaryReport', 'update', ['description', 'visibility'], report_id)


@app.route('/report/<int:report_id>', methods=['DELETE'])
def delete_diary_report(report_id):
    return handle_request('DiaryReport', 'delete', [], report_id)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
