# tests/test_comparator.py

import pytest
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from modulus_ml.comparator import ModelComparator

def test_model_comparison():
    # Create sample data
    X, y = make_classification(n_samples=100, n_features=20, random_state=42)

    # Initialize comparator
    comparator = ModelComparator()

    # Add models
    comparator.add_model('logistic', LogisticRegression())
    comparator.add_model('random_forest', RandomForestClassifier())

    # Run comparison
    results = comparator.compare(X, y)

    # Check results
    assert len(results) == 2
    assert 'logistic' in comparator.results
    assert 'random_forest' in comparator.results