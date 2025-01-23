"""Core module for comparing machine learning models."""

from typing import Dict, List, Any, Union
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.model_selection import cross_validate
from .metrics import MetricsCalculator, calculate_cv_metrics
from .utils import timer, validate_input

class ModelComparator:
    """Class for comparing multiple machine learning models."""

    def __init__(self, random_state: int = 42):
        """
        Initialize ModelComparator.

        Args:
            random_state: Random seed for reproducibility
        """
        self.random_state = random_state
        self.results = {}
        self.models = {}
        self.metrics_calculator = MetricsCalculator()

    def add_model(self, name: str, model: BaseEstimator) -> None:
        """
        Add a model to the comparison.

        Args:
            name: Name of the model
            model: Model instance
        """
        if hasattr(model, 'random_state'):
            model.random_state = self.random_state
        self.models[name] = model

    @timer
    def compare(
        self,
        X: np.ndarray,
        y: np.ndarray,
        cv: int = 5,
        scoring: List[str] = None,
        return_train_score: bool = True
    ) -> pd.DataFrame:
        """
        Compare all added models using cross-validation.

        Args:
            X: Feature matrix
            y: Target vector
            cv: Number of cross-validation folds
            scoring: List of scoring metrics
            return_train_score: Whether to include training scores

        Returns:
            DataFrame containing comparison results
        """
        validate_input(X, y)

        if scoring is None:
            scoring = ['accuracy', 'precision_weighted', 'recall_weighted', 'f1_weighted']

        results = []

        for name, model in self.models.items():
            cv_results = cross_validate(
                model,
                X, y,
                cv=cv,
                scoring=scoring,
                n_jobs=-1,
                return_train_score=return_train_score
            )

            metrics = calculate_cv_metrics(cv_results)
            metrics['model'] = name
            results.append(metrics)

            # Store detailed results
            self.results[name] = {
                'cv_results': cv_results,
                'metrics': metrics
            }

        return pd.DataFrame(results)

    def get_best_model(self, metric: str = 'test_accuracy') -> str:
        """
        Get the name of the best performing model.

        Args:
            metric: Metric to use for comparison

        Returns:
            Name of the best model
        """
        if not self.results:
            raise ValueError("No comparison results available. Run compare() first.")

        scores = {
            name: results['metrics'][metric]['mean']
            for name, results in self.results.items()
        }
        return max(scores.items(), key=lambda x: x[1])[0]

    def get_detailed_results(self) -> Dict[str, Any]:
        """Get detailed comparison results."""
        return self.results

    def summary(self) -> str:
        """
        Generate a formatted summary of the comparison results.

        Returns:
            Formatted string containing the comparison summary
        """
        if not self.results:
            return "No comparison results available. Run compare() first."

        summary = ["Model Comparison Summary:", "=" * 50, ""]

        for model_name, results in self.results.items():
            summary.append(f"\nModel: {model_name}")
            summary.append("-" * 20)

            metrics = results['metrics']
            for metric, values in metrics.items():
                if metric != 'model':
                    summary.append(f"{metric}:")
                    for stat, value in values.items():
                        summary.append(f"  {stat}: {value:.4f}")

        return "\n".join(summary)