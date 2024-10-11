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


def create_resource(table, params, primary_key):
    keys = ', '.join(
        [f'"{key[0].upper() + key[1:].replace("Id", "ID")}"' for key in params.keys()])
    values = ', '.join(['%s' for _ in params.keys()])
    query = f'INSERT INTO "{table}" ({keys}) VALUES ({values}) RETURNING "{
        primary_key}"'
    return execute_query(query, tuple(params.values()), fetch_one=True)


def update_resource(table, params, identifier, primary_key):
    set_clause = ', '.join(
        [f'"{key[0].upper() + key[1:].replace("Id", "ID")}" = %s' for key in params.keys()])
    query = f'UPDATE "{table}" SET {set_clause} WHERE "{primary_key}" = %s'
    return execute_query(query, tuple(params.values()) + (identifier,))


def delete_resource(table, identifier, primary_key):
    query = f'DELETE FROM "{table}" WHERE "{primary_key}" = %s'
    return execute_query(query, (identifier,))


def get_resource(table, identifier, primary_key):
    query = f'SELECT * FROM "{table}" WHERE "{primary_key}" = %s'
    return execute_query(query, (identifier,), fetch_one=True)


def handle_request(table, operation, required_fields, primary_key, identifier=None):
    # Extract and validate parameters
    data = request.form
    params = {field: data.get(field) for field in required_fields}

    if any(value is None for value in params.values()):
        return jsonify({"error": f"Missing fields: {params.values()}"}), 400

    # Perform the requested operation
    if operation.lower() == 'create':
        resource_id = create_resource(table, params, primary_key)
        if resource_id is None:
            return jsonify({"error": f"{table} creation failed"}), 500
        return jsonify({"message": f"{table} created", f"{primary_key}": resource_id}), 201

    elif operation.lower() == 'update':
        result = update_resource(table, params, identifier, primary_key)
        if result is None or result == 0:
            return jsonify({"error": f"{table} update failed"}), 404
        return jsonify({"message": f"{table} updated"}), 200

    elif operation.lower() == 'delete':
        result = delete_resource(table, identifier, primary_key)
        if result is None or result == 0:
            return jsonify({"error": f"{table} not found"}), 404
        return jsonify({"message": f"{table} deleted"}), 200


# ============================
#         USER ROUTES
# ============================

@app.route('/user/', methods=['POST'])
def create_user():
    return handle_request('User', 'create', ['username', 'visibility'], 'UserID')


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return handle_request('User', 'get', [], 'UserID', user_id)


@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    return handle_request('User', 'update', ['username', 'visibility'], 'UserID', user_id)


@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return handle_request('User', 'delete', [], 'UserID', user_id)


# ============================
#     SONG ROUTES
# ============================

@app.route('/song/', methods=['POST'])
def create_song():
    return handle_request('Song', 'create', ['name', 'releaseDate'], 'SongID')


@app.route('/song/<int:song_id>', methods=['GET'])
def get_song(song_id):
    return handle_request('Song', 'get', [], 'SongID', song_id)


@app.route('/song/<int:song_id>', methods=['PUT'])
def update_song(song_id):
    return handle_request('Song', 'update', ['name', 'releaseDate'], 'SongID', song_id)


@app.route('/song/<int:song_id>', methods=['DELETE'])
def delete_song(song_id):
    return handle_request('Song', 'delete', [], 'SongID', song_id)


# ============================
#     ALBUM ROUTES
# ============================

@app.route('/album/', methods=['POST'])
def create_album():
    return handle_request('Album', 'create', ['name'], 'AlbumID')


@app.route('/album/<int:album_id>', methods=['GET'])
def get_album(album_id):
    return handle_request('Album', 'get', [], 'AlbumID', album_id)


@app.route('/album/<int:album_id>', methods=['PUT'])
def update_album(album_id):
    return handle_request('Album', 'update', ['name'], 'AlbumID', album_id)


@app.route('/album/<int:album_id>', methods=['DELETE'])
def delete_album(album_id):
    return handle_request('Album', 'delete', [], 'AlbumID', album_id)


# ============================
#     ARTIST ROUTES
# ============================

@app.route('/artist/', methods=['POST'])
def create_artist():
    return handle_request('Artist', 'create', ['name'], 'ArtistID')


@app.route('/artist/<int:artist_id>', methods=['GET'])
def get_artist(artist_id):
    return handle_request('Artist', 'get', [], 'ArtistID', artist_id)


@app.route('/artist/<int:artist_id>', methods=['PUT'])
def update_artist(artist_id):
    return handle_request('Artist', 'update', ['name'], 'ArtistID', artist_id)


@app.route('/artist/<int:artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    return handle_request('Artist', 'delete', [], 'ArtistID', artist_id)


# ============================
#     PLATFORM ROUTES
# ============================

@app.route('/platform/', methods=['POST'])
def create_platform():
    return handle_request('StreamingPlatform', 'create', ['name'], 'StreamingPlatformID')


@app.route('/platform/<int:platform_id>', methods=['GET'])
def get_platform(platform_id):
    return handle_request('StreamingPlatform', 'get', [], 'StreamingPlatformID', platform_id)


@app.route('/platform/<int:platform_id>', methods=['PUT'])
def update_platform(platform_id):
    return handle_request('StreamingPlatform', 'update', ['name'], 'StreamingPlatformID', platform_id)


@app.route('/platform/<int:platform_id>', methods=['DELETE'])
def delete_platform(platform_id):
    return handle_request('StreamingPlatform', 'delete', [], 'StreamingPlatformID', platform_id)


# ============================
#       REVIEW ROUTES
# ============================

# POST /review/:songId - Create a review for a song
@app.route('/review/<int:song_id>', methods=['POST'])
def create_review(song_id):
    data = request.form.to_dict()
    data['songId'] = song_id
    return handle_request('Review', 'create', ['contents', 'visibility', 'songId'], 'ReviewID')


# PUT /review/:reviewId - Update a review by its ID
@app.route('/review/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    return handle_request('Review', 'update', ['contents', 'visibility'], 'ReviewID', review_id)


# DELETE /review/:reviewId - Delete a review by its ID
@app.route('/review/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    return handle_request('Review', 'delete', [], 'ReviewID', review_id)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
