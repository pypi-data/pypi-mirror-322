"""
Statistical computations module providing basic and advanced statistical functions.
"""

import numpy as np
import pandas as pd
from scipy import stats
from typing import Union, Optional, Tuple

def describe_column(data: pd.DataFrame, column: str) -> dict:
    """
    Calculate basic statistical measures for a column.
    
    Args:
        data: Input DataFrame
        column: Name of the column to analyze
        
    Returns:
        dict: Dictionary containing statistical measures
    """
    series = data[column]
    return {
        "mean": series.mean(),
        "median": series.median(),
        "mode": series.mode().iloc[0],
        "std": series.std(),
        "variance": series.var(),
        "skewness": series.skew(),
        "kurtosis": series.kurtosis()
    }

def correlation_analysis(data: pd.DataFrame, method: str = "pearson") -> pd.DataFrame:
    """
    Calculate correlation matrix for numerical columns.
    
    Args:
        data: Input DataFrame
        method: Correlation method ("pearson", "spearman", or "kendall")
        
    Returns:
        pd.DataFrame: Correlation matrix
    """
    return data.select_dtypes(include=[np.number]).corr(method=method)

def ttest_columns(data: pd.DataFrame, col1: str, col2: str) -> Tuple[float, float]:
    """
    Perform Student's t-test between two columns.
    
    Args:
        data: Input DataFrame
        col1: First column name
        col2: Second column name
        
    Returns:
        Tuple[float, float]: t-statistic and p-value
    """
    t_stat, p_value = stats.ttest_ind(data[col1], data[col2])
    return t_stat, p_value 