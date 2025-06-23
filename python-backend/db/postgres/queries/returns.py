class ReturnsQuery:
    @staticmethod
    def get_order_status_and_date(order_number: str):
        return '''
            SELECT status, created_at
            FROM orders
            WHERE order_number = %s
        ''', (order_number,)

    @staticmethod
    def insert_return(return_id: str, order_number: str, product_id: str, return_reason: str, status: str, requested_at: str):
        return '''
            INSERT INTO returns (return_id, order_number, product_id, return_reason, status, requested_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (return_id, order_number, product_id, return_reason, status, requested_at)