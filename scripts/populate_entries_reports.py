import requests
import random
from music_data import data

BASE_URL = "http://localhost:5400"

# ========================================================================
#   Code below was largely written with ChatGPT to save time
#   This is non-critical code that just adds sample data to the database
# ========================================================================

# Generate Diary Entries from the provided `data`
diary_entries = []
entry_counter = 1  # To create unique descriptions and dates
usernames = ["admin", "Bob", "Patrick", "Ben"]

for artist, albums in data.items():
    for album, songs in albums.items():
        for song in songs:
            diary_entries.append(
                {
                    "date": f"2023-11-{entry_counter:02d}",
                    "description": f"Entry {entry_counter}: Amazing song discovery.",
                    "visibility": random.choice(["PUBLIC", "PRIVATE", "FRIENDS"]),
                    "username": random.choice(usernames),
                    "song_name": song,
                }
            )
            entry_counter += 1

# Generate Diary Reports
diary_reports = []
report_counter = 1

for username in usernames:
    for day in range(1, 32, len(usernames)):
        diary_reports.append(
            {
                "date": f"2023-11-{day:02d}",
                "description": f"Report {report_counter}: Weekly roundup of songs.",
                "visibility": random.choice(["PUBLIC", "FRIENDS"]),
                "username": username,
            }
        )
        report_counter += 1


# Helper functions to get user and song IDs
def get_user_id(username):
    response = requests.get(f"{BASE_URL}/user/{username}")
    if response.status_code != 200:
        print(
            f"Failed to fetch user: {username} - Status: {response.status_code}, Response: {response.json()}"
        )
        return None
    user = response.json()
    return user.get("UserID")


def get_song_id(song_name):
    response = requests.get(f"{BASE_URL}/song/{song_name}")
    if response.status_code != 200:
        print(
            f"Failed to fetch song: {song_name} - Status: {response.status_code}, Response: {response.json()}"
        )
        return None
    song = response.json()
    return song.get("SongID")


# Create Diary Entries and Store IDs
entry_ids = {}
current_entry_id = 1  # Ensure unique IDs
for entry in diary_entries:
    user_id = get_user_id(entry["username"])
    song_id = get_song_id(entry["song_name"])

    if user_id is None or song_id is None:
        print(
            f"Skipping diary entry creation for {entry} due to missing user or song ID."
        )
        continue

    response = requests.post(
        f"{BASE_URL}/entry/",
        data={
            "date": entry["date"],
            "description": entry["description"],
            "visibility": entry["visibility"],
            "userId": user_id,
            "songId": song_id,
        },
    )
    if response.status_code == 201:
        entry_ids[entry["description"]] = current_entry_id
        print(f"Diary entry created: {entry['description']} - ID: {current_entry_id}")
        current_entry_id += 1
    else:
        print(
            f"Failed to create diary entry: {entry} - Status: {response.status_code}, Response: {response.json()}"
        )

# Create Diary Reports and Store IDs
report_ids = {}
current_report_id = 1  # Ensure unique IDs
for report in diary_reports:
    user_id = get_user_id(report["username"])

    if user_id is None:
        print(f"Skipping diary report creation for {report} due to missing user ID.")
        continue

    response = requests.post(
        f"{BASE_URL}/report/",
        data={
            "date": report["date"],
            "description": report["description"],
            "visibility": report["visibility"],
            "userId": user_id,
        },
    )
    if response.status_code == 201:
        report_ids[report["description"]] = current_report_id
        print(
            f"Diary report created: {report['description']} - ID: {current_report_id}"
        )
        current_report_id += 1
    else:
        print(
            f"Failed to create diary report: {report} - Status: {response.status_code}, Response: {response.json()}"
        )

# Populate `report_entries` with numeric keys (ReportID and EntryID)
report_entries = []
for report in diary_reports:
    report_id = report_ids.get(report["description"])
    if report_id is None:
        print(f"Skipping report '{report['description']}' due to missing ReportID.")
        continue

    # Ensure at least one diary entry is associated with each report
    linked_entries = random.sample(
        list(entry_ids.items()), k=max(1, min(len(entry_ids), 5))
    )
    for description, entry_id in linked_entries:
        if entry_id is None:
            print(f"Skipping entry '{description}' due to missing EntryID.")
            continue

        report_entries.append(
            {
                "reportId": report_id,
                "entryId": entry_id,
            }
        )

# Debug: Check `report_entries`
print(f"Generated {len(report_entries)} report entries.")

# Validate and Link Report Entries
for report_entry in report_entries:
    report_id = report_entry["reportId"]
    entry_id = report_entry["entryId"]

    print(f"Linking ReportID={report_id} with EntryID={entry_id}")

    # Make POST request
    response = requests.post(
        f"{BASE_URL}/report_entry/",
        data={"reportId": report_id, "entryId": entry_id},
    )
    if response.status_code == 201:
        print(f"Successfully linked ReportID {report_id} with EntryID {entry_id}")
    else:
        print(
            f"Failed to link ReportID {report_id} with EntryID {entry_id} - "
            f"Status: {response.status_code}, Response: {response.json()}"
        )
