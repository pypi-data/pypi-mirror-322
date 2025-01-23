import logging
import pandas as pd
import os

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
)


def evaluate_model(
    model, X, y, fold=None, model_name="RF", metrics_path="metrics.xlsx", save_metrics=False
):
    """
    Evaluate model, log metrics, and optionally save them to an Excel file.

    Args:
        model: Trained model to evaluate.
        X (pd.DataFrame or np.ndarray): Features for evaluation.
        y (pd.Series or np.ndarray): True labels for evaluation.
        fold (int, optional): Fold index (if using cross-validation).
        model_name (str): Name of the model.
        metrics_path (str): Path to save the metrics Excel file.
        save_metrics (bool): Whether to save metrics to a file.

    Returns:
        dict: Evaluation metrics.
        np.ndarray: Confusion matrix.
    """

    # Calculate predictions and probabilities
    predictions = model.predict(X)
    probabilities = model.predict_proba(X)[:, 1] if hasattr(
        model, "predict_proba") else None

    # Calculate metrics
    metrics = {
        "Model": model_name,
        "Fold": fold,
        "Accuracy": round(accuracy_score(y, predictions), 4),
        "Precision": round(precision_score(y, predictions), 4),
        "Recall": round(recall_score(y, predictions), 4),
        "F1": round(f1_score(y, predictions), 4),
    }
    if probabilities is not None:
        metrics["ROC_AUC"] = round(roc_auc_score(y, probabilities), 4)

    # Confusion matrix
    confusion = confusion_matrix(y, predictions)
    metrics.update({
        "TP": int(confusion[1, 1]),
        "TN": int(confusion[0, 0]),
        "FP": int(confusion[0, 1]),
        "FN": int(confusion[1, 0]),
    })

    # Log metrics
    logging.info(f"Metrics: {metrics}")
    logging.info(f"Confusion Matrix:\n{confusion}")

    # Save metrics to CSV if required
    if save_metrics:
        metrics_df = pd.DataFrame([metrics])
        # Ensure values are rounded to 4 decimals
        metrics_df = metrics_df.round(4)

        # Check if the CSV file exists
        write_header = not os.path.exists(metrics_path)

        # Save to CSV
        metrics_df.to_csv(metrics_path, index=False,
                          mode="a", header=write_header)
        if write_header:
            logging.info(
                f"Metrics saved with header to new CSV file: {metrics_path}")
        else:
            logging.info(
                f"Metrics appended to existing CSV file: {metrics_path}")

    return metrics, confusion
