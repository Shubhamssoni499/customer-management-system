import mysql.connector
from config.db_config import get_connection


class CustomerService:

    def __init__(self):
        self.connection = None

    # --------------------------
    # Private DB connection
    # --------------------------
    def _connect(self):
        if self.connection is None or not self.connection.is_connected():
            self.connection = get_connection()
        return self.connection

    # --------------------------
    # Add New Customer
    # --------------------------
    def add_customer(self, name, email, phone, address):
        conn = self._connect()
        cursor = conn.cursor()

        query = """
            INSERT INTO customers (name, email, phone, address)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(query, (name, email, phone, address))
        conn.commit()
        cursor.close()

        return True

    # --------------------------
    # Fetch All Customers
    # --------------------------
    def get_all_customers(self):
        conn = self._connect()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM customers ORDER BY id DESC"

        cursor.execute(query)
        customers = cursor.fetchall()
        cursor.close()

        return customers

    # --------------------------
    # Get Single Customer by ID
    # --------------------------
    def get_customer(self, customer_id):
        conn = self._connect()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM customers WHERE id = %s"
        cursor.execute(query, (customer_id,))
        customer = cursor.fetchone()

        cursor.close()

        return customer

    # --------------------------
    # Update Customer
    # --------------------------
    def update_customer(self, customer_id, name, email, phone, address):
        conn = self._connect()
        cursor = conn.cursor()

        query = """
            UPDATE customers
            SET name=%s, email=%s, phone=%s, address=%s
            WHERE id=%s
        """

        cursor.execute(query, (name, email, phone, address, customer_id))
        conn.commit()

        cursor.close()

        return True

    # --------------------------
    # Delete Customer
    # --------------------------
    def delete_customer(self, customer_id):
        conn = self._connect()
        cursor = conn.cursor()

        query = "DELETE FROM customers WHERE id = %s"
        cursor.execute(query, (customer_id,))
        conn.commit()

        cursor.close()

        return True