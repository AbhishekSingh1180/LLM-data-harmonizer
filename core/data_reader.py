import pandas as pd
from typing import Union
import os
import logging
logging.basicConfig(level=logging.INFO)


def input_path() -> str:
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

    logging.info('File Path: %s', data_dir)

    if not os.path.exists(data_dir) or not os.path.isdir(data_dir):
        logging.error("Data directory does not exist: %s", data_dir)
        raise FileNotFoundError(f"Data directory does not exist: {data_dir}")

    files = [f for f in os.listdir(data_dir)
             if os.path.isfile(os.path.join(data_dir, f))]
    if not files:
        logging.error("No files found in data directory: %s", data_dir)
        raise FileNotFoundError(f"No files found in data directory: {data_dir}")

    data_path: str = os.path.join(data_dir, files[0])

    return data_path


def read(file_path: str) -> Union[pd.DataFrame, str, list[str], None]:
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.json'):
        return pd.read_json(file_path)
    elif file_path.endswith('.parquet'):
        return pd.read_parquet(file_path)
    elif file_path.endswith('.md'):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        print(f"Unsupported file format: {file_path}")
        return None
