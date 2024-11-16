import requests
import random
from music_data import data

BASE_URL = "http://localhost:5400"

platforms = [
    "Spotify",
    "Apple Music",
    "YouTube Music",
    "Tidal",
    "Amazon Music",
    "SoundCloud",
    "Locally Hosted",
]


# Add Streaming Platforms
for platform in platforms:
    response = requests.post(f"{BASE_URL}/platform/", data={"name": platform})
    print(
        f"Adding platform: {platform} - Status: {response.status_code}, Response: {response.json()}"
    )

# Generate and Add Reviews for Songs
for artist, albums in data.items():
    for album, songs in albums.items():
        for song in songs:
            # Get Song by Name
            song_response = requests.get(f"{BASE_URL}/song/{song.replace(' ', '%20')}")
            if song_response.status_code != 200:
                print(
                    f"Failed to fetch song: {song} - Status: {song_response.status_code}"
                )
                continue
            song_data = song_response.json()
            song_id = song_data.get("SongID")

            # Generate Review Data
            review_content = random.choice(
                [
                    "This track is phenomenal!",
                    "Absolutely love it!",
                    "A timeless masterpiece.",
                    "This song is on repeat!",
                    "Can't stop listening to this one!",
                ]
            )
            review_visibility = random.choice(["public", "private"])
            user_username = random.choice(["admin", "Patrick", "Ben", "Bob"])

            # Get User by Username
            user_response = requests.get(f"{BASE_URL}/user/{user_username}")
            if user_response.status_code != 200:
                print(
                    f"Failed to fetch user: {user_username} - Status: {user_response.status_code}"
                )
                continue
            user_data = user_response.json()
            user_id = user_data.get("UserID")

            # Add Review
            review_response = requests.post(
                f"{BASE_URL}/review/",
                data={
                    "contents": review_content,
                    "visibility": review_visibility,
                    "songId": song_id,
                    "userId": user_id,
                },
            )
            print(
                f"Adding review for song '{song}' - Status: {review_response.status_code}, Response: {review_response.json()}"
            )

# Link Songs to Platforms
for platform in platforms:
    response = requests.post(f"{BASE_URL}/platform/", data={"name": platform})
    print(
        f"Adding platform: {platform} - Status: {response.status_code}, Response: {response.json()}"
    )

# Randomly Assign Songs to Platforms
for artist, albums in data.items():
    for album, songs in albums.items():
        for song in songs:
            # Fetch Song by Name
            song_response = requests.get(f"{BASE_URL}/song/{song.replace(' ', '%20')}")
            if song_response.status_code != 200:
                print(
                    f"Failed to fetch song: {song} - Status: {song_response.status_code}"
                )
                continue
            song_data = song_response.json()
            song_id = song_data.get("SongID")

            # Randomly Assign Platforms
            assigned_platforms = random.sample(
                platforms, k=random.randint(1, len(platforms))
            )
            for platform in assigned_platforms:
                # Fetch Platform by Name
                platform_response = requests.get(f"{BASE_URL}/platform/{platform}")
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
