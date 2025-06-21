import sqlite3
import json
import os

# Define o caminho do banco de dados na mesma pasta do script
DB_PATH = os.path.join(os.path.dirname(__file__), 'ecom_database.db')
# Caminho para a pasta dos JSONs (agora apenas para a criação inicial)
JSON_DIR = os.path.dirname(__file__)

def create_initial_json_files():
    """Cria os arquivos JSON temporariamente para popular o banco de dados."""
    
    products_data = [
      {
        "id": "prod_123",
        "name": "Tênis de Corrida UltraBoost",
        "description": "Tênis de alta performance para corredores, com tecnologia de amortecimento Boost.",
        "price": 899.90,
        "category": "Calçados",
        "stock": 150
      },
      {
        "id": "prod_456",
        "name": "Camiseta Dry-Fit",
        "description": "Camiseta leve e respirável, ideal para atividades físicas.",
        "price": 129.90,
        "category": "Vestuário",
        "stock": 300
      },
      {
        "id": "prod_789",
        "name": "Garrafa Térmica Inox",
        "description": "Garrafa de 750ml que mantém a temperatura de líquidos por até 12 horas.",
        "price": 89.90,
        "category": "Acessórios",
        "stock": 500
      }
    ]
    with open(os.path.join(JSON_DIR, 'products.json'), 'w') as f:
        json.dump(products_data, f, indent=2)

    customers_data = [
      {
        "user_id": "user_d5a89af6-eb7b-4160-87bc-6cf4c63742de",
        "name": "João da Silva",
        "email": "cliente1@email.com",
        "phone": "+5511912345678",
        "address": {
          "street": "Rua das Flores, 123",
          "city": "São Paulo",
          "state": "SP",
          "zip_code": "01234-567"
        }
      },
      {
        "user_id": "user_c4b78de5-fa6c-4251-98ef-5df3b54671ab",
        "name": "Maria Oliveira",
        "email": "cliente2@email.com",
        "phone": "+5521987654321",
        "address": {
          "street": "Avenida Copacabana, 456",
          "city": "Rio de Janeiro",
          "state": "RJ",
          "zip_code": "21234-567"
        }
      }
    ]
    with open(os.path.join(JSON_DIR, 'customers.json'), 'w') as f:
        json.dump(customers_data, f, indent=2)

    orders_data = [
      {
        "order_number": "ORD-2025-001",
        "customer_email": "cliente1@email.com",
        "user_id": "user_d5a89af6-eb7b-4160-87bc-6cf4c63742de",
        "items": [
          {"product_id": "prod_123", "quantity": 1, "price": 899.90},
          {"product_id": "prod_456", "quantity": 2, "price": 129.90}
        ],
        "total_amount": 1159.70, "status": "Enviado", "tracking_code": "BR123456789PT",
        "payment_id": "pay_abc123", "discount_code": "PROMO10", "created_at": "2025-07-22T10:00:00Z"
      },
      {
        "order_number": "ORD-2025-002",
        "customer_email": "cliente2@email.com",
        "user_id": "user_c4b78de5-fa6c-4251-98ef-5df3b54671ab",
        "items": [{"product_id": "prod_789", "quantity": 1, "price": 89.90}],
        "total_amount": 89.90, "status": "Processando", "tracking_code": None,
        "payment_id": "pay_def456", "discount_code": None, "created_at": "2025-07-23T14:30:00Z"
      }
    ]
    with open(os.path.join(JSON_DIR, 'orders.json'), 'w') as f:
        json.dump(orders_data, f, indent=2)

    discounts_data = [
        {"discount_code": "PROMO10", "description": "10% de desconto em qualquer compra.", "type": "percentage", "value": 10, "is_active": True, "expiration_date": "2026-12-31"},
        {"discount_code": "FRETEGRATIS", "description": "Frete grátis para compras acima de R$200.", "type": "shipping", "value": "free", "min_purchase_value": 200, "is_active": True, "expiration_date": "2026-12-31"},
        {"discount_code": "INVERNO20", "description": "R$20 de desconto em produtos da categoria 'Vestuário'.", "type": "fixed", "value": 20, "applicable_category": "Vestuário", "is_active": True, "expiration_date": "2026-12-31"}
    ]
    with open(os.path.join(JSON_DIR, 'discounts.json'), 'w') as f:
        json.dump(discounts_data, f, indent=2)
    
    payments_data = [
      {"payment_id": "pay_abc123", "order_number": "ORD-2025-001", "amount": 1159.70, "method": "credit_card", "status": "approved", "transaction_date": "2025-07-22T09:59:50Z"},
      {"payment_id": "pay_def456", "order_number": "ORD-2025-002", "amount": 89.90, "method": "pix", "status": "pending", "transaction_date": "2025-07-23T14:29:45Z"}
    ]
    with open(os.path.join(JSON_DIR, 'payments.json'), 'w') as f:
        json.dump(payments_data, f, indent=2)

    returns_data = [
      {"return_id": "ret_xyz789", "order_number": "ORD-2025-001", "product_id": "prod_123", "return_reason": "Tamanho incorreto", "status": "Aguardando envio do cliente", "requested_at": "2025-07-25T11:00:00Z"}
    ]
    with open(os.path.join(JSON_DIR, 'returns.json'), 'w') as f:
        json.dump(returns_data, f, indent=2)

def create_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('CREATE TABLE customers (user_id TEXT PRIMARY KEY, name TEXT, email TEXT, phone TEXT, address_street TEXT, address_city TEXT, address_state TEXT, address_zip_code TEXT)')
    cursor.execute('CREATE TABLE products (id TEXT PRIMARY KEY, name TEXT, description TEXT, price REAL, category TEXT, stock INTEGER)')
    cursor.execute('CREATE TABLE orders (order_number TEXT PRIMARY KEY, customer_email TEXT, user_id TEXT, total_amount REAL, status TEXT, tracking_code TEXT, payment_id TEXT, discount_code TEXT, created_at TEXT, FOREIGN KEY (user_id) REFERENCES customers (user_id))')
    cursor.execute('CREATE TABLE order_items (id INTEGER PRIMARY KEY AUTOINCREMENT, order_number TEXT, product_id TEXT, quantity INTEGER, price REAL, FOREIGN KEY (order_number) REFERENCES orders (order_number), FOREIGN KEY (product_id) REFERENCES products (id))')
    cursor.execute('CREATE TABLE discounts (discount_code TEXT PRIMARY KEY, description TEXT, type TEXT, value REAL, is_active BOOLEAN, expiration_date TEXT, min_purchase_value REAL, applicable_category TEXT)')
    cursor.execute('CREATE TABLE payments (payment_id TEXT PRIMARY KEY, order_number TEXT, amount REAL, method TEXT, status TEXT, transaction_date TEXT, FOREIGN KEY (order_number) REFERENCES orders (order_number))')
    cursor.execute('CREATE TABLE returns (return_id TEXT PRIMARY KEY, order_number TEXT, product_id TEXT, return_reason TEXT, status TEXT, requested_at TEXT, FOREIGN KEY (order_number) REFERENCES orders (order_number), FOREIGN KEY (product_id) REFERENCES products (id))')

    conn.commit()
    conn.close()
    print("Banco de dados e tabelas criados com sucesso.")

def populate_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(os.path.join(JSON_DIR, 'customers.json'), 'r') as f:
        customers = json.load(f)
        for c in customers:
            cursor.execute('INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (c['user_id'], c['name'], c['email'], c['phone'], c['address']['street'], c['address']['city'], c['address']['state'], c['address']['zip_code']))

    with open(os.path.join(JSON_DIR, 'products.json'), 'r') as f:
        products = json.load(f)
        for p in products:
            cursor.execute('INSERT INTO products VALUES (?, ?, ?, ?, ?, ?)', (p['id'], p['name'], p['description'], p['price'], p['category'], p['stock']))

    with open(os.path.join(JSON_DIR, 'orders.json'), 'r') as f:
        orders = json.load(f)
        for o in orders:
            cursor.execute('INSERT INTO orders (order_number, customer_email, user_id, total_amount, status, tracking_code, payment_id, discount_code, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (o['order_number'], o['customer_email'], o['user_id'], o['total_amount'], o['status'], o['tracking_code'], o['payment_id'], o['discount_code'], o['created_at']))
            for item in o['items']:
                 cursor.execute('INSERT INTO order_items (order_number, product_id, quantity, price) VALUES (?, ?, ?, ?)', (o['order_number'], item['product_id'], item['quantity'], item['price']))

    with open(os.path.join(JSON_DIR, 'discounts.json'), 'r') as f:
        discounts = json.load(f)
        for d in discounts:
            cursor.execute('INSERT INTO discounts VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (d.get('discount_code'), d.get('description'), d.get('type'), d.get('value'), d.get('is_active'), d.get('expiration_date'), d.get('min_purchase_value'), d.get('applicable_category')))

    with open(os.path.join(JSON_DIR, 'payments.json'), 'r') as f:
        payments = json.load(f)
        for p in payments:
            cursor.execute('INSERT INTO payments VALUES (?, ?, ?, ?, ?, ?)', (p['payment_id'], p['order_number'], p['amount'], p['method'], p['status'], p['transaction_date']))

    with open(os.path.join(JSON_DIR, 'returns.json'), 'r') as f:
        returns = json.load(f)
        for r in returns:
            cursor.execute('INSERT INTO returns VALUES (?, ?, ?, ?, ?, ?)', (r['return_id'], r['order_number'], r['product_id'], r['return_reason'], r['status'], r['requested_at']))

    conn.commit()
    conn.close()
    print("Tabelas populadas com sucesso.")

def cleanup_json_files():
    """Apaga os arquivos JSON temporários."""
    for file_name in ['products.json', 'customers.json', 'orders.json', 'discounts.json', 'payments.json', 'returns.json']:
        os.remove(os.path.join(JSON_DIR, file_name))
    print("Arquivos JSON temporários removidos.")

if __name__ == '__main__':
    create_initial_json_files()
    create_database()
    populate_tables()
    cleanup_json_files()
    print("\nSetup concluído! Banco de dados 'ecom_database.db' está pronto para uso.") 