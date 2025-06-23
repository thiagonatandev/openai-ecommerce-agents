from db.postgres.db import get_connection
from db.postgres.queries.orders import OrdersQuery
from psycopg2.extras import RealDictCursor
from db.postgres.discounts_repository import DiscountsRepository
class OrdersRepository:
    @staticmethod
    def get_order_by_user_id_and_order_number(user_id: str, order_number: str):
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query, params = OrdersQuery.get_order_by_code(user_id, order_number)
        cursor.execute(query, params)

        row = cursor.fetchone()
        cursor.close()
        conn.close()

        return row
    
    @staticmethod
    def apply_discount(order_number: str, discount_code: str):
        conn = get_connection()
        cursor = conn.cursor()

        valid_promos = DiscountsRepository.list_valid_promotions_for_order(order_number)
        valid_codes = [promo["discount_code"] for promo in valid_promos]

        if discount_code not in valid_codes:
            cursor.close()
            conn.close()
            return False  

        query, params = OrdersQuery.apply_discount_code(discount_code, order_number)
        cursor.execute(query, params)
    
        conn.commit()
        cursor.close()
        conn.close()

        return True
