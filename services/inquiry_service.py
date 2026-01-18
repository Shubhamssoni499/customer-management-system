import mysql.connector
from config.db_config import get_connection


class InquiryService:

    def __init__(self):
        self.connection = None

    # --------------------------------
    # PRIVATE DB CONNECTION
    # --------------------------------
    def _connect(self):
        if self.connection is None or not self.connection.is_connected():
            self.connection = get_connection()
        return self.connection

    # --------------------------------
    # ADD NEW INQUIRY
    # --------------------------------
    def add_inquiry(self, customer_id, inquiry_text, status="Pending"):
        conn = self._connect()
        cursor = conn.cursor()

        query = """
            INSERT INTO inquiries (customer_id, inquiry_text, status)
            VALUES (%s, %s, %s)
        """

        cursor.execute(query, (customer_id, inquiry_text, status))
        conn.commit()
        cursor.close()

        return True

    # --------------------------------
    # GET ALL INQUIRIES WITH CUSTOMER NAME
    # --------------------------------
    def get_all_inquiries(self):
        conn = self._connect()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                inquiries.id,
                customers.name AS customer_name,
                inquiries.inquiry_text,
                inquiries.status,
                inquiries.created_at
            FROM inquiries
            LEFT JOIN customers ON inquiries.customer_id = customers.id
            ORDER BY inquiries.id DESC
        """

        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    # --------------------------------
    # GET SINGLE INQUIRY BY ID
    # --------------------------------
    def get_inquiry(self, inquiry_id):
        conn = self._connect()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM inquiries WHERE id = %s"
        cursor.execute(query, (inquiry_id,))
        result = cursor.fetchone()

        cursor.close()
        return result

    # --------------------------------
    # UPDATE INQUIRY STATUS
    # --------------------------------
    def update_inquiry(self, inquiry_id, new_status):
        conn = self._connect()
        cursor = conn.cursor()

        query = """
            UPDATE inquiries
            SET status = %s
            WHERE id = %s
        """

        cursor.execute(query, (new_status, inquiry_id))
        conn.commit()

        cursor.close()
        return True

    # --------------------------------
    # DELETE INQUIRY
    # --------------------------------
    def delete_inquiry(self, inquiry_id):
        conn = self._connect()
        cursor = conn.cursor()

        query = "DELETE FROM inquiries WHERE id = %s"
        cursor.execute(query, (inquiry_id,))
        conn.commit()

        cursor.close()
        return True