# Author Tejas Gupta
# Entry point for ETL pipe

import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

from etl.file_reader import read_csv_in_chunks
from etl.transformer import transform_chunk
from etl.db_writer import create_connection, create_table_if_not_exists, insert_dataframe
from etl.utils import setup_logger
import config
# # Constants
# DB_PATH = "etl_data.db"
# TABLE_NAME = "transactions"
# CSV_PATH = "sample.csv"  # Update this if needed
# CHUNK_SIZE = 3
# TEMP_DIR = "temp_chunks"
# FINAL_CSV = "final_processed.csv"
# MAX_WORKERS = 4  # Adjust based on CPU

# Initialize logger
logger = setup_logger()


def ensure_temp_dir():
    if not os.path.exists(config.TEMP_DIR):
        os.makedirs(config.TEMP_DIR)


def process_and_save_chunk(chunk, index):
    try:
        cleaned = transform_chunk(chunk)
        temp_path = os.path.join(config.TEMP_DIR, f"chunk_{index}.csv")
        cleaned.to_csv(temp_path, index=False)
        logger.info(f"Processed and saved chunk {index}")
        return temp_path
    except Exception as e:
        logger.error(f"Error processing chunk {index}: {e}")
        return None


def parallel_process_chunks():
    chunk_paths = []
    futures = []

    with ThreadPoolExecutor(max_workers=config.MAX_WORKERS) as executor:
        for i, chunk in enumerate(read_csv_in_chunks(config.CSV_PATH, config.CHUNK_SIZE)):
            futures.append(executor.submit(process_and_save_chunk, chunk, i))

        for future in as_completed(futures):
            result = future.result()
            if result:
                chunk_paths.append(result)

    return chunk_paths


def merge_all_chunks(chunk_paths):
    try:
        dataframes = [pd.read_csv(path) for path in chunk_paths]
        merged_df = pd.concat(dataframes, ignore_index=True)
        merged_df.to_csv(config.FINAL_CSV, index=False)
        logger.info(f"Merged final CSV written to {config.FINAL_CSV}")
        return merged_df
    except Exception as e:
        logger.error(f"Error merging chunks: {e}")
        return pd.DataFrame()


def load_into_db(df):
    conn = create_connection(config.DB_PATH)
    if conn:
        try:
            create_table_if_not_exists(conn, config.TABLE_NAME)
            insert_dataframe(conn, df, config.TABLE_NAME)
            logger.info(f"Inserted {len(df)} rows into database.")
        except Exception as e:
            logger.error(f"DB Insertion Error: {e}")
        finally:
            conn.close()


def run_pipeline():
    logger.info("Starting ETL pipeline")
    ensure_temp_dir()
    
    chunk_files = parallel_process_chunks()

    if not chunk_files:
        logger.warning("No chunks were processed successfully.")
        return

    merged_df = merge_all_chunks(chunk_files)

    if not merged_df.empty:
        load_into_db(merged_df)

    logger.info("ETL pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()
