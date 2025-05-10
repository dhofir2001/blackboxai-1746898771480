import sqlite3
from sqlite3 import Error

DB_NAME = "livestream_app.db"

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def create_tables():
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS stream_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            encrypted_key TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS streaming_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            video_path TEXT NOT NULL,
            start_time TEXT,
            end_time TEXT,
            status TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """)
        conn.commit()
        conn.close()

if __name__ == "__main__":
    create_tables()
