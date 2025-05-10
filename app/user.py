import hashlib
from app.db import create_connection

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

class UserManager:
    def __init__(self):
        self.conn = create_connection()

    def register_user(self, username: str, password: str, is_admin: bool = False) -> bool:
        cursor = self.conn.cursor()
        try:
            password_hash = hash_password(password)
            cursor.execute("INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, ?)",
                           (username, password_hash, int(is_admin)))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error registering user: {e}")
            return False

    def validate_login(self, username: str, password: str) -> bool:
        cursor = self.conn.cursor()
        password_hash = hash_password(password)
        cursor.execute("SELECT * FROM users WHERE username = ? AND password_hash = ?", (username, password_hash))
        user = cursor.fetchone()
        return user is not None

    def is_admin(self, username: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("SELECT is_admin FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        if result:
            return bool(result[0])
        return False
