"""
Machine learning module providing regression and classification capabilities.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    mean_squared_error,
    r2_score,
    accuracy_score,
    classification_report
)
from typing import Union, Optional, Tuple, Dict

class RegressionModel:
    """Base class for regression models."""
    
    def __init__(self, model_type: str = "linear"):
        """
        Initialize regression model.
        
        Args:
            model_type: Type of regression model ("linear" or "polynomial")
        """
        self.model_type = model_type
        self.model = LinearRegression()
        self.is_fitted = False
    
    def fit(self, X: Union[pd.DataFrame, np.ndarray], y: Union[pd.Series, np.ndarray]) -> None:
        """
        Fit the regression model.
        
        Args:
            X: Features
            y: Target variable
        """
        self.model.fit(X, y)
        self.is_fitted = True
    
    def predict(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """
        Make predictions using the fitted model.
        
        Args:
            X: Features to predict
            
        Returns:
            np.ndarray: Predicted values
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before making predictions")
        return self.model.predict(X)
    
    def evaluate(self, X: Union[pd.DataFrame, np.ndarray], y: Union[pd.Series, np.ndarray]) -> Dict[str, float]:
        """
        Evaluate model performance.
        
        Args:
            X: Features
            y: True target values
            
        Returns:
            Dict[str, float]: Dictionary containing evaluation metrics
        """
        predictions = self.predict(X)
        return {
            "mse": mean_squared_error(y, predictions),
            "rmse": np.sqrt(mean_squared_error(y, predictions)),
            "r2": r2_score(y, predictions)
        }

class ClassificationModel:
    """Base class for classification models."""
    
    def __init__(self, model_type: str = "logistic"):
        """
        Initialize classification model.
        
        Args:
            model_type: Type of classifier ("logistic", "decision_tree", or "knn")
        """
        self.model_type = model_type
        if model_type == "logistic":
            self.model = LogisticRegression()
        elif model_type == "decision_tree":
            self.model = DecisionTreeClassifier()
        elif model_type == "knn":
            self.model = KNeighborsClassifier()
        else:
            raise ValueError("Unsupported model type")
        self.is_fitted = False
    
    def fit(self, X: Union[pd.DataFrame, np.ndarray], y: Union[pd.Series, np.ndarray]) -> None:
        """
        Fit the classification model.
        
        Args:
            X: Features
            y: Target classes
        """
        self.model.fit(X, y)
        self.is_fitted = True
    
    def predict(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """
        Make predictions using the fitted model.
        
        Args:
            X: Features to predict
            
        Returns:
            np.ndarray: Predicted classes
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before making predictions")
        return self.model.predict(X)
    
    def predict_proba(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """
        Get probability estimates for each class.
        
        Args:
            X: Features to predict
            
        Returns:
            np.ndarray: Probability estimates
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before making predictions")
        return self.model.predict_proba(X)
    
    def evaluate(self, X: Union[pd.DataFrame, np.ndarray], y: Union[pd.Series, np.ndarray]) -> Dict[str, float]:
        """
        Evaluate model performance.
        
        Args:
            X: Features
            y: True classes
            
        Returns:
            Dict[str, float]: Dictionary containing evaluation metrics
        """
        predictions = self.predict(X)
        return {
            "accuracy": accuracy_score(y, predictions),
            "classification_report": classification_report(y, predictions)
        }

def prepare_data(
    data: pd.DataFrame,
    target: str,
    features: Optional[list[str]] = None,
    test_size: float = 0.2,
    random_state: Optional[int] = None
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Prepare data for machine learning by splitting into train and test sets.
    
    Args:
        data: Input DataFrame
        target: Name of target column
        features: List of feature columns (if None, use all except target)
        test_size: Proportion of data to use for testing
        random_state: Random seed for reproducibility
        
    Returns:
        Tuple containing X_train, X_test, y_train, y_test
    """
    if features is None:
        features = [col for col in data.columns if col != target]
    
    X = data[features]
    y = data[target]
    
    return train_test_split(X, y, test_size=test_size, random_state=random_state) 