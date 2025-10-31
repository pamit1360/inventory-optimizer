# utils/db_utils.py
import sqlite3
import pandas as pd

DB_PATH = "database/inventory.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def fetch_table(table_name: str):
    conn = get_connection()
    df = pd.read_sql_query(f"SELECT * FROM {table_name};", conn)
    conn.close()
    return df


def list_tables():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cur.fetchall()]
    conn.close()
    return tables
