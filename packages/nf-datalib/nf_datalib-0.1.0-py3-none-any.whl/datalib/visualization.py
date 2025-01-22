"""
Visualization module providing plotting and charting capabilities.
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Optional, Tuple, Union

def plot_histogram(
    data: pd.DataFrame,
    column: str,
    bins: int = 30,
    title: Optional[str] = None,
    figsize: Tuple[int, int] = (10, 6)
) -> plt.Figure:
    """
    Create a histogram for a numerical column.
    
    Args:
        data: Input DataFrame
        column: Name of the column to plot
        bins: Number of bins in histogram
        title: Plot title
        figsize: Figure size as (width, height)
        
    Returns:
        plt.Figure: The generated figure
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.hist(data[column], bins=bins, edgecolor='black')
    ax.set_xlabel(column)
    ax.set_ylabel('Frequency')
    ax.set_title(title or f'Histogram of {column}')
    return fig

def plot_scatter(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: Optional[str] = None,
    figsize: Tuple[int, int] = (10, 6)
) -> plt.Figure:
    """
    Create a scatter plot between two numerical columns.
    
    Args:
        data: Input DataFrame
        x_col: Name of the column for x-axis
        y_col: Name of the column for y-axis
        title: Plot title
        figsize: Figure size as (width, height)
        
    Returns:
        plt.Figure: The generated figure
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.scatter(data[x_col], data[y_col], alpha=0.5)
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title(title or f'Scatter Plot: {x_col} vs {y_col}')
    return fig

def plot_correlation_matrix(
    data: pd.DataFrame,
    figsize: Tuple[int, int] = (10, 8),
    cmap: str = 'coolwarm'
) -> plt.Figure:
    """
    Create a heatmap of correlation matrix.
    
    Args:
        data: Input DataFrame
        figsize: Figure size as (width, height)
        cmap: Color map for the heatmap
        
    Returns:
        plt.Figure: The generated figure
    """
    corr = data.select_dtypes(include=[np.number]).corr()
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(corr, annot=True, cmap=cmap, ax=ax)
    ax.set_title('Correlation Matrix')
    return fig

def plot_boxplot(
    data: pd.DataFrame,
    columns: Union[str, list[str]],
    figsize: Tuple[int, int] = (10, 6)
) -> plt.Figure:
    """
    Create box plots for one or more numerical columns.
    
    Args:
        data: Input DataFrame
        columns: Column name or list of column names
        figsize: Figure size as (width, height)
        
    Returns:
        plt.Figure: The generated figure
    """
    if isinstance(columns, str):
        columns = [columns]
    
    fig, ax = plt.subplots(figsize=figsize)
    data[columns].boxplot(ax=ax)
    ax.set_title('Box Plot')
    plt.xticks(rotation=45)
    return fig 