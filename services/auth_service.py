import mysql.connector
from config.db_config import get_connection


class AuthService:

    def __init__(self):
        self.connection = None

    # --------------------------
    # Private DB Connection
    # --------------------------
    def _connect(self):
        if self.connection is None or not self.connection.is_connected():
            self.connection = get_connection()
        return self.connection

    # --------------------------
    # Login Function
    # --------------------------
    def login(self, username, password):
        """
        Check user's username and password.
        Returns user dict if success, else None.
        """

        conn = self._connect()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT id, username, role 
            FROM users
            WHERE username = %s AND password = %s
        """

        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        cursor.close()

        return user

    # --------------------------
    # Register new user
    # --------------------------
    def register_user(self, username, password, role="user"):
        """
        Insert new user into 'users' table.
        """

        conn = self._connect()
        cursor = conn.cursor()

        query = """
            INSERT INTO users (username, password, role)
            VALUES (%s, %s, %s)
        """

        cursor.execute(query, (username, password, role))
        conn.commit()

        cursor.close()

        return True