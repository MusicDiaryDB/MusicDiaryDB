import psycopg2

# Function to drop all tables in the correct order considering foreign key dependencies


def drop_all_tables(conn):
    # List all the tables in the order they should be dropped (considering dependencies)
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
        "User"
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
        conn.rollback()  # Rollback if there was an error

    finally:
        cur.close()  # Close the cursor


# Sample usage
if __name__ == "__main__":
    # Define connection parameters (adjust to your own settings)
    conn_params = {
        'dbname': 'music_diary_db',
        'user': 'admin',
        'password': 'admin',
        'host': 'localhost',
        'port': '5432'
    }

    # Establish connection to the PostgreSQL database
    try:
        conn = psycopg2.connect(**conn_params)
        drop_all_tables(conn)
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
    finally:
        if conn:
            conn.close()  # Close the connection when done
