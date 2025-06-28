# ETL Project: Large CSV Processor

This project performs an ETL (Extract, Transform, Load) pipeline on a large transaction CSV file using pandas and SQLite.

## Features

- Chunked CSV reading using `pandas.read_csv(chunksize=...)`
- Transformation (filtering and cleaning)
- Intermediate chunk storage
- Final aggregation and SQLite database load
- Parallel processing
- Robust error handling
- Unit testing for transformation and DB logic

## How to Run

```bash
python main.py --input transactions.csv --db database.sqlite --chunksize 50000
