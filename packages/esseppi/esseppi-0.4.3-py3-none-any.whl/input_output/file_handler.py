# Refactored file_handler.py

from functools import lru_cache
import pandas as pd
import logging
import os
import psutil

import pickle
import logging
from typing import Any

# Constants
XLSX_HEADER_ROW = 2  # Header starts from row 2 (0-indexed)

# Setup logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def ensure_output_folder(folder: str):
    """Ensure the existence of a directory, creating it if necessary."""
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
        
def save_object(obj: Any, path: str):
    """Save a Python object to a file using pickle."""
    try:
        with open(path, "wb") as f:
            pickle.dump(obj, f)
        logging.info(f"Object saved at {path}.")
    except Exception as e:
        logging.error(f"Error saving object to {path}: {e}")

def load_object(path: str) -> Any:
    """Load a Python object from a file using pickle."""
    if not os.path.exists(path):
        logging.error(f"File not found: {path}")
        return None
    try:
        with open(path, "rb") as f:
            obj = pickle.load(f)
        logging.info(f"Object loaded from {path}.")
        return obj
    except Exception as e:
        logging.error(f"Error loading object from {path}: {e}")
        return None

@lru_cache(maxsize=None)
def load_data(file_path, chunksize=None):
    """
    Load data from a file with optional chunking for large files.
    Supports .pkl, .xlsx, and .csv file formats.

    Args:
        file_path (str): Path to the file.
        chunksize (int, optional): Number of rows per chunk for memory efficiency.

    Returns:
        pd.DataFrame: Loaded data as a DataFrame.
    """
    try:
        if file_path.endswith('.pkl'):
            data = pd.read_pickle(file_path)
        elif file_path.endswith('.xlsx'):
            data = pd.read_excel(file_path, header=XLSX_HEADER_ROW)
        elif file_path.endswith('.csv'):
            data = pd.read_csv(file_path, chunksize=chunksize)
        else:
            raise ValueError(f"Unsupported file type: {file_path}")

        if data is None or data.empty:
            logging.warning(
                f"Loaded file '{file_path}' is empty or could not be loaded correctly.")

        return data
    except Exception as e:
        logging.error(f"Error loading file '{file_path}': {str(e)}")
        return pd.DataFrame()


def save_data(df, output_dir, filename, pkl=True, sql_db=None, table_name=None):
    """
    Save DataFrame to multiple formats.

    Args:
        df (pd.DataFrame): Data to save.
        output_dir (str): Directory to save files.
        filename (str): File name without extension.
        pkl (bool): Save as pickle file if True.
        sql_db (str): DuckDB database path.
        table_name (str): Table name for DuckDB database.
    """
    # Ensure resources are monitored before saving
    monitor_resources("save_data")

    os.makedirs(output_dir, exist_ok=True)

    if pkl:
        pkl_path = os.path.join(output_dir, f"{filename}.pkl")
        try:
            df.to_pickle(pkl_path)
            logging.info(f"Data saved as pickle: {pkl_path}")
        except Exception as e:
            logging.error(f"Error saving pickle file {pkl_path}: {str(e)}")


def monitor_resources(stage="default"):
    """
    Monitor system resources and stop the process if memory or CPU usage exceeds thresholds.

    Args:
        stage (str): Identifier for the current processing stage.
    """
    memory = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=1)

    if memory.percent > 85 or cpu > 85:
        logging.error(
            f"Resource usage exceeded during {stage}: Memory {memory.percent}%, CPU {cpu}%. Stopping process.")
        raise SystemExit("Resource usage exceeded threshold.")

# Additional utility function


def get_file_size(file_path):
    """
    Get the size of a file in MB.

    Args:
        file_path (str): Path to the file.

    Returns:
        float: File size in megabytes.
    """
    try:
        size = os.path.getsize(file_path) / (1024 * 1024)
        logging.info(f"File size of '{file_path}': {size:.2f} MB")
        return size
    except Exception as e:
        logging.error(f"Error getting file size for '{file_path}': {str(e)}")
        return -1
