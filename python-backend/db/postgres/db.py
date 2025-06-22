import psycopg2
from utils.get_env import load_config
import csv
from pathlib import Path

config = load_config()

def get_connection():
    return psycopg2.connect(
        database = config["POSTGRES_DB"],
        user = config["POSTGRES_USER"],
        host = config["POSTGRES_HOST"],
        password = config["POSTGRES_PASSWORD"],
        port = config["POSTGRES_PORT"],
    )

def run_migrations():
    conn = get_connection()
    create_base_tables(conn=conn)
    populate_tables(conn=conn)

def create_base_tables(conn, path=None):
    cursor = conn.cursor()
    try:
        if path is None:
            base_dir = Path(__file__).resolve().parent.parent.parent.parent
            path = base_dir / ".config" / "schema.sql"

        with open(path, "r") as f:
            cursor.execute(f.read())
        conn.commit()
        print("✅ Tables created from SQL script.")
    except Exception as e:
        conn.rollback()
        print("❌ Error creating tables:", e)
    finally:
        cursor.close()
        conn.close()

def populate_tables(conn, data_dir=None):
    conn = get_connection()
    cursor = conn.cursor()

    if data_dir is None:
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        data_dir = base_dir / ".config" / "fixtures"

    csv_files = {
        "customers": "customers.csv",
        "products": "products.csv",
        "orders": "orders.csv",
        "order_items": "order_items.csv",
        "discounts": "discounts.csv",
        "payments": "payments.csv",
        "returns": "returns.csv"
    }

    def table_is_empty(table):
        cursor.execute(f"SELECT EXISTS (SELECT 1 FROM {table} LIMIT 1)")
        return not cursor.fetchone()[0]

    try:
        for table, file in csv_files.items():
            if not table_is_empty(table):
                print(f"⚠️  Table '{table}' already has data. Skipping...")
                continue

            path = f"{data_dir}/{file}"
            with open(path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader)
                placeholders = ','.join(['%s'] * len(headers))
                query = f"INSERT INTO {table} ({','.join(headers)}) VALUES ({placeholders})"
                for row in reader:
                    cursor.execute(query, row)

            print(f"✅ Data inserted into '{table}'.")

        conn.commit()

    except Exception as e:
        conn.rollback()
        print("❌ Error populating tables:", e)
    finally:
        cursor.close()
        conn.close()
