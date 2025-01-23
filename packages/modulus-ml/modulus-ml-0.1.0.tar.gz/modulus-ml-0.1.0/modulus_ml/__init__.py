"""
Modulus ML - A comprehensive machine learning model comparison library.
"""

from .comparator import ModelComparator
from .metrics import MetricsCalculator
from .visualizer import ComparisonVisualizer

__version__ = "0.1.0"

__all__ = ["ModelComparator", "MetricsCalculator", "ComparisonVisualizer"]