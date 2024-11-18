import requests
from music_data import data

BASE_URL = "http://localhost:5400"

for artist in data.keys():
    response = requests.post(f"{BASE_URL}/artist/", data={"name": artist})
    print(
        f"Adding artist: {artist} - Status: {response.status_code}, Response: {response.json()}"
    )

for artist, album_data in data.items():
    for album, songs in album_data.items():
        album_response = requests.post(
            f"{BASE_URL}/album/{artist.replace(' ', '%20')}", data={"name": album}
        )
        print(
            f"Adding album: {album} for artist: {artist} - Status: {album_response.status_code}, Response: {album_response.json()}"
        )

        for song in songs:
            song_response = requests.post(
                f"{BASE_URL}/song/{album.replace(' ', '%20')}", data={"name": song}
            )
            print(
                f"Adding song: {song} to album: {album} - Status: {song_response.status_code}, Response: {song_response.json()}"
            )
