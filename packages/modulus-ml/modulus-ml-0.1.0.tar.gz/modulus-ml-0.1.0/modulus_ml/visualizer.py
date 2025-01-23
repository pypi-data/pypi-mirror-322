"""Module for visualizing model comparison results."""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import Dict, Optional, List

class ComparisonVisualizer:
    """Class for creating visualizations of model comparisons."""

    @staticmethod
    def plot_metric_comparison(
        results: pd.DataFrame,
        metric: str = 'test_accuracy',
        figsize: tuple = (10, 6)
    ) -> None:
        """
        Plot comparison of models for a specific metric.

        Args:
            results: DataFrame containing comparison results
            metric: Metric to visualize
            figsize: Figure size
        """
        plt.figure(figsize=figsize)

        data = results[['model', metric]].copy()

        sns.barplot(x='model', y=metric, data=data)
        plt.title(f'Model Comparison - {metric}')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_metrics_heatmap(
        results: pd.DataFrame,
        metrics: Optional[List[str]] = None,
        figsize: tuple = (12, 8)
    ) -> None:
        """
        Create a heatmap of all metrics for all models.

        Args:
            results: DataFrame containing comparison results
            metrics: List of metrics to include
            figsize: Figure size
        """
        plt.figure(figsize=figsize)

        if metrics is None:
            metrics = [col for col in results.columns if col != 'model']

        data = results.set_index('model')[metrics]

        sns.heatmap(data, annot=True, cmap='YlOrRd', center=0)
        plt.title('Model Comparison Heatmap')
        plt.tight_layout()
        plt.show()