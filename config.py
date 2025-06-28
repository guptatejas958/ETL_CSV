# This is configuration file to take parameters from user while running.
# Default parameters are set for the testing files and directories.
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="ETL Pipeline Configuration")

    parser.add_argument("--csv_path", type=str, default="sample.csv", help="Path to the input CSV file")
    parser.add_argument("--db_path", type=str, default="etl_data.db", help="SQLite database file path")
    parser.add_argument("--table_name", type=str, default="transactions", help="Target table name in SQLite DB")
    parser.add_argument("--chunk_size", type=int, default=3, help="Number of rows per CSV chunk")
    parser.add_argument("--temp_dir", type=str, default="temp_chunks", help="Directory for temporary chunk files")
    parser.add_argument("--final_csv", type=str, default="final_processed.csv", help="Final merged CSV path")
    parser.add_argument("--max_workers", type=int, default=4, help="Maximum number of threads for processing")

    return parser.parse_args()

args = parse_args()

CSV_PATH = args.csv_path
DB_PATH = args.db_path
TABLE_NAME = args.table_name
CHUNK_SIZE = args.chunk_size
TEMP_DIR = args.temp_dir
FINAL_CSV = args.final_csv
MAX_WORKERS = args.max_workers