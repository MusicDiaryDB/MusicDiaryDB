from typing import Any
from flask import Blueprint, request
from helpers import execute_query_ret_result, execute_query

bp = Blueprint("admin", __name__)

# ==========================
#   Add/Remove Admin Users
# ==========================


# Make a user into an admin user
@bp.route("/admin/add/<string:username>", methods=["PUT"])
def make_user_admin(username):
    print(request)
    query = """
    UPDATE "User"
    SET "IsAdmin" = TRUE
    WHERE "Username" = %s;
    """
    return execute_query_ret_result(query, (username,))


# Remove admin status from a user
@bp.route("/admin/remove/<string:username>", methods=["PUT"])
def remove_user_admin(username):
    print(request)
    query = """
    UPDATE "User"
    SET "IsAdmin" = FALSE
    WHERE "Username" = %s;
    """
    return execute_query_ret_result(query, (username,))


# ======================
#     DB HEALTH/INFO
# ======================

#
# Info metrics
#


@bp.route("/admin/info/rows", methods=["GET"])
def get_db_info() -> Any:
    print(request)
    # This query relies on up to data schema information
    # Analyze query must be run or it will likely be out-of-date
    execute_query("ANALYZE;")
    query = """
    SELECT
        schemaname AS schema,
        relname AS table,
        n_live_tup AS row_count
    FROM
        pg_stat_user_tables
    ORDER BY
        row_count DESC;
    """
    return execute_query_ret_result(query)


@bp.route("/admin/info/dbsize", methods=["GET"])
def get_db_size() -> Any:
    print(request)
    execute_query("ANALYZE;")
    query = (
        "SELECT pg_size_pretty(pg_database_size(current_database())) AS database_size;"
    )
    return execute_query_ret_result(query)


@bp.route("/admin/info/tablesize", methods=["GET"])
def get_table_sizes():
    print(request)
    execute_query("ANALYZE;")
    query = """
    SELECT
        schemaname AS schema,
        relname AS table,
        pg_size_pretty(pg_total_relation_size(relid)) AS total_size
    FROM
        pg_catalog.pg_statio_user_tables
    ORDER BY
        pg_total_relation_size(relid) DESC;
    """
    return execute_query_ret_result(query)


@bp.route("/admin/info/conns", methods=["GET"])
def get_info_num_conns():
    print(request)
    execute_query("ANALYZE;")
    query = """
    SELECT
        count(*) AS total_connections
    FROM
        pg_stat_activity;
    """
    return execute_query_ret_result(query)


@bp.route("/admin/info/conns-activity", methods=["GET"])
def get_info_conns_activity():
    print(request)
    execute_query("ANALYZE;")
    query = """
    SELECT
        state,
        count(*) AS count
    FROM
        pg_stat_activity
    GROUP BY
        state;
    """
    return execute_query_ret_result(query)


#
# Performance metrics
#


@bp.route("/admin/perf/cache-hit-ratio", methods=["GET"])
def get_perf_cache_hit_ratios():
    print(request)
    # execute_query("ANALYZE;")
    query = "SELECT sum(blks_hit) / (sum(blks_hit) + sum(blks_read)) AS cache_hit_ratio FROM pg_stat_database;"
    return execute_query_ret_result(query)


@bp.route("/admin/perf/long-running-queries", methods=["GET"])
def get_perf_long_running_queries():
    print(request)
    # execute_query("ANALYZE;")
    query = """
    SELECT
        pid,
        now() - pg_stat_activity.query_start AS duration,
        query
    FROM
        pg_stat_activity
    WHERE
        state = 'active'
        AND (now() - pg_stat_activity.query_start) > interval '5 minutes'
    ORDER BY
        duration DESC;
    """
    return execute_query_ret_result(query)
