# Refactored parallel.py

from concurrent.futures import ProcessPoolExecutor
import logging
from typing import List
import pandas as pd
from .file_handler import load_data, monitor_resources
from joblib import Parallel, delayed
import os
from typing import List, Any

def parallel_waterfall(video_names: List[str], shap_values: Any, y_sample: List[Any], output_folder: str, n_jobs: int = -1):
    """Generate SHAP waterfall plots in parallel."""
    def generate_plot(idx_video, video_name):
        score_folder = os.path.join(output_folder, str(y_sample[idx_video]))
        ensure_output_folder(score_folder)
        output_path = os.path.join(score_folder, f"{video_name}.png")
        plot_waterfall(shap_values[idx_video], output_path)

    with ProcessPoolExecutor(max_workers=n_jobs) as executor:
        tasks = [
            executor.submit(generate_plot, idx_video, video_name)
            for idx_video, video_name in enumerate(video_names)
        ]
        for future in tasks:
            future.result()

def parallel_beeswarm(unique_scores: List[Any], y_sample: List[Any], shap_values: Any, output_folder: str, n_jobs: int = -1):
    """Generate SHAP beeswarm plots in parallel."""
    def plot_for_score(score):
        score_indices = y_sample[y_sample == score].index.values
        output_path = os.path.join(output_folder, f"beeswarm_score_{score}.png")
        plot_beeswarm(shap_values[score_indices, :, score], output_path)

    Parallel(n_jobs=n_jobs)(delayed(plot_for_score)(score) for score in unique_scores)

def merge_raw_files(file_list: List[str], chunksize=None, max_workers=None, batch_size=5) -> pd.DataFrame:
    """
    Merge multiple raw files into a single DataFrame using multiprocessing.

    Args:
        file_list (List[str]): List of file paths to merge.
        chunksize (int, optional): Number of rows per chunk for memory efficiency.
        max_workers (int, optional): Maximum number of parallel workers.
        batch_size (int): Number of files to process in a batch.

    Returns:
        pd.DataFrame: Merged DataFrame containing all data.
    """
    monitor_resources("before_merge")

    merged_df = pd.DataFrame()

    for i in range(0, len(file_list), batch_size):
        batch = file_list[i:i + batch_size]
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(process_file_safe,
                           batch, [chunksize] * len(batch)))

        for idx, df in enumerate(results):
            if not df.empty:
                merged_df = pd.concat([merged_df, df], ignore_index=True)
        monitor_resources("batch_merge")

    if merged_df.empty:
        logging.warning("Merged DataFrame is empty. Check the input files.")
    else:
        logging.info(f"Merged DataFrame created with {len(merged_df)} rows.")

    return merged_df


def process_file_safe(file_path, chunksize=None):
    """
    Process a single file and return its DataFrame safely.

    Args:
        file_path (str): Path to the file.
        chunksize (int, optional): Number of rows per chunk for memory efficiency.

    Returns:
        pd.DataFrame: Processed DataFrame from the file.
    """
    try:
        data = load_data(file_path, chunksize)
        monitor_resources("process_file")
        return data
    except Exception as e:
        logging.error(f"Error processing file {file_path}: {str(e)}")
        return pd.DataFrame()

# Additional utility function


def log_file_batch(batch: List[str]):
    """
    Log details about the files in a processing batch.

    Args:
        batch (List[str]): List of file paths in the batch.

    Returns:
        None
    """
    logging.info(f"Processing batch of {len(batch)} files: {batch}")
