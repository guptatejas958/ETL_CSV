
import pandas as pd
from typing import Generator


def read_csv_in_chunks(file_path: str, chunksize: int) -> Generator[pd.DataFrame, None, None]:
    try:
        for chunk in pd.read_csv(file_path, chunksize=chunksize):
            yield chunk
    except pd.errors.ParserError as e:
        print(f"Parser error while reading CSV: {e}")
        raise
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise
