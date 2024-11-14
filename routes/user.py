from typing import Any
from flask import Blueprint
from helpers import handle_request, execute_query, delete_resource_with_multiple_keys

bp = Blueprint("user", __name__)


# ============================
#         USER ROUTES
# ============================


@bp.route("/user/", methods=["POST"])
def create_user() -> Any:
    return handle_request(
        "User", "create", ["username", "visibility", "password", "isAdmin"], "UserID"
    )


@bp.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id) -> Any:
    if user_id == "all":
        return handle_request("User", "get", [], "*", "all")
    return handle_request("User", "get", [], "UserID", user_id)


@bp.route("/user/<string:username>", methods=["GET"])
def get_user_by_username(username) -> Any:
    return handle_request("User", "get", [], "Username", username)


@bp.route("/user/<int:user_id>", methods=["PUT"])
def update_user(user_id) -> Any:
    return handle_request(
        "User",
        "update",
        ["username", "visibility", "password", "isAdmin"],
        "UserID",
        user_id,
    )


@bp.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id) -> Any:
    return handle_request("User", "delete", [], "UserID", user_id)


# ============================
#     USER FRIENDS ROUTES
# ============================


@bp.route("/user_friend/", methods=["POST"])
def create_user_friend() -> Any:
    return handle_request("UserFriends", "create", ["userId", "friendUserId"], None)


@bp.route("/user_friend/<int:user_id>/<int:friend_user_id>", methods=["GET"])
def get_user_friend(user_id, friend_user_id) -> Any:
    return handle_request(
        "UserFriends", "get", [], ["UserID", "FriendUserID"], (user_id, friend_user_id)
    )


@bp.route("/user_friends/<int:user_id>", methods=["GET"])
def get_user_friends(user_id) -> Any:
    print(f"UserID from URL: {user_id}")

    query = f'SELECT u."UserID", u."Username" FROM "User" u JOIN "UserFriends" uf ON u."UserID" = uf."FriendUserID" WHERE uf."UserID" = {user_id};'
    friends = execute_query(query)
    print(friends)
    return friends


@bp.route("/user_friend/<int:user_id>/<int:friend_user_id>", methods=["DELETE"])
def delete_user_friend(user_id, friend_user_id) -> Any:
    return delete_resource_with_multiple_keys(
        "UserFriends", ["UserID", "FriendUserID"], (user_id, friend_user_id)
    )
