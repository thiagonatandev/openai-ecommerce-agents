from db.postgres.db import get_connection
from db.postgres.queries.payments import PaymentsQuery
from psycopg2.extras import RealDictCursor

class PaymentsRepository:
    @staticmethod
    def get_payment_by_id(payment_id: str):
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query, params = PaymentsQuery.get_payment_by_id(payment_id)
        cursor.execute(query, params)

        row = cursor.fetchone()
        cursor.close()
        conn.close()

        return row
