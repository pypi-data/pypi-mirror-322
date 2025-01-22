"""
Tests for the statistics module.
"""

import pytest
import pandas as pd
import numpy as np
from datalib.statistics import describe_column, correlation_analysis, ttest_columns

def test_describe_column():
    """Test basic statistical measures calculation"""
    df = pd.DataFrame({"A": [1, 2, 2, 3, 4, 5]})
    stats = describe_column(df, "A")
    
    assert stats["mean"] == pytest.approx(2.833333, rel=1e-5)
    assert stats["median"] == 2.5
    assert stats["mode"] == 2
    assert stats["std"] == pytest.approx(1.471960, rel=1e-5)

def test_correlation_analysis():
    """Test correlation matrix calculation"""
    df = pd.DataFrame({
        "A": [1, 2, 3, 4, 5],
        "B": [2, 4, 6, 8, 10]  # Perfect positive correlation with A
    })
    corr = correlation_analysis(df)
    
    assert corr.loc["A", "B"] == pytest.approx(1.0)
    assert corr.loc["B", "A"] == pytest.approx(1.0)

def test_ttest_columns():
    """Test t-test between columns"""
    df = pd.DataFrame({
        "A": [1, 2, 3, 4, 5],
        "B": [1, 2, 3, 4, 5]  # Identical distribution
    })
    t_stat, p_value = ttest_columns(df, "A", "B")
    
    # For identical distributions, t-stat should be 0 and p-value should be 1
    assert t_stat == pytest.approx(0, abs=1e-10)
    assert p_value == pytest.approx(1.0) 