CREATE TABLE IF NOT EXISTS customers (
    user_id TEXT PRIMARY KEY,
    name TEXT,
    email TEXT,
    phone TEXT,
    address_street TEXT,
    address_city TEXT,
    address_state TEXT,
    address_zip_code TEXT
);

CREATE TABLE IF NOT EXISTS products (
    id TEXT PRIMARY KEY,
    name TEXT,
    description TEXT,
    price REAL,
    category TEXT,
    stock INTEGER
);

CREATE TABLE IF NOT EXISTS orders (
    order_number TEXT PRIMARY KEY,
    customer_email TEXT,
    user_id TEXT,
    total_amount REAL,
    status TEXT,
    tracking_code TEXT,
    payment_id TEXT,
    discount_code TEXT,
    created_at TEXT,
    FOREIGN KEY (user_id) REFERENCES customers (user_id)
);

CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_number TEXT,
    product_id TEXT,
    quantity INTEGER,
    price REAL,
    FOREIGN KEY (order_number) REFERENCES orders (order_number),
    FOREIGN KEY (product_id) REFERENCES products (id)
);

CREATE TABLE IF NOT EXISTS discounts (
    discount_code TEXT PRIMARY KEY,
    description TEXT,
    type TEXT,
    value REAL,
    is_active BOOLEAN,
    expiration_date TEXT,
    min_purchase_value REAL,
    applicable_category TEXT
);

CREATE TABLE IF NOT EXISTS payments (
    payment_id TEXT PRIMARY KEY,
    order_number TEXT,
    amount REAL,
    method TEXT,
    status TEXT,
    transaction_date TEXT,
    FOREIGN KEY (order_number) REFERENCES orders (order_number)
);

CREATE TABLE IF NOT EXISTS returns (
    return_id TEXT PRIMARY KEY,
    order_number TEXT,
    product_id TEXT,
    return_reason TEXT,
    status TEXT,
    requested_at TEXT,
    FOREIGN KEY (order_number) REFERENCES orders (order_number),
    FOREIGN KEY (product_id) REFERENCES products (id)
);
