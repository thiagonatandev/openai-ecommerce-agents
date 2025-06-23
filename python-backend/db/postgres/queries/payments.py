
class PaymentsQuery:
    @staticmethod
    def get_payment_by_id(payment_id: str):
        query = '''
            SELECT 
                amount, method, status, transaction_date
            FROM payments
            WHERE payment_id = %s;
        '''
        return query, (payment_id,)
