"""
Tests for the data manipulation module.
"""

import pytest
import pandas as pd
import numpy as np
from datalib.data_manipulation import normalize_column

def test_normalize_column_minmax():
    """Test minmax normalization"""
    df = pd.DataFrame({"A": [1, 2, 3, 4, 5]})
    result = normalize_column(df, "A", method="minmax")
    
    # Check if values are between 0 and 1
    assert result["A"].min() == 0
    assert result["A"].max() == 1
    
    # Check if original data is unchanged
    assert df["A"].tolist() == [1, 2, 3, 4, 5]

def test_normalize_column_zscore():
    """Test z-score normalization"""
    df = pd.DataFrame({"A": [1, 2, 3, 4, 5]})
    result = normalize_column(df, "A", method="zscore")
    
    # Check if mean is close to 0 and std is close to 1
    assert abs(result["A"].mean()) < 1e-10
    assert abs(result["A"].std() - 1) < 1e-10

def test_normalize_column_invalid_method():
    """Test invalid normalization method"""
    df = pd.DataFrame({"A": [1, 2, 3]})
    with pytest.raises(ValueError):
        normalize_column(df, "A", method="invalid") 