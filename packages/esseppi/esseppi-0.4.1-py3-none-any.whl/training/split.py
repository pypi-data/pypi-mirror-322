import logging
import time
from sklearn.model_selection import train_test_split


def validate_splits(train_split: float, val_split: float, test_split: float) -> None:
    """
    Validate that the dataset splits add up to 1.

    Args:
        train_split (float): Proportion of training data.
        val_split (float): Proportion of validation data.
        test_split (float): Proportion of test data.

    Raises:
        ValueError: If the splits do not sum to approximately 1.
    """
    total_split = train_split + val_split + test_split
    if not 0.99 <= total_split <= 1.01:
        raise ValueError(
            "Train, validation, and test splits must sum up to 1.")


def split_data(
    X, y, train_split: float, val_split: float, test_split: float, random_state: int
):
    """
    Split data into training, validation, and test sets.

    Args:
        X (array-like): Features dataset.
        y (array-like): Target labels.
        train_split (float): Proportion of training data.
        val_split (float): Proportion of validation data.
        test_split (float): Proportion of test data.
        random_state (int): Random seed for reproducibility.

    Returns:
        tuple: (X_train, X_val, X_test, y_train, y_val, y_test)
    """
    start_time = time.time()
    validate_splits(train_split, val_split, test_split)

    # Initial split for training set
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=(1 - train_split), stratify=y, random_state=random_state
    )

    # Further split for validation and test sets
    val_proportion = val_split / (val_split + test_split)
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=(1 - val_proportion), stratify=y_temp, random_state=random_state
    )

    logging.info(
        f"Data split completed in {time.time() - start_time:.2f} seconds.")
    logging.info(
        f"Training set size: {len(y_train)}, Validation set size: {len(y_val)}, Test set size: {len(y_test)}")

    return X_train, X_val, X_test, y_train, y_val, y_test
