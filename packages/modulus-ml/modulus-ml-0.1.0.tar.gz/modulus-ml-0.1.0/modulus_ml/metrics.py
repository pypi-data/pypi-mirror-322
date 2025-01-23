"""Module for calculating and aggregating model performance metrics."""

from typing import Dict, List, Union
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

class MetricsCalculator:
    """Class for calculating various model performance metrics."""

    @staticmethod
    def calculate_basic_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """
        Calculate basic classification metrics.

        Args:
            y_true: True labels
            y_pred: Predicted labels

        Returns:
            Dictionary containing metric scores
        """
        return {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, average='weighted'),
            'recall': recall_score(y_true, y_pred, average='weighted'),
            'f1': f1_score(y_true, y_pred, average='weighted')
        }

    @staticmethod
    def calculate_advanced_metrics(y_true: np.ndarray, y_pred_proba: np.ndarray) -> Dict[str, float]:
        """
        Calculate advanced classification metrics.

        Args:
            y_true: True labels
            y_pred_proba: Predicted probabilities

        Returns:
            Dictionary containing metric scores
        """
        try:
            roc_auc = roc_auc_score(y_true, y_pred_proba, multi_class='ovr')
        except ValueError:
            roc_auc = None

        return {
            'roc_auc': roc_auc
        }

def calculate_cv_metrics(cv_results: Dict[str, np.ndarray]) -> Dict[str, Dict[str, float]]:
    """
    Calculate metrics from cross-validation results.

    Args:
        cv_results: Cross-validation results dictionary

    Returns:
        Dictionary containing mean and std of metrics
    """
    metrics = {}

    for key in cv_results:
        if key.startswith(('test_', 'train_')):
            scores = cv_results[key]
            metric_name = key.split('_', 1)[1]
            metrics[key] = {
                'mean': scores.mean(),
                'std': scores.std(),
                'min': scores.min(),
                'max': scores.max()
            }

    return metrics

def get_metric_names() -> List[str]:
    """Get list of available metric names."""
    return ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']