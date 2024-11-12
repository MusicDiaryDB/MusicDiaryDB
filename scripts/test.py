import requests

BASE_URL = "http://127.0.0.1:5400"


def print_response(response):
    print("Status Code:", response.status_code)
    print(
        "Response JSON:",
        response.json() if response.status_code == 200 else response.text,
    )
    print()


def test_create_user():
    print("Testing Create User...")
    response = requests.post(
        f"{BASE_URL}/user/",
        json={
            "username": "testuser",
            "password": "testpassword",
            "visibility": "public",
        },
    )
    print_response(response)


def test_get_user(user_id):
    print(f"Testing Get User {user_id}...")
    response = requests.get(f"{BASE_URL}/user/{user_id}")
    print_response(response)


def test_update_user(user_id):
    print(f"Testing Update User {user_id}...")
    response = requests.put(
        f"{BASE_URL}/user/{user_id}",
        json={
            "username": "updated_user",
            "password": "updated_password",
            "visibility": "private",
        },
    )
    print_response(response)


def test_delete_user(user_id):
    print(f"Testing Delete User {user_id}...")
    response = requests.delete(f"{BASE_URL}/user/{user_id}")
    print_response(response)


# ========== SONG TESTS ==========


def test_create_song():
    print("Testing Create Song...")
    response = requests.post(
        f"{BASE_URL}/song/",
        json={"name": "Test Song", "albumId": 1},
    )
    print_response(response)


def test_get_song(song_id):
    print(f"Testing Get Song {song_id}...")
    response = requests.get(f"{BASE_URL}/song/{song_id}")
    print_response(response)


def test_update_song(song_id):
    print(f"Testing Update Song {song_id}...")
    response = requests.put(
        f"{BASE_URL}/song/{song_id}",
        json={"name": "Updated Song", "albumId": 2},
    )
    print_response(response)


def test_delete_song(song_id):
    print(f"Testing Delete Song {song_id}...")
    response = requests.delete(f"{BASE_URL}/song/{song_id}")
    print_response(response)


# ========== DIARY ENTRY TESTS ==========


def test_create_diary_entry():
    print("Testing Create Diary Entry...")
    response = requests.post(
        f"{BASE_URL}/entry/",
        json={
            "date": "2023-01-01",
            "description": "Diary entry description",
            "visibility": "public",
            "userId": 1,
            "songId": 1,
        },
    )
    print_response(response)


def test_get_diary_entry(entry_id):
    print(f"Testing Get Diary Entry {entry_id}...")
    response = requests.get(f"{BASE_URL}/entry/{entry_id}")
    print_response(response)


def test_update_diary_entry(entry_id):
    print(f"Testing Update Diary Entry {entry_id}...")
    response = requests.put(
        f"{BASE_URL}/entry/{entry_id}",
        json={
            "description": "Updated description",
            "visibility": "private",
            "songId": 2,
        },
    )
    print_response(response)


def test_delete_diary_entry(entry_id):
    print(f"Testing Delete Diary Entry {entry_id}...")
    response = requests.delete(f"{BASE_URL}/entry/{entry_id}")
    print_response(response)


# ========== ALBUM TESTS ==========


def test_create_album():
    print("Testing Create Album...")
    response = requests.post(
        f"{BASE_URL}/album/", json={"name": "Test Album", "artistId": 1}
    )
    print_response(response)


def test_get_album(album_id):
    print(f"Testing Get Album {album_id}...")
    response = requests.get(f"{BASE_URL}/album/{album_id}")
    print_response(response)


def test_update_album(album_id):
    print(f"Testing Update Album {album_id}...")
    response = requests.put(
        f"{BASE_URL}/album/{album_id}", json={"name": "Updated Album", "artistId": 2}
    )
    print_response(response)


def test_delete_album(album_id):
    print(f"Testing Delete Album {album_id}...")
    response = requests.delete(f"{BASE_URL}/album/{album_id}")
    print_response(response)


# ========== AGGREGATE REPORT TESTS ==========


def test_total_users_reports():
    print("Testing Total Users Report...")
    response = requests.get(f"{BASE_URL}/report/total_users")
    print_response(response)


def test_avg_visibility_entries_report():
    print("Testing Average Visibility Entries Report...")
    response = requests.get(f"{BASE_URL}/report/avg_visibility_entries")
    print_response(response)


def run_all_tests():
    test_create_user()
    test_get_user(1)
    test_update_user(1)
    # test_delete_user(1)

    test_create_song()
    test_get_song(1)
    test_update_song(1)
    # test_delete_song(1)

    test_create_diary_entry()
    test_get_diary_entry(1)
    test_update_diary_entry(1)
    # test_delete_diary_entry(1)

    test_create_album()
    test_get_album(1)
    test_update_album(1)
    # test_delete_album(1)

    test_total_users_reports()
    test_avg_visibility_entries_report()


if __name__ == "__main__":
    run_all_tests()
