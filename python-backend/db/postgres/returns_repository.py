import datetime
from db.postgres.db import get_connection
from psycopg2.extras import RealDictCursor
from db.postgres.queries.returns import ReturnsQuery

class ReturnsRepository:
    @staticmethod
    def get_order_status_and_date(order_number: str):
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        query, params = ReturnsQuery.get_order_status_and_date(order_number)
        cursor.execute(query, params)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def create_return(return_id: str, order_number: str, product_id: str, return_reason: str):
        conn = get_connection()
        cursor = conn.cursor()
        query, params = ReturnsQuery.insert_return(
            return_id, order_number, product_id, return_reason, "Pending", datetime.datetime.now().isoformat()
        )
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()