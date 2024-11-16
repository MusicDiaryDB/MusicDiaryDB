import requests
import random

BASE_URL = "http://localhost:5400"

users = [
    {
        "username": "admin",
        "visibility": "PRIVATE",
        "password": "admin",
        "is_admin": True,
    },
    {
        "username": "Patrick",
        "visibility": "FRIENDS",
        "password": "12345",
        "is_admin": True,
    },
    {
        "username": "Ben",
        "visibility": "PUBLIC",
        "password": "password123",
        "is_admin": False,
    },
    {
        "username": "Bob",
        "visibility": "PUBLIC",
        "password": "securepassword",
        "is_admin": False,
    },
    {
        "username": "Charlie",
        "visibility": "PRIVATE",
        "password": "mypassword",
        "is_admin": False,
    },
]

friendships = [
    ("admin", "Patrick"),
    ("admin", "Ben"),
    ("Patrick", "Bob"),
    ("Ben", "Charlie"),
    ("Bob", "Charlie"),
]

# ========================================================================
#   Code below was largely written with ChatGPT to save time
#   This is non-critical code that just adds sample data to the database
# ========================================================================

# Generate 26 additional synthetic users
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
for letter in alphabet:
    users.append(
        {
            "username": f"User_{letter}",
            "visibility": random.choice(["PUBLIC", "FRIENDS", "PRIVATE"]),
            "password": f"password_{letter}",
            "is_admin": False,
        }
    )


for user in users:
    response = requests.post(
        f"{BASE_URL}/user/",
        data={
            "username": user["username"],
            "visibility": user["visibility"],
            "password": user["password"],
            "isAdmin": str(user["is_admin"]).lower(),
        },
    )
    print(
        f"Adding user: {user['username']} - Status: {response.status_code}, Response: {response.json()}"
    )


# Fetch user IDs by username
def get_user_id(username):
    response = requests.get(f"{BASE_URL}/user/{username}")
    if response.status_code != 200:
        print(
            f"Failed to fetch all users - Status: {response.status_code}, Response: {response.json()}"
        )
        return None
    user = response.json()
    if user["Username"] == username:
        return user["UserID"]
    print(f"User {username} not found.")
    return None


# Generate 30 additional friendships randomly
usernames = [user["username"] for user in users]
for _ in range(30):
    user1, user2 = random.sample(usernames, 2)
    if (user1, user2) not in friendships and (user2, user1) not in friendships:
        friendships.append((user1, user2))

# Add friendships
for user1, user2 in friendships:
    user1_id = get_user_id(user1)
    user2_id = get_user_id(user2)

    if user1_id is None or user2_id is None:
        print(
            f"Skipping friendship creation for {user1} and {user2} due to missing user ID(s)."
        )
        continue

    response = requests.post(
        f"{BASE_URL}/user_friend/",
        data={"userId": user1_id, "friendUserId": user2_id},
    )
    print(
        f"Adding friendship: {user1} ({user1_id}) -> {user2} ({user2_id}) - "
        f"Status: {response.status_code}, Response: {response.json()}"
    )
