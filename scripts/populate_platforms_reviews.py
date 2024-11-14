import requests

BASE_URL = "http://localhost:5400"

platforms = ["Spotify", "Apple Music", "YouTube Music"]

reviews = [
    {
        "contents": "Great song!",
        "visibility": "public",
        "song_name": "The 1975",
        "user_username": "Ben",
    },
    {
        "contents": "Great guitar work",
        "visibility": "private",
        "song_name": "Reptilia",
        "user_username": "Bob",
    },
    {
        "contents": "My favorite song",
        "visibility": "public",
        "song_name": "A Change of Heart",
        "user_username": "Patrick",
    },
]

song_platform_links = {
    "The 1975": ["Spotify", "Apple Music"],
    "Settle Down": ["Spotify", "YouTube Music"],
    "A Change of Heart": ["Apple Music", "YouTube Music"],
}

# ========================================================================
#   Code below was largely written with ChatGPT to save time
#   This is non-critical code that just adds sample data to the database
# ========================================================================


# Add Streaming Platforms
for platform in platforms:
    response = requests.post(f"{BASE_URL}/platform/", data={"name": platform})
    print(
        f"Adding platform: {platform} - Status: {response.status_code}, Response: {response.json()}"
    )


# Add Reviews
for review in reviews:
    # Get Song by Name
    song_response = requests.get(
        f"{BASE_URL}/song/{review['song_name'].replace(' ', '%20')}"
    )
    if song_response.status_code != 200:
        print(
            f"Failed to fetch song: {review['song_name']} - Status: {song_response.status_code}"
        )
        continue
    song_data = song_response.json()
    song_id = song_data.get("SongID")

    # Get User by Username
    user_response = requests.get(f"{BASE_URL}/user/{review['user_username']}")
    if user_response.status_code != 200:
        print(
            f"Failed to fetch user: {review['user_username']} - Status: {user_response.status_code}"
        )
        continue
    user_data = user_response.json()
    user_id = user_data.get("UserID")

    # Add Review
    review_response = requests.post(
        f"{BASE_URL}/review/",
        data={
            "contents": review["contents"],
            "visibility": review["visibility"],
            "songId": song_id,
            "userId": user_id,
        },
    )
    print(
        f"Adding review for song '{review['song_name']}' by user '{review['user_username']}' - Status: {review_response.status_code}, Response: {review_response.json()}"
    )

# Link Songs to Platforms
for song, linked_platforms in song_platform_links.items():
    # Get Song by Name
    song_response = requests.get(f"{BASE_URL}/song/{song}")
    if song_response.status_code != 200:
        print(
            f"Failed to fetch song: {song} - Status: {song_response.status_code}, Response: {song_response.json()}"
        )
        continue
    song_data = song_response.json()
    song_id = song_data.get("SongID")

    for platform in linked_platforms:
        # Get Platform by Name
        platform_response = requests.get(
            f"{BASE_URL}/platform/{platform}",
        )
        if platform_response.status_code != 200:
            print(
                f"Failed to fetch platform: {platform} - Status: {platform_response.status_code}, Response: {platform_response.json()}"
            )
            continue
        platform_data = platform_response.json()
        platform_id = platform_data.get("StreamingPlatformID")

        # Link Song to Platform
        link_response = requests.post(
            f"{BASE_URL}/platform_song/",
            data={"streamingPlatformId": platform_id, "songId": song_id},
        )
        print(
            f"Linking song '{song}' to platform '{platform}' - Status: {link_response.status_code}, Response: {link_response.json()}"
        )
