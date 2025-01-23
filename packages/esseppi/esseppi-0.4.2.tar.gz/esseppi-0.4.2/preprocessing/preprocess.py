import logging
from esseppi.preprocessing.cleaning import handle_missing_values, fix_data_types, remove_classes_below_threshold
from esseppi.memory import optimize_memory


def preprocess(df, target_column, threshold=50, date_columns=None, numeric_columns=None, critical_columns=None):
    """
    Preprocess the dataset by handling missing values, fixing data types, 
    removing classes below a threshold, and optimizing memory usage.

    Args:
        df (pd.DataFrame): Input DataFrame.
        target_column (str): The target column for the dataset.
        threshold (int): Minimum number of samples required per class.
        date_columns (list, optional): List of columns to convert to datetime.
        numeric_columns (list, optional): List of columns to convert to numeric.
        critical_columns (list, optional): List of critical columns that must not contain NaN.

    Returns:
        pd.DataFrame: Preprocessed DataFrame.
    """
    logging.info("Starting data preprocessing...")

    # Step 1: Handle missing values
    if critical_columns:
        df = handle_missing_values(df, critical_columns, missing_threshold=0.5)

    # Step 2: Fix data types
    df = fix_data_types(df, date_columns=date_columns,
                        numeric_columns=numeric_columns)

    # Step 3: Handle class imbalance
    df = remove_classes_below_threshold(df, target_column, threshold)

    # Step 4: Optimize memory usage
    df = optimize_memory(df)

    logging.info("Data preprocessing completed.")
    return df
