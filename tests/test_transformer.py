import pandas as pd

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from etl.transformer import transform_chunk

def test_transform_chunk():
    data = {
        "transaction_id": [1, 2, 3, 4],
        "user_id": [101, 102, 103, 104],
        "amount": [100.0, -50.0, 200.0, 300.0],
        "timestamp": ["2024-01-01 10:00:00"] * 4,
        "status": ["SUCCESS", "FAILED", "cancelled", "Pending"]
    }
    df = pd.DataFrame(data)
    transformed_df = transform_chunk(df)

    assert transformed_df.shape[0] == 2
    assert all(transformed_df["amount"] >= 0)
    assert all(transformed_df["status"] != "cancelled")

    assert all(transformed_df["status"].str.islower())

    assert "processed_at" in transformed_df.columns