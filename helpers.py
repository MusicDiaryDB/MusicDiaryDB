from functools import wraps
from typing import Tuple, Union
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import request, jsonify, Response, session


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
    if primary_key and isinstance(primary_key, str):
        max_id_query = f'SELECT MAX("{primary_key}") FROM "{table}"'
        max_id_result = execute_query(max_id_query, fetch_one=True)

        max_id = None
        if isinstance(max_id_result, dict):
            max_id = max_id_result.get("max")
            print(f"Max ID = {max_id}")
        else:
            print("Failed to get max id result")

        table_quoted = f'"{table}"'
        seq_name_query = (
            f"SELECT pg_get_serial_sequence('{table_quoted}', '{primary_key}')"
        )
        seq_name_result = execute_query(seq_name_query, fetch_one=True)

        seq_name = None
        if seq_name_result and isinstance(seq_name_result, dict):
            seq_name = seq_name_result.get("pg_get_serial_sequence")
        else:
            print(
                f"No sequence found for table '{table}' and primary key '{primary_key}'"
            )

        if seq_name is not None and max_id is not None:
            setval_query = f"SELECT setval('{seq_name}', {max_id})"
            execute_query(setval_query)
    else:
        print(f"Table '{table}' has no single primary key. Skipping sequence reset.")

    keys = ", ".join([f'"{format_column_name(key)}"' for key in params.keys()])
    values = ", ".join(["%s" for _ in params.keys()])

    insert_query = f'INSERT INTO "{table}" ({keys}) VALUES ({values})'
    print(insert_query)

    result = execute_query(insert_query, tuple(params.values()))
    if result is not None and primary_key and isinstance(primary_key, str):
        return get_last_insert_id(table, primary_key)
    else:
        return True

def create_user_resource(table, params):
    try:
        keys = ", ".join([f'"{format_column_name(key)}"' for key in params.keys()])
        values = ", ".join(["%s" for _ in params.keys()])
        insert_query = f'INSERT INTO "{table}" ({keys}) VALUES ({values})'

        
        result = execute_query(insert_query, tuple(params.values()))
        
        
        if result is not None:
            return {"message": "User created successfully"}, 201
        else:
            
            return {"error": "User creation failed"}, 500

    except psycopg2.errors.UniqueViolation:
        # Handle unique constraint error for username
        return {"error": "Username already exists"}, 409
    except Exception as e:
        # Handle generic errors and provide more context in logs for debugging
        print(f"Error during user creation: {e}")
        return {"error": "User creation failed due to server error"}, 500

#Helper function to restrict users from accessing admin controls/Checking for admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the user is logged in
        if 'user_id' not in session:
            return jsonify({"error": "Authentication required"}), 401

        # Retrieve user_id from session
        user_id = session.get('user_id')

        # Retrieve the user from the database to verify if they are an admin
        user = get_resource("User", user_id, "UserID")
        if not user or not user.get('IsAdmin'):
            return jsonify({"error": "Admin access is required"}), 403

        # If the user is an admin, call the original function
        return f(*args, **kwargs)
    return decorated_function


def get_last_insert_id(table, primary_key):
    query = f'SELECT MAX("{primary_key}") AS id FROM "{table}"'
    result = execute_query(query, fetch_one=True)
    if result and "id" in result:
        return result["id"]
    else:
        return None


def update_resource(table, params, identifier, primary_key):
    set_clause = ", ".join(
        [f'"{format_column_name(key)}" = %s' for key in params.keys()]
    )
    query = f'UPDATE "{table}" SET {set_clause} WHERE "{primary_key}" = %s'
    return execute_query(query, tuple(params.values()) + (identifier,))


def delete_resource(table, identifier, primary_key):
    query = f'DELETE FROM "{table}" WHERE "{primary_key}" = %s'
    return execute_query(query, (identifier,))


def get_resource(table, identifier, primary_key):
    query = f'SELECT * FROM "{table}" WHERE "{primary_key}" = %s'
    return execute_query(query, (identifier,), fetch_one=True)


def get_all_resources(table, identifier):
    query = f'SELECT * FROM "{table}"'
    return execute_query(query, (identifier,), fetch_one=False)


def format_column_name(key):
    return key[0].upper() + key[1:].replace("Id", "ID")


def update_resource_with_multiple_keys(table, data, primary_keys, identifiers):
    params = {key: data.get(key) for key in data.keys() if data.get(key)}
    formatted_params = {format_column_name(key): value for key, value in params.items()}

    set_clause = ", ".join([f'"{key}" = %s' for key in formatted_params.keys()])
    where_clause = " AND ".join(
        [f'"{format_column_name(pk)}" = %s' for pk in primary_keys]
    )

    query = f'UPDATE "{table}" SET {set_clause} WHERE {where_clause}'
    print(query)

    values = tuple(formatted_params.values()) + identifiers
    result = execute_query(query, values)
    if result is None or result == 0:
        return jsonify({"error": f"{table} update failed"}), 404
    return jsonify({"message": f"{table} updated successfully!"}), 200


def delete_resource_with_multiple_keys(table, primary_keys, identifiers):
    where_clause = " AND ".join(
        [f'"{format_column_name(pk)}" = %s' for pk in primary_keys]
    )
    query = f'DELETE FROM "{table}" WHERE {where_clause}'
    print(query)

    result = execute_query(query, identifiers)
    if result is None or result == 0:
        return jsonify({"error": f"{table} deletion failed"}), 404
    return jsonify({"message": f"{table} deleted successfully!"}), 200


def get_resource_with_multiple_keys(table, primary_keys, identifiers):
    where_clause = " AND ".join(
        [f'"{format_column_name(pk)}" = %s' for pk in primary_keys]
    )
    query = f'SELECT * FROM "{table}" WHERE {where_clause}'
    result = execute_query(query, identifiers, fetch_one=True)
    if result is None:
        return jsonify({"error": f"{table} not found"}), 404
    return jsonify(result), 200


def handle_request(
    table, operation, required_fields, primary_key, identifier=None
) -> Tuple[Union[Response, None], int]:
    print(
        f"Request received: {table}, {operation}, {required_fields}, {primary_key}, {identifier}"
    )
    print(request)

    data = request.form
    params = {field: data.get(field) for field in required_fields}

    # special case for setting create user
    if table == "User":
        if params.get("isAdmin") is None:
            params["isAdmin"] = "false"

    if any(value is None for value in params.values()):
        missing_fields = [field for field in params if params[field] is None]
        return jsonify({"error": f"Missing fields: {missing_fields}"}), 400

    if operation.lower() == "create":
        resource_created = create_resource(table, params, primary_key)
        if not resource_created:
            return jsonify({"error": f"{table} creation failed"}), 500
        response = {"message": f"{table} created"}
        if primary_key and isinstance(primary_key, str):
            response[primary_key] = resource_created
        return jsonify(response), 201

    elif operation.lower() == "update":
        if isinstance(primary_key, list) and isinstance(identifier, tuple):
            return update_resource_with_multiple_keys(
                table, data, primary_key, identifier
            )
        else:
            result = update_resource(table, params, identifier, primary_key)
            if result is None or result == 0:
                return jsonify({"error": f"{table} update failed"}), 404
            return jsonify({"message": f"{table} updated"}), 200

    elif operation.lower() == "delete":
        if isinstance(primary_key, list) and isinstance(identifier, tuple):
            return delete_resource_with_multiple_keys(table, primary_key, identifier)
        else:
            result = delete_resource(table, identifier, primary_key)
            if result is None or result == 0:
                return jsonify({"error": f"{table} not found"}), 404
            return jsonify({"message": f"{table} deleted"}), 200

    elif operation.lower() == "get":
        if identifier == "all":
            return get_all_resources(table, identifier)
        if isinstance(primary_key, list) and isinstance(identifier, tuple):
            return get_resource_with_multiple_keys(table, primary_key, identifier)
        if isinstance(primary_key, list) and identifier == "all":
            return get_all_resources_by_key(
                table, primary_key[0], primary_key_value=identifier[0]
            )
        else:
            resource = get_resource(table, identifier, primary_key)
            if resource is None:
                return jsonify({"error": f"{table} not found"}), 404
            return jsonify(resource), 200
    return None, 404


def get_reviews_for_song(song_id):
    query = """
    SELECT r."ReviewID", r."Contents", r."Visibility", u."Username"
    FROM "Review" r
    JOIN "User" u ON r."UserID" = u."UserID"
    WHERE r."SongID" = %s AND r."Visibility" = 'PUBLIC'
    """
    return execute_query(query, (song_id,))


def get_all_resources_by_key(table, key, primary_key_value):
    query = f"SELECT * FROM {table} WHERE {key} = %s"
    cursor.execute(query, (primary_key_value,))
    results = cursor.fetchall()
    return jsonify(results), 200


def check_query_result(result):
    if result is None or result == 0:
        return jsonify({"error": "Table update failed"}), 500
    return jsonify({"result": result}), 200


# Use this over 'execute_query' if you are directly returning the result
def execute_query_ret_result(query, params=None):
    return check_query_result(execute_query(query, params))
