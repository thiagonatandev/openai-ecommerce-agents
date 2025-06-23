class DiscountsQuery:
    @staticmethod
    def list_valid_promotions_for_order(order_number: str):
        query = '''
            SELECT d.*
            FROM discounts d
            WHERE d.is_active = TRUE
            AND (d.expiration_date IS NULL OR d.expiration_date::DATE > CURRENT_DATE)
            AND d.min_purchase_value <= (
                SELECT total_amount FROM orders WHERE order_number = %s
            )
            AND (
                d.applicable_category IS NULL OR EXISTS (
                SELECT 1 FROM order_items oi
                JOIN products p ON oi.product_id = p.id
                WHERE oi.order_number = %s
                    AND p.category = d.applicable_category
                )
            )
            AND d.discount_code NOT IN (
                SELECT discount_code FROM orders
                WHERE user_id = (SELECT user_id FROM orders WHERE order_number = %s)
                AND discount_code IS NOT NULL
            )
            ;
        '''
        return query, (order_number, order_number, order_number)
