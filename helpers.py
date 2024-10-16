import psycopg2
from psycopg2.extras import RealDictCursor
from flask import request, jsonify


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

    # TODO: add better handling of intermediary tables where max_id doesn't matter.
    # the seq name is none if you try to run it in that case

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

    insert_query = f'INSERT INTO "{table}" ({keys}) VALUES ({values})'
    # NOTE: commented out to avoid issues with multi-key tables (also didn't really work anyway)
    # f'INSERT INTO "{table}" ({keys}) VALUES ({values}) RETURNING "{primary_key}"'
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


def format_param_key(key):
    if key.startswith("new-"):
        return "new-" + key[4].upper() + key[5:].replace("Id", "ID")
    return key[0].upper() + key[1:].replace("Id", "ID")


def update_resource_with_multiple_keys(table, data, primary_keys, identifier):
    params = {key: data.get(key) for key in data.keys()}
    formatted_params = {format_param_key(key): value for key, value in params.items()}
    set_clause = ", ".join(
        [
            f'"{format_param_key(key[4:])}" = %s'
            for key in params.keys()
            if key.startswith("new-")
        ]
    )
    where_clause = " AND ".join([f'"{key}" = %s' for key in primary_keys])
    query = f"""
    UPDATE "{table}"
    SET {set_clause}
    WHERE {where_clause}
    """
    print(query)
    set_values = tuple(formatted_params[f"new-{key}"] for key in primary_keys)
    where_values = identifier
    values = set_values + where_values
    print(values)
    result = execute_query(query, values)
    if result is None or result == 0:
        return jsonify({"error": f"{table} update failed"}), 404
    return jsonify({"message": f"{table} updated successfully!"}), 200


def delete_resource_with_multiple_keys(table, primary_keys, identifier):
    where_clause = " AND ".join([f'"{key}" = %s' for key in primary_keys])
    query = f"""
    DELETE FROM "{table}"
    WHERE {where_clause}
    """
    print(query)
    values = identifier
    print(values)
    result = execute_query(query, values)
    if result is None or result == 0:
        return jsonify({"error": f"{table} deletion failed"}), 404
    return jsonify({"message": f"{table} deleted successfully!"}), 200


def handle_request(table, operation, required_fields, primary_key, identifier=None):
    print(
        f"Request received: {table}, {operation}, {required_fields}, {primary_key}, {identifier}"
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
        if isinstance(identifier, tuple):
            result = None
            print("don't use handle_request for multiple key deletes/updates")
        else:
            result = update_resource(table, params, identifier, primary_key)
        if result is None or result == 0:
            return jsonify({"error": f"{table} update failed"}), 404
        return jsonify({"message": f"{table} updated"}), 200

    elif operation.lower() == "delete":
        if isinstance(identifier, tuple):
            result = None
            print("don't use handle_request for multiple key deletes/updates")
        else:
            result = delete_resource(table, identifier, primary_key)
        if result is None or result == 0:
            return jsonify({"error": f"{table} not found"}), 404
        return jsonify({"message": f"{table} deleted"}), 200
