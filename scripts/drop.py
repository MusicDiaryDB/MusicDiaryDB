import psycopg2


def drop_all_tables(conn):
    tables = [
        "ReportEntries",
        "UserFriends",
        "UserDiaryEntries",
        "UserDiaryReports",
        "UserReviews",
        "DiaryEntrySongs",
        "StreamingPlatformSongs",
        "AlbumSongs",
        "ArtistAlbums",
        "DiaryEntry",
        "DiaryReport",
        "Review",
        "Song",
        "StreamingPlatform",
        "Album",
        "Artist",
        "User",
    ]

    try:
        # Open a cursor to perform database operations
        cur = conn.cursor()

        # Drop each table in the right order
        for table in tables:
            drop_statement = f'DROP TABLE IF EXISTS "{table}" CASCADE;'
            cur.execute(drop_statement)
            print(f"Dropped table: {table}")

        # Commit the changes to the database
        conn.commit()
        print("All tables dropped successfully!")

    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()

    finally:
        cur.close()


conn_params = {
    "dbname": "music_diary_db",
    "user": "admin",
    "password": "admin",
    "host": "localhost",
    "port": "5432",
}

try:
    conn = psycopg2.connect(**conn_params)
    drop_all_tables(conn)
except Exception as e:
    print(f"Failed to connect to the database: {e}")
finally:
    if conn:
        conn.close()
