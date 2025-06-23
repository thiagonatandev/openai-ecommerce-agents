
class OrdersQuery:
    @staticmethod
    def get_order_by_code(user_id: str, order_number: str):
        query = '''
            SELECT
                order_number,
                total_amount,
                status,
                tracking_code,
                payment_id,
                discount_code,
                created_at
            FROM
                orders
            WHERE
                user_id = %s AND order_number = %s;
        '''
        return query, (user_id, order_number)
    
    @staticmethod
    def list_used_discount_codes(user_id: str):
        query = '''
            SELECT
                discount_code
            FROM 
                orders
            WHERE
                user_id = %s;
        '''
        return query, (user_id,)

    @staticmethod
    def apply_discount_code(discount_code: str, order_number: str):
        query = "UPDATE orders SET discount_code = %s WHERE order_number = %s"
        return query, (discount_code, order_number)