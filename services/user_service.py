import mysql.connector
from config.db_config import get_connection


class UserService:

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
    # Add New User
    # --------------------------
    def add_user(self, username, password, role="user"):
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

    # --------------------------
    # Get All Users
    # --------------------------
    def get_all_users(self):
        conn = self._connect()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT id, username, role FROM users ORDER BY id DESC"

        cursor.execute(query)
        users = cursor.fetchall()

        cursor.close()
        return users

    # --------------------------
    # Get Single User
    # --------------------------
    def get_user(self, user_id):
        conn = self._connect()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT id, username, role FROM users WHERE id = %s"

        cursor.execute(query, (user_id,))
        user = cursor.fetchone()

        cursor.close()
        return user

    # --------------------------
    # Update User Info
    # --------------------------
    def update_user(self, user_id, username, role):
        conn = self._connect()
        cursor = conn.cursor()

        query = """
            UPDATE users
            SET username = %s, role = %s
            WHERE id = %s
        """

        cursor.execute(query, (username, role, user_id))
        conn.commit()

        cursor.close()
        return True

    # --------------------------
    # Update Only Password
    # --------------------------
    def update_password(self, user_id, new_password):
        conn = self._connect()
        cursor = conn.cursor()

        query = "UPDATE users SET password = %s WHERE id = %s"

        cursor.execute(query, (new_password, user_id))
        conn.commit()

        cursor.close()
        return True

    # --------------------------
    # Delete User
    # --------------------------
    def delete_user(self, user_id):
        conn = self._connect()
        cursor = conn.cursor()

        query = "DELETE FROM users WHERE id = %s"

        cursor.execute(query, (user_id,))
        conn.commit()

        cursor.close()
        return True