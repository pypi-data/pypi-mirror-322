from sklearn.preprocessing import OrdinalEncoder, StandardScaler
import logging
import pandas as pd

DATE_FORMAT = "%d-%b-%Y"  # Date format for Italian locale


def handle_missing_values(df: pd.DataFrame, critical_columns: list, missing_threshold: float = 0.5) -> pd.DataFrame:
    """
    Handle missing values by dropping rows with missing critical values and columns exceeding a threshold of missing data.

    Args:
        df (pd.DataFrame): Input DataFrame.
        critical_columns (list): Columns that must not have missing values.
        missing_threshold (float): Proportion threshold for dropping columns.

    Returns:
        pd.DataFrame: DataFrame with missing values handled.
    """
    logging.info("Handling missing values...")

    for col in critical_columns:
        if col in df.columns:
            df = df.dropna(subset=[col])
        else:
            logging.warning(f"Critical column '{col}' not found.")

    missing_ratio = df.isnull().mean()
    columns_dropped = missing_ratio[missing_ratio >
                                    missing_threshold].index.tolist()
    df = df.drop(columns=columns_dropped)

    logging.info(
        f"Dropped columns exceeding missing threshold: {columns_dropped}")
    return df


def fix_data_types(
    df: pd.DataFrame, date_columns: list = [], numeric_columns: list = []
) -> pd.DataFrame:
    """
    Convert specified columns to appropriate data types.

    Args:
        df (pd.DataFrame): Input DataFrame.
        date_columns (list, optional): List of date columns to convert.
        numeric_columns (list, optional): List of numeric columns to convert.

    Returns:
        pd.DataFrame: DataFrame with corrected data types.
    """
    date_columns = date_columns or []
    numeric_columns = numeric_columns or []

    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(
                df[col], format=DATE_FORMAT, errors="coerce")

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    other_columns = set(df.columns) - set(date_columns) - set(numeric_columns)
    for col in other_columns:
        df[col] = df[col].astype(str).fillna("Unknown")

    return df


def remove_classes_below_threshold(df: pd.DataFrame, target_column: str, threshold: int) -> pd.DataFrame:
    """
    Remove rows belonging to classes with fewer samples than the specified threshold.

    Args:
        df (pd.DataFrame): Input DataFrame.
        target_column (str): Column containing class labels.
        threshold (int): Minimum number of samples per class.

    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    class_counts = df[target_column].value_counts()
    valid_classes = class_counts[class_counts >= threshold].index
    return df[df[target_column].isin(valid_classes)]


def extract_year_from_date(df: pd.DataFrame, date_column: str, year_column: str) -> pd.DataFrame:
    """
    Extract the year from a date column and add it as a new column.

    Args:
        df (pd.DataFrame): Input DataFrame.
        date_column (str): Column containing date values.
        year_column (str): Name of the new column for extracted year values.

    Returns:
        pd.DataFrame: DataFrame with the year column added.
    """
    if date_column in df.columns:
        df[year_column] = pd.to_datetime(
            df[date_column], errors="coerce").dt.year
    return df


def handle_invalid_values(
    df: pd.DataFrame, column_name: str, min_value: float, max_value: float, action: str = "warn"
) -> pd.DataFrame:
    """
    Handle invalid values by logging or removing them.

    Args:
        df (pd.DataFrame): Input DataFrame.
        column_name (str): Column to validate.
        min_value (float): Minimum valid value.
        max_value (float): Maximum valid value.
        action (str): Action to take ('warn' or 'remove').

    Returns:
        pd.DataFrame: DataFrame with invalid values handled.
    """
    if column_name not in df.columns:
        return df

    invalid_rows = df[(df[column_name] < min_value) |
                      (df[column_name] > max_value)]
    if action == "warn" and not invalid_rows.empty:
        logging.warning(
            f"Invalid values in column '{column_name}':\n{invalid_rows}")
    elif action == "remove":
        df = df[(df[column_name] >= min_value) &
                (df[column_name] <= max_value)]
    return df


def anonymize_values(df: pd.DataFrame) -> tuple:
    """
    Anonymize values in the dataset using specific transformations based on data type:
    - OrdinalEncoder for categorical, string, and date columns.
    - StandardScaler for numeric columns.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        tuple: Anonymized DataFrame and metadata for reversal.
    """
    logging.info("Starting anonymization process...")

    anonymized_df = df.copy()
    metadata = {"encoders": {}, "scalers": {}}

    # Process columns
    for col in anonymized_df.columns:
        if anonymized_df[col].dtype == "object" or pd.api.types.is_categorical_dtype(anonymized_df[col]):
            # Ordinal encoding for strings, categorical, or object columns
            logging.info(
                f"Anonymizing categorical column '{col}' using OrdinalEncoder...")
            encoder = OrdinalEncoder(
                handle_unknown="use_encoded_value", unknown_value=-1)
            anonymized_df[col] = encoder.fit_transform(
                anonymized_df[[col]].astype(str))
            metadata["encoders"][col] = encoder

        elif pd.api.types.is_datetime64_any_dtype(anonymized_df[col]):
            # Ordinal encoding for date columns
            logging.info(
                f"Anonymizing date column '{col}' using OrdinalEncoder...")
            encoder = OrdinalEncoder(
                handle_unknown="use_encoded_value", unknown_value=-1)
            anonymized_df[col] = encoder.fit_transform(
                anonymized_df[[col]].astype(str))
            metadata["encoders"][col] = encoder

        elif pd.api.types.is_numeric_dtype(anonymized_df[col]):
            # Standard scaling for numeric columns
            logging.info(
                f"Anonymizing numeric column '{col}' using StandardScaler...")
            scaler = StandardScaler()
            anonymized_df[col] = scaler.fit_transform(
                anonymized_df[[col]].fillna(0))
            metadata["scalers"][col] = scaler

        else:
            # Handle unexpected column types
            logging.warning(
                f"Column '{col}' has an unsupported type and will be skipped.")
            anonymized_df[col] = anonymized_df[col].astype(str)

    logging.info("Anonymization process completed.")
    return anonymized_df, metadata


def pivot_aggregated_data(df: pd.DataFrame, indexes: list, columns: list, values: list) -> pd.DataFrame:
    """
    Pivot aggregated data for analysis and machine learning.

    Args:
        df (pd.DataFrame): Aggregated DataFrame.
        indexes (list): Columns to use as pivot indexes.
        columns (list): Columns to pivot.
        values (list): Columns to use as values.

    Returns:
        pd.DataFrame: Pivoted DataFrame.
    """
    pivoted = df.pivot(index=indexes, columns=columns, values=values)
    pivoted.columns = [f"{metric} {month}" for metric,
                       month in pivoted.columns]
    pivoted.reset_index(inplace=True)
    return pivoted


def filter_invalid_grades(df: pd.DataFrame, grade_column: str, flag_column: str = "Flag Giudizio/Voto", judgement_column: str = "Giudizio") -> pd.DataFrame:
    """
    Handle invalid grades based on flag and judgement columns.

    Args:
        df (pd.DataFrame): Input DataFrame.
        grade_column (str): Column for grades.
        flag_column (str): Column indicating grade flag.
        judgement_column (str): Column indicating judgement.

    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    if grade_column not in df.columns or flag_column not in df.columns or judgement_column not in df.columns:
        logging.warning(
            "Required columns are missing. Skipping grade filtering.")
        return df

    def determine_grade(row):
        if row[flag_column] == "N":
            return row[grade_column]
        elif row[flag_column] == "S":
            return 30 if row[judgement_column] == "IDONEO" else None
        return None

    df[grade_column] = df.apply(determine_grade, axis=1)
    df = handle_invalid_values(df, grade_column, 17, 30, action="remove")
    return df.dropna(subset=[grade_column])


def validate_columns(df: pd.DataFrame, required_columns: list) -> None:
    """
    Validate the presence of required columns in the DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame.
        required_columns (list): List of required column names.

    Raises:
        ValueError: If any required column is missing.
    """
    missing_columns = [
        col for col in required_columns if col not in df.columns]
    if missing_columns:
        logging.error(f"Missing required columns: {missing_columns}")
        raise ValueError(f"Missing columns: {missing_columns}")


def compute_weighted_average(df: pd.DataFrame, grade_column: str, credit_column: str) -> float:
    """
    Compute the weighted average of grades based on credits.

    Args:
        df (pd.DataFrame): Input DataFrame.
        grade_column (str): Column with grade values.
        credit_column (str): Column with credit values.

    Returns:
        float: Weighted average of grades.
    """
    total_weighted = (df[grade_column] * df[credit_column]).sum()
    total_credits = df[credit_column].sum()
    return total_weighted / total_credits if total_credits > 0 else float("nan")


def anonymize_feature_names(df: pd.DataFrame) -> tuple:
    """
    Replace feature names with generic ones for anonymization.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        tuple: Anonymized DataFrame and a dictionary mapping original names to new ones.
    """
    column_mapping = {col: f"Feature_{i+1}" for i,
                      col in enumerate(df.columns)}
    anonymized_df = df.rename(columns=column_mapping)
    return anonymized_df, column_mapping


def de_anonymize_values(df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
    """
    Reverse the anonymization process for DataFrame values using metadata.

    Args:
        df (pd.DataFrame): Anonymized DataFrame.
        metadata (dict): Metadata containing encoders and scalers.

    Returns:
        pd.DataFrame: De-anonymized DataFrame.
    """
    for col, encoder in metadata.get("encoders", {}).items():
        df[col] = encoder.inverse_transform(df[[col]])

    for col, scaler in metadata.get("scalers", {}).items():
        df[col] = scaler.inverse_transform(df[[col]])

    return df
