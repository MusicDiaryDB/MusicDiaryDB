import random
from faker import Faker
import pandas as pd

# Initialize Faker object
fake = Faker()

# Number of records to generate for each table
num_users = 30
num_entries = 30
num_reports = 30
num_reviews = 30
num_songs = 100
num_streaming_platforms = 5
num_albums = 30
num_artists = 30

# Helper function to generate random visibility


def random_visibility():
    return random.choice(['Public', 'Private', 'Friends'])

# Helper function to format dates for PostgreSQL (YYYY-MM-DD)


def format_date(date):
    return date.strftime('%Y-%m-%d')

# Generate synthetic data for the User table


def generate_users(num):
    users = []
    for i in range(1, num + 1):
        users.append((i, fake.user_name(), random_visibility()))
    return users

# Generate synthetic data for the Song table


def generate_songs(num):
    songs = []
    for i in range(1, num + 1):
        songs.append(
            (i, format_date(fake.date_this_decade()), fake.catch_phrase()))
    return songs

# Generate synthetic data for the DiaryEntry table


def generate_diary_entries(num, num_users):
    entries = []
    for i in range(1, num + 1):
        description = f'Listened to "{fake.catch_phrase()}" today. {
            fake.sentence()}'
        entries.append((i, format_date(fake.date_this_year()), description,
                       random_visibility(), random.randint(1, num_users)))
    return entries

# Generate synthetic data for the DiaryReport table


def generate_diary_reports(num, num_users):
    reports = []
    for i in range(1, num + 1):
        reports.append((i, format_date(fake.date_this_year()), random_visibility(
        ), fake.text(), random.randint(1, num_users)))
    return reports

# Generate synthetic data for the Review table


def generate_reviews(num, num_songs):
    reviews = []
    for i in range(1, num + 1):
        reviews.append((i, fake.text(), random_visibility(),
                       random.randint(1, num_songs)))
    return reviews

# Generate synthetic data for the StreamingPlatform table


def generate_streaming_platforms(num):
    platforms = []
    for i in range(1, num + 1):
        platforms.append((i, fake.company()))
    return platforms

# Generate synthetic data for the Album table


def generate_albums(num):
    albums = []
    for i in range(1, num + 1):
        albums.append((i, fake.catch_phrase()))
    return albums

# Generate synthetic data for the Artist table


def generate_artists(num):
    artists = []
    for i in range(1, num + 1):
        artists.append((i, fake.name()))
    return artists

# Generate synthetic data for the intermediary tables

# Linking albums to songs


def generate_album_songs(num_songs, num_albums):
    album_songs = []
    for song_id in range(1, num_songs + 1):
        album_id = random.randint(1, num_albums)
        album_songs.append((song_id, album_id))
    return album_songs

# Linking artists to albums


def generate_artist_albums(num_albums, num_artists):
    artist_albums = []
    for album_id in range(1, num_albums + 1):
        artist_id = random.randint(1, num_artists)
        artist_albums.append((artist_id, album_id))
    return artist_albums

# Linking diary entries to songs


def generate_diary_entry_songs(num_entries, num_songs):
    diary_entry_songs = []
    for entry_id in range(1, num_entries + 1):
        song_id = random.randint(1, num_songs)
        diary_entry_songs.append((entry_id, song_id))
    return diary_entry_songs

# Linking streaming platforms to songs


def generate_streaming_platform_songs(num_songs, num_streaming_platforms):
    platform_songs = []
    for song_id in range(1, num_songs + 1):
        platform_id = random.randint(1, num_streaming_platforms)
        platform_songs.append((platform_id, song_id))
    return platform_songs

# Linking diary entries to reports


def generate_report_entries(num_reports, num_entries):
    report_entries = []
    for report_id in range(1, num_reports + 1):
        entry_id = random.randint(1, num_entries)
        report_entries.append((report_id, entry_id))
    return report_entries

# Linking users to diary entries


def generate_user_diary_entries(num_users, num_entries):
    user_diary_entries = []
    for entry_id in range(1, num_entries + 1):
        user_id = random.randint(1, num_users)
        user_diary_entries.append((user_id, entry_id))
    return user_diary_entries


# Generate synthetic data for UserFriends
def generate_user_friends(num_users, max_friends_per_user=5):
    user_friends_data = []

    for user_id in range(1, num_users + 1):
        num_friends = random.randint(1, max_friends_per_user)
        # Ensure the user doesn't friend themselves and that friendship is mutual (bidirectional)
        friends = random.sample(
            [i for i in range(1, num_users + 1) if i != user_id], num_friends)
        for friend_id in friends:
            if (user_id, friend_id) not in user_friends_data and (friend_id, user_id) not in user_friends_data:
                user_friends_data.append((user_id, friend_id))

    return user_friends_data

# Generate synthetic data for UserReviews


def generate_user_reviews(num_users, num_reviews):
    user_reviews_data = []

    # Assign random users to existing reviews
    for review_id in range(1, num_reviews + 1):
        user_id = random.randint(1, num_users)
        user_reviews_data.append((user_id, review_id))

    return user_reviews_data


# Linking users to reports


def generate_user_diary_reports(num_users, num_reports):
    user_diary_reports = []
    for report_id in range(1, num_reports + 1):
        user_id = random.randint(1, num_users)
        user_diary_reports.append((user_id, report_id))
    return user_diary_reports

# Generate insert statements for each table


def create_insert_statement(table, data):
    columns = ', '.join([f'"{col}"' for col in data.columns])
    insert_statements = []
    for index, row in data.iterrows():
        values = ', '.join([f"'{str(val)}'" if isinstance(
            val, str) else str(val) for val in row])
        insert_statements.append(
            f'INSERT INTO "{table}" ({columns}) VALUES ({values});')
    return insert_statements


# Generate synthetic data and create SQL insert statements
users = generate_users(num_users)
songs = generate_songs(num_songs)
diary_entries = generate_diary_entries(num_entries, num_users)
diary_reports = generate_diary_reports(num_reports, num_users)
reviews = generate_reviews(num_reviews, num_songs)
streaming_platforms = generate_streaming_platforms(num_streaming_platforms)
albums = generate_albums(num_albums)
artists = generate_artists(num_artists)

# Intermediary table data
album_songs = generate_album_songs(num_songs, num_albums)
artist_albums = generate_artist_albums(num_albums, num_artists)
diary_entry_songs = generate_diary_entry_songs(num_entries, num_songs)
platform_songs = generate_streaming_platform_songs(
    num_songs, num_streaming_platforms)
report_entries = generate_report_entries(num_reports, num_entries)
user_diary_entries = generate_user_diary_entries(num_users, num_entries)
user_diary_reports = generate_user_diary_reports(num_users, num_reports)

# Convert lists to DataFrames
df_users = pd.DataFrame(users, columns=['UserID', 'Username', 'Visibility'])
df_songs = pd.DataFrame(songs, columns=['SongID', 'ReleaseDate', 'Name'])
df_diary_entries = pd.DataFrame(diary_entries, columns=[
                                'EntryID', 'Date', 'Description', 'Visibility', 'UserID'])
df_diary_reports = pd.DataFrame(diary_reports, columns=[
                                'ReportID', 'Date', 'Visibility', 'Description', 'UserID'])
df_reviews = pd.DataFrame(
    reviews, columns=['ReviewID', 'Contents', 'Visibility', 'SongID'])
df_streaming_platforms = pd.DataFrame(streaming_platforms, columns=[
                                      'StreamingPlatformID', 'Name'])
df_albums = pd.DataFrame(albums, columns=['AlbumID', 'Name'])
df_artists = pd.DataFrame(artists, columns=['ArtistID', 'Name'])

df_album_songs = pd.DataFrame(album_songs, columns=['SongID', 'AlbumID'])
df_artist_albums = pd.DataFrame(artist_albums, columns=['ArtistID', 'AlbumID'])
df_diary_entry_songs = pd.DataFrame(
    diary_entry_songs, columns=['EntryID', 'SongID'])
df_platform_songs = pd.DataFrame(platform_songs, columns=[
                                 'StreamingPlatformID', 'SongID'])
df_report_entries = pd.DataFrame(
    report_entries, columns=['ReportID', 'EntryID'])
df_user_diary_entries = pd.DataFrame(
    user_diary_entries, columns=['UserID', 'EntryID'])
df_user_diary_reports = pd.DataFrame(
    user_diary_reports, columns=['UserID', 'ReportID'])

# Create SQL insert statements
user_insert = create_insert_statement("User", df_users)
song_insert = create_insert_statement("Song", df_songs)
diary_entry_insert = create_insert_statement("DiaryEntry", df_diary_entries)
diary_report_insert = create_insert_statement("DiaryReport", df_diary_reports)
review_insert = create_insert_statement("Review", df_reviews)
streaming_platform_insert = create_insert_statement(
    "StreamingPlatform", df_streaming_platforms)
album_insert = create_insert_statement("Album", df_albums)
artist_insert = create_insert_statement("Artist", df_artists)

album_song_insert = create_insert_statement("AlbumSongs", df_album_songs)
artist_album_insert = create_insert_statement("ArtistAlbums", df_artist_albums)
diary_entry_song_insert = create_insert_statement(
    "DiaryEntrySongs", df_diary_entry_songs)
platform_song_insert = create_insert_statement(
    "StreamingPlatformSongs", df_platform_songs)
report_entry_insert = create_insert_statement(
    "ReportEntries", df_report_entries)
user_diary_entry_insert = create_insert_statement(
    "UserDiaryEntries", df_user_diary_entries)
user_diary_report_insert = create_insert_statement(
    "UserDiaryReports", df_user_diary_reports)

# Print SQL insert statements
print("\n".join(user_insert))
print("\n".join(song_insert))
print("\n".join(diary_entry_insert))
print("\n".join(diary_report_insert))
print("\n".join(review_insert))
print("\n".join(streaming_platform_insert))
print("\n".join(album_insert))
print("\n".join(artist_insert))
print("\n".join(album_song_insert))
print("\n".join(artist_album_insert))
print("\n".join(diary_entry_song_insert))
print("\n".join(platform_song_insert))
print("\n".join(report_entry_insert))
print("\n".join(user_diary_entry_insert))
print("\n".join(user_diary_report_insert))


user_friends_data = generate_user_friends(num_users)
user_reviews_data = generate_user_reviews(num_users, num_reviews)

# Convert to DataFrames
df_user_friends = pd.DataFrame(user_friends_data, columns=[
                               "UserID", "FriendUserID"])
df_user_reviews = pd.DataFrame(
    user_reviews_data, columns=["UserID", "ReviewID"])

# Create insert statements for UserFriends and UserReviews tables
user_friends_insert = create_insert_statement("UserFriends", df_user_friends)
user_reviews_insert = create_insert_statement("UserReviews", df_user_reviews)

# Print SQL insert statements for UserFriends and UserReviews
print("\n".join(user_friends_insert))
print("\n".join(user_reviews_insert))
