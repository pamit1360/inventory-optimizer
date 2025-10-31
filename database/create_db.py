# database/create_db.py
import sqlite3
from data.synthetic_data import generate_data

DB_PATH = "database/inventory.db"


def create_tables(conn):
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        unit_cost REAL,
        holding_cost REAL,
        lead_time_days INTEGER
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS warehouses (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        capacity INTEGER
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        warehouse_id INTEGER,
        current_stock INTEGER,
        reorder_point INTEGER,
        FOREIGN KEY (product_id) REFERENCES products(id),
        FOREIGN KEY (warehouse_id) REFERENCES warehouses(id)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS demand (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        product_id INTEGER,
        quantity INTEGER,
        FOREIGN KEY (product_id) REFERENCES products(id)
    );
    """)

    conn.commit()


def populate_tables(conn):
    products, warehouses, inventory, demand = generate_data()

    cur = conn.cursor()

    cur.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?);", products)
    cur.executemany("INSERT INTO warehouses VALUES (?, ?, ?);", warehouses)
    cur.executemany(
        "INSERT INTO inventory (product_id, warehouse_id, current_stock, reorder_point) VALUES (?, ?, ?, ?);",
        inventory,
    )
    cur.executemany(
        "INSERT INTO demand (date, product_id, quantity) VALUES (?, ?, ?);", demand
    )

    conn.commit()


def main():
    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)
    populate_tables(conn)
    print("✅ Database created and populated successfully!")
    conn.close()


if __name__ == "__main__":
    main()
