import os
import logging
import matplotlib.pyplot as plt
import pandas as pd
import shap
import os
from typing import Any

def generate_best_plot(
    series_before: pd.Series,
    series_after: pd.Series,
    column_name: str,
    output_dir: str,
    scale: str = "linear",
    orientation: str = "vertical",
    show_before: bool = True,
    show_after: bool = True
) -> None:
    """
    Generate a distribution plot for a column with options to compare before and after cleaning.

    Args:
        series_before (pd.Series): Column data before cleaning.
        series_after (pd.Series): Column data after cleaning.
        column_name (str): Name of the column.
        output_dir (str): Directory to save the plots.
        scale (str): Scale of the plot ('linear' or 'log').
        orientation (str): Orientation of the plot ('vertical' or 'horizontal').
        show_before (bool): Whether to include the "before cleaning" distribution.
        show_after (bool): Whether to include the "after cleaning" distribution.

    Returns:
        None
    """
    os.makedirs(output_dir, exist_ok=True)

    if series_before.empty or series_after.empty:
        logging.warning(
            f"Column {column_name} is empty. Skipping plot generation.")
        return

    if len(series_before.unique()) < 2 and len(series_after.unique()) < 2:
        logging.warning(
            f"Column {column_name} has fewer than 2 unique values. Skipping plot generation.")
        return

    if scale == "log" and (series_before.min() <= 0 or series_after.min() <= 0):
        logging.warning(
            f"Log scale not applicable for column {column_name} with non-positive values. Switching to linear scale.")
        scale = "linear"

    plt.figure(figsize=(12, 6))
    is_numeric = pd.api.types.is_numeric_dtype(series_before)
    before_color, after_color = "#1b9e77", "#d95f02"

    if is_numeric:
        plot_fn = plt.hist
        if orientation == "horizontal":
            orientation_args = {"orientation": "horizontal"}
        else:
            orientation_args = {}

        if show_before:
            plot_fn(
                series_before,
                bins=30,
                alpha=0.6,
                label="Before Cleaning",
                color=before_color,
                edgecolor="black",
                log=(scale == "log"),
                **orientation_args
            )

        if show_after:
            plot_fn(
                series_after,
                bins=30,
                alpha=0.6,
                label="After Cleaning",
                color=after_color,
                edgecolor="black",
                log=(scale == "log"),
                **orientation_args
            )

        plt.xlabel("Value") if orientation == "vertical" else plt.ylabel("Value")
        plt.ylabel("Frequency") if orientation == "vertical" else plt.xlabel(
            "Frequency")
    else:
        plot_fn = "barh" if orientation == "horizontal" else "bar"

        if show_before:
            series_before.value_counts().plot(
                kind=plot_fn,
                alpha=0.6,
                label="Before Cleaning",
                color=before_color,
                log=(scale == "log")
            )

        if show_after:
            series_after.value_counts().plot(
                kind=plot_fn,
                alpha=0.6,
                label="After Cleaning",
                color=after_color,
                log=(scale == "log")
            )

        plt.ylabel("Category") if orientation == "vertical" else plt.xlabel(
            "Category")
        plt.xlabel("Frequency") if orientation == "vertical" else plt.ylabel(
            "Frequency")

    plt.title(f"Distribution of {column_name} Before and After Cleaning")
    plt.legend()
    plt.tight_layout()

    plot_path = os.path.join(output_dir, f"{column_name}_distribution.png")
    plt.savefig(plot_path)
    plt.close()
    logging.info(f"Plot for {column_name} saved to {plot_path}.")


def generate_stats(
    df_before: pd.DataFrame, df_after: pd.DataFrame, output_dir: str, dataset_name: str
) -> dict:
    """
    Generate and save dataset statistics before and after cleaning.

    Args:
        df_before (pd.DataFrame): Dataset before cleaning.
        df_after (pd.DataFrame): Dataset after cleaning.
        output_dir (str): Directory to save the statistics.
        dataset_name (str): Name of the dataset.

    Returns:
        dict: Dictionary containing dataset statistics.
    """
    os.makedirs(output_dir, exist_ok=True)

    stats = {
        "dataset_name": dataset_name,
        "rows_before": len(df_before),
        "rows_after": len(df_after),
        "columns_before": len(df_before.columns),
        "columns_after": len(df_after.columns),
        "missing_percentage_before": df_before.isnull().mean().mean() * 100,
        "missing_percentage_after": df_after.isnull().mean().mean() * 100,
    }

    stats_file = os.path.join(output_dir, f"{dataset_name}_stats.csv")
    pd.DataFrame([stats]).to_csv(stats_file, index=False)
    logging.info(f"Statistics for {dataset_name} saved to {stats_file}.")

    return stats


def log_dataframe_stats(df: pd.DataFrame, message: str) -> None:
    """
    Log basic statistics for a DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame.
        message (str): Message describing the logged DataFrame.

    Returns:
        None
    """
    if df.empty:
        logging.warning(f"{message}: DataFrame is empty.")
    else:
        logging.info(
            f"{message}: Rows = {len(df)}, Columns = {len(df.columns)}\nSample Data:\n{df.head()}"
        )


def save_feature_importance(
    model, feature_names: list, visualization_path: str, threshold: float = 0.01
) -> None:
    """
    Save feature importance visualization for a model, filtering by importance threshold.

    Args:
        model: Trained model with feature importances.
        feature_names (list): List of feature names.
        visualization_path (str): Directory to save the plot.
        threshold (float): Minimum importance value for features to be included in the plot.

    Returns:
        None
    """
    os.makedirs(visualization_path, exist_ok=True)

    # Retrieve feature importances
    importances = model.feature_importances_

    # Create a DataFrame for easier filtering and sorting
    importance_df = pd.DataFrame({
        "Feature": feature_names,
        "Importance": importances
    }).sort_values(by="Importance", ascending=False)

    # Filter features based on the threshold
    filtered_df = importance_df[importance_df["Importance"] >= threshold]

    # Log the number of filtered features
    logging.info(
        f"{len(filtered_df)} features selected with importance >= {threshold}. Total features: {len(importance_df)}"
    )

    # Plot the filtered features
    # Adjust height dynamically
    plt.figure(figsize=(10, max(6, len(filtered_df) / 5)))
    plt.barh(filtered_df["Feature"], filtered_df["Importance"],
             align="center", color="#1f77b4")
    plt.xlabel("Feature Importance")
    plt.ylabel("Feature")
    plt.title(f"Top Features (Importance >= {threshold})")
    plt.tight_layout()

    # Save the plot
    plot_path = os.path.join(
        visualization_path, "feature_importance_filtered.png")
    plt.savefig(plot_path)
    plt.close()
    logging.info(f"Filtered feature importance plot saved to {plot_path}.")

    # Save the filtered data to CSV
    csv_path = os.path.join(
        visualization_path, "feature_importance_filtered.csv")
    filtered_df.to_csv(csv_path, index=False)
    logging.info(f"Filtered feature importance data saved to {csv_path}.")



def plot_waterfall(shap_values: Any, output_path: str, max_display: int = 9):
    """Plot a SHAP waterfall plot."""
    plt.figure(figsize=(12, 8))
    shap.plots.waterfall(shap_values, show=False, max_display=max_display)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_beeswarm(shap_values: Any, output_path: str):
    """Plot a SHAP beeswarm plot."""
    plt.figure(figsize=(12, 8))
    shap.plots.beeswarm(shap_values, show=False)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_scatter(shap_values: Any, output_path: str):
    """Plot a SHAP scatter plot."""
    plt.figure(figsize=(12, 8))
    shap.plots.scatter(shap_values, color=shap_values, show=False)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
