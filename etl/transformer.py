#Transformation logic as per requirement

import pandas as pd
from datetime import datetime, timezone


def transform_chunk(df: pd.DataFrame) -> pd.DataFrame:
    try:
        df['status'] = df['status'].astype(str).str.lower()
        df = df[(df['amount'] >= 0) & (df['status'] != 'cancelled')]
        processed_time = datetime.now(timezone.utc).isoformat()
        df['processed_at'] = processed_time
        
        return df

    except Exception as e:
        raise ValueError(f"Error transforming chunk: {e}")
