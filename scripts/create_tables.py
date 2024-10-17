import psycopg2

db_config = {
    "dbname": "music_diary_db",
    "user": "admin",
    "password": "admin",
    "host": "127.0.0.1",
    "port": "5432",
}


def create_connection():
    try:
        conn = psycopg2.connect(**db_config)
        print("Database connection successful")
        return conn
    except Exception as e:
        print(f"Error: {e}")
        return None


def create_tables(conn):
    create_users_table: str
    with open("data/tables.sql") as f:
        create_users_table = str(f.read())
        # print(create_users_table)

    try:
        with conn.cursor() as cur:
            cur.execute(create_users_table)
            conn.commit()
            print("Tables created successfully")
    except Exception as e:
        print(f"Error creating tables: {e}")
        conn.rollback()


def insert_data(conn):
    insert_data: str
    with open("data/fake-data.sql") as f:
        insert_data = str(f.read())
        # print(insert_data)

    try:
        with conn.cursor() as cur:
            cur.execute(insert_data)
            conn.commit()
            print("Inserted data successfully")
    except Exception as e:
        print(f"Error inserting data: {e}")
        conn.rollback()


if __name__ == "__main__":
    conn = create_connection()

    if conn:
        create_tables(conn)
        # insert_data(conn)
        conn.close()
        print("Connection closed")
