# to write to DB
import sqlite3
import pandas as pd
import os
from typing import Optional


def create_connection(db_path: str) -> sqlite3.Connection:
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        raise ConnectionError(f"Failed to connect to database: {e}")


def create_table_if_not_exists(conn: sqlite3.Connection, table_name: str) -> None:
    query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        transaction_id TEXT,
        user_id TEXT,
        amount REAL,
        timestamp TEXT,
        status TEXT,
        processed_at TEXT
    );
    """
    try:
        conn.execute(query)
        conn.commit()
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to create table: {e}")


def insert_dataframe(
    conn: sqlite3.Connection,
    df: pd.DataFrame,
    table_name: str
) -> None:
    
    try:
        if df.empty:
            return  # skip empty chunks

        columns = ['transaction_id', 'user_id', 'amount', 'timestamp', 'status', 'processed_at']
        data = df[columns].values.tolist()

        placeholders = ','.join('?' for _ in columns)
        insert_query = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})"

        conn.executemany(insert_query, data)
        conn.commit()
    except Exception as e:
        raise RuntimeError(f"Failed to insert data: {e}")
