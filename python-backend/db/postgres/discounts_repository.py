from db.postgres.db import get_connection
from db.postgres.queries.discounts import DiscountsQuery
from psycopg2.extras import RealDictCursor

class DiscountsRepository:
    @staticmethod
    def list_valid_promotions_for_order(order_number: str):
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query, params = DiscountsQuery.list_valid_promotions_for_order(order_number)
        cursor.execute(query, params)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()
        return rows

    @staticmethod
    def list_all_discounts():
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query, params = DiscountsQuery.list_all_codes()
        cursor.execute(query, params)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()
        return rows
