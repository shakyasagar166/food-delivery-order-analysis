"""
Pre-seed script for SQLite database (data/food_delivery.db)
"""
import os
import sqlite3
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
DB_PATH = os.path.join(BASE_DIR, "data", "food_delivery.db")

print(f"Connecting to database: {DB_PATH}")
conn = sqlite3.connect(DB_PATH)

csv_mapping = {
    "customers": "customers.csv",
    "restaurants": "restaurants.csv",
    "riders": "riders.csv",
    "orders": "orders.csv",
    "order_items": "order_items.csv",
    "deliveries": "deliveries.csv",
    "payments": "payments.csv"
}

for table_name, csv_file in csv_mapping.items():
    file_path = os.path.join(DATA_DIR, csv_file)
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"Loaded {len(df):,} rows into '{table_name}'")

cursor = conn.cursor()
cursor.execute("CREATE INDEX IF NOT EXISTS idx_ord_cust ON orders(customer_id);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_ord_rest ON orders(restaurant_id);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_ord_date ON orders(order_date);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_ord_status ON orders(order_status);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_delv_order ON deliveries(order_id);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_delv_sla ON deliveries(sla_status);")

conn.commit()
conn.close()
print("Database successfully initialized!")
