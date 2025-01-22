"""
Tests for the visualization module.
"""

import pytest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datalib.visualization import (
    plot_histogram,
    plot_scatter,
    plot_correlation_matrix,
    plot_boxplot
)

@pytest.fixture
def sample_data():
    """Create sample data for testing"""
    np.random.seed(42)
    return pd.DataFrame({
        "A": np.random.normal(0, 1, 100),
        "B": np.random.normal(2, 1.5, 100),
        "C": np.random.uniform(0, 10, 100)
    })

def test_plot_histogram(sample_data):
    """Test histogram plotting"""
    fig = plot_histogram(sample_data, "A")
    assert isinstance(fig, plt.Figure)
    plt.close(fig)

def test_plot_scatter(sample_data):
    """Test scatter plot"""
    fig = plot_scatter(sample_data, "A", "B")
    assert isinstance(fig, plt.Figure)
    plt.close(fig)

def test_plot_correlation_matrix(sample_data):
    """Test correlation matrix plot"""
    fig = plot_correlation_matrix(sample_data)
    assert isinstance(fig, plt.Figure)
    plt.close(fig)

def test_plot_boxplot_single(sample_data):
    """Test box plot with single column"""
    fig = plot_boxplot(sample_data, "A")
    assert isinstance(fig, plt.Figure)
    plt.close(fig)

def test_plot_boxplot_multiple(sample_data):
    """Test box plot with multiple columns"""
    fig = plot_boxplot(sample_data, ["A", "B", "C"])
    assert isinstance(fig, plt.Figure)
    plt.close(fig) 