
class CustomerQuery:
    @staticmethod
    def get_customer_by_email(email: str):
        query = '''
            SELECT 
                user_id, name, email, phone, 
                address_street, address_city, address_state, address_zip_code
            FROM customers
            WHERE email = %s;
        '''
        return query, (email,)
