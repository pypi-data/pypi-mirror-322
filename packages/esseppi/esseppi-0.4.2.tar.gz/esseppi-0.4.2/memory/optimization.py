# Refactored optimization.py

import pandas as pd


def optimize_memory(df: pd.DataFrame) -> pd.DataFrame:
    """
    Optimize memory usage by downcasting numeric columns and converting suitable object columns to categories.

    Parameters:
        df (pd.DataFrame): The DataFrame to optimize.

    Returns:
        pd.DataFrame: The optimized DataFrame.
    """
    initial_memory = df.memory_usage(deep=True).sum()

    # Optimize numeric columns
    for col in df.select_dtypes(include=['float', 'int']).columns:
        try:
            df[col] = pd.to_numeric(
                df[col], downcast='integer' if df[col].dtype.kind == 'i' else 'float')
        except ValueError as e:
            logging.warning(f"Skipping column '{col}' due to error: {e}")

    # Optimize object columns
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].nunique() / max(len(df[col]), 1) < 0.5:  # High cardinality check
            try:
                df[col] = df[col].astype('category')
            except ValueError as e:
                logging.warning(f"Skipping column '{col}' due to error: {e}")

    final_memory = df.memory_usage(deep=True).sum()
    logging.info(
        f"Memory usage reduced from {initial_memory / 1024**2:.2f} MB to {final_memory / 1024**2:.2f} MB")

    return df

# Additional utility function


def memory_usage_report(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate a memory usage report for each column in the DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: A DataFrame with memory usage details for each column.
    """
    usage = df.memory_usage(deep=True).to_frame(name="Memory (bytes)")
    usage["Memory (MB)"] = usage["Memory (bytes)"] / (1024**2)
    usage["Data Type"] = df.dtypes.values
    return usage.reset_index().rename(columns={"index": "Column"})
