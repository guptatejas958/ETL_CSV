
# ETL_CSV: Chunked CSV ETL Pipeline with SQLite Storage

## Project Overview

`ETL_CSV` is a robust and modular ETL (Extract-Transform-Load) pipeline designed for processing **very large CSV files** (up to several GBs), transforming them in **parallel**, and storing the final cleaned data into a **SQLite database**.

This project is optimized to:
- Handle CSVs larger than system memory using **chunked processing**
- Transform and clean data
- Merge results
- Insert clean records into a local database
- Log errors and status
- Run in **parallel using ThreadPoolExecutor**
- Be testable and CLI-configurable

## Features

- Efficient chunked reading to avoid memory overload  
- Data cleaning: remove negatives, standardize case, timestamp enrichment  
- Temp file output for each chunk (stored in `/temp_chunks`)  
- Final output merge into a single `.csv` file  
- Batch inserts into SQLite  
- Detailed logging of errors  
- CLI interface for configuration  
- Parallel processing using `concurrent.futures`  
- Unit testing support

## Project Structure

```
etl_project/
├── main.py                      # Entry point for the pipeline
├── config.py                    # Default config (overridden via CLI)
├── etl/
│   ├── file_reader.py           # Reads CSV in chunks
│   ├── transformer.py           # Cleans and transforms data
│   ├── db_writer.py             # DB connection and insertions
│   └── utils.py                 # Logger setup and helpers
├── tests/
│   ├── test_transformer.py      # Tests for transformation logic
│   └── test_db_writer.py        # Tests for DB insertion
├── logs/
│   └── error.log                # Logs errors during execution
├── temp_chunks/                # Temporary chunk storage
├── sample.csv               # Sample CSV (for testing)
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

## Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/guptatejas958/ETL_CSV.git
cd ETL_CSV
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate      
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

## How to Run

You can run the pipeline using the default values in `config.py`, or pass arguments via CLI.

### Option 1: Default config

```bash
python main.py
```

### Option 2: CLI Arguments

```bash
python main.py --csv_path "test_file.csv" --db_path "output.db" --table_name "cleaned_data" --chunk_size 1000 --temp_dir "chunks" --final_csv "cleaned_output.csv" --max_workers 10
```

## Module Responsibilities

### `etl/file_reader.py`
- Uses `pandas.read_csv(..., chunksize=n)`
- Generator yielding one chunk at a time

### `etl/transformer.py`
- Lowercases the `status` field
- Removes rows with:
  - Negative `amount`
  - `status == "cancelled"`
- Adds `processed_at` (UTC)

### `etl/db_writer.py`
- Creates SQLite connection
- Creates target table if missing
- Uses `executemany()` for batch inserts

### `etl/utils.py`
- Sets up a rotating log to `logs/error.log`
- Timestamps and formats logs

### `main.py`
- Orchestrates entire pipeline:
  - Read → Transform → Save chunk → Merge → Load DB
  - Executes transformations in parallel

## Testing

I’ve implemented two primary test modules using `pytest`.
End-to-End integration testing has also been done with 5GB test_file with logs as below. (go to link)
https://drive.google.com/file/d/1ajyroMsUK7h2i8ccYjycDivVMC__f8MA/view?usp=sharing

### 1. `test_transformer.py`
assert cancelled/negative rows removed

### 2. `test_db_writer.py`
Test if the dataframe is writing in DB


### Run Tests

```bash
pytest tests/
```

## Development Timeline

| Stage                     | Time Spent |
|---------------------------|------------|
| Initial Development       | 3 hours    |
| Debugging & CLI Integration | 2 hours |
| Stress Testing (5GB CSV)  | 2.5 hours  |

## Example Log Output

```
[INFO] Starting ETL pipeline with parallel processing...
[INFO] Processed and saved chunk 0
[INFO] Processed and saved chunk 1
[INFO] Merged final CSV written to cleaned_output.csv
[INFO] Inserted 5000 rows into database.
[INFO] ETL pipeline completed successfully.
```

In case of faulty data:

```
[ERROR] Error processing chunk 12: ValueError: could not convert string to float: 'abc'
```

## Author

Built by [Tejas Gupta]  
guptatejas958@gmail.com
