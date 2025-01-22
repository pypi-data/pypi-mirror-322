"""
Data manipulation module for handling CSV files and data transformations.
"""

import pandas as pd
import numpy as np
from typing import Union, Optional

def read_csv(filepath: str, **kwargs) -> pd.DataFrame:
    """
    Read a CSV file into a pandas DataFrame.
    
    Args:
        filepath: Path to the CSV file
        **kwargs: Additional arguments passed to pandas.read_csv
        
    Returns:
        pd.DataFrame: The loaded data
    """
    return pd.read_csv(filepath, **kwargs)

def normalize_column(data: pd.DataFrame, column: str, method: str = "minmax") -> pd.DataFrame:
    """
    Normalize a column in the DataFrame.
    
    Args:
        data: Input DataFrame
        column: Name of the column to normalize
        method: Normalization method ("minmax" or "zscore")
        
    Returns:
        pd.DataFrame: DataFrame with normalized column
    """
    df = data.copy()
    
    if method == "minmax":
        df[column] = (df[column] - df[column].min()) / (df[column].max() - df[column].min())
    elif method == "zscore":
        df[column] = (df[column] - df[column].mean()) / df[column].std()
    else:
        raise ValueError("Method must be either 'minmax' or 'zscore'")
    
    return df 