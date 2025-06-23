from db.postgres.db import get_connection
from db.postgres.queries.customers import CustomerQuery
from psycopg2.extras import RealDictCursor

class CustomersRepository:
    @staticmethod
    def get_customer_by_email(email: str):
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query, params = CustomerQuery.get_customer_by_email(email)
        cursor.execute(query, params)

        row = cursor.fetchone()
        cursor.close()
        conn.close()

        return row
