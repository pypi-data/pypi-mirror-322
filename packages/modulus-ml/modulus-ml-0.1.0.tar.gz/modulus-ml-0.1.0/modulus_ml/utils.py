"""Utility functions for the modulus-ml package."""

import time
from functools import wraps
from typing import Callable, Any

def timer(func: Callable) -> Callable:
    """
    A decorator that prints the execution time of a function.

    Args:
        func: The function to be timed

    Returns:
        The wrapped function
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.2f} seconds to execute")
        return result
    return wrapper

def validate_input(X, y):
    """
    Validate input data for model comparison.

    Args:
        X: Feature matrix
        y: Target vector

    Raises:
        ValueError: If inputs are invalid
    """
    if X is None or y is None:
        raise ValueError("Input data cannot be None")
    if len(X) != len(y):
        raise ValueError("X and y must have the same length")