import sqlite3
import pandas as pd
# from etl.db_writer import create_connection, create_table_if_not_exists, insert_dataframe
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from etl.db_writer import create_connection, create_table_if_not_exists, insert_dataframe

def test_db_insertion(tmp_path):
    db_path = tmp_path / "test.db"
    table_name = "transactions_test"
    data = {
        "transaction_id": [1, 2],
        "user_id": [101, 102],
        "amount": [99.99, 150.00],
        "timestamp": ["2024-01-01 10:00:00", "2024-01-02 11:00:00"],
        "status": ["success", "failed"],
        "processed_at": ["2025-01-01T12:00:00Z", "2025-01-01T12:00:00Z"]
    }
    df = pd.DataFrame(data)


    conn = create_connection(str(db_path))
    create_table_if_not_exists(conn, table_name)
    insert_dataframe(conn, df, table_name)

    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cur.fetchone()[0]
    assert count == 2

    conn.close()