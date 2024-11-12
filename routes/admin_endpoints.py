from flask import Blueprint, jsonify
from helpers import handle_request, execute_query

bp = Blueprint("admin", __name__)


# Generate a managerial report about database-wide information
@bp.route("/admin/report", methods=["GET"])
def generate_managerial_report():
    # TODO: aggregation query?

    return {}


# Make a user into an admin user
@bp.route("/admin/add/<string:username>", methods=["PUT"])
def make_user_admin(username):
    query = """
    UPDATE "User"
    SET "IsAdmin" = TRUE
    WHERE "Username" = %s;
    """
    return jsonify(execute_query(query, (username,))), 200


# Remove admin status from a user
@bp.route("/admin/remove/<string:username>", methods=["PUT"])
def remove_user_admin(username):
    query = """
    UPDATE "User"
    SET "IsAdmin" = FALSE
    WHERE "Username" = %s;
    """
    return jsonify(execute_query(query, (username,))), 200
