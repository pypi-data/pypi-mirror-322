"""
Tests for the machine learning module.
"""

import pytest
import pandas as pd
import numpy as np
from datalib.ml import RegressionModel, ClassificationModel, prepare_data

@pytest.fixture
def regression_data():
    """Create sample regression data"""
    np.random.seed(42)
    X = np.random.normal(0, 1, (100, 2))
    y = 2 * X[:, 0] + 3 * X[:, 1] + np.random.normal(0, 0.1, 100)
    return pd.DataFrame(X, columns=["X1", "X2"]), pd.Series(y, name="target")

@pytest.fixture
def classification_data():
    """Create sample classification data"""
    np.random.seed(42)
    X = np.random.normal(0, 1, (100, 2))
    y = (X[:, 0] + X[:, 1] > 0).astype(int)
    return pd.DataFrame(X, columns=["X1", "X2"]), pd.Series(y, name="target")

def test_regression_model(regression_data):
    """Test regression model functionality"""
    X, y = regression_data
    model = RegressionModel()
    
    # Test fitting
    model.fit(X, y)
    assert model.is_fitted
    
    # Test prediction
    predictions = model.predict(X)
    assert len(predictions) == len(y)
    
    # Test evaluation
    metrics = model.evaluate(X, y)
    assert "mse" in metrics
    assert "rmse" in metrics
    assert "r2" in metrics
    assert 0 <= metrics["r2"] <= 1

def test_classification_model(classification_data):
    """Test classification model functionality"""
    X, y = classification_data
    
    for model_type in ["logistic", "decision_tree", "knn"]:
        model = ClassificationModel(model_type=model_type)
        
        # Test fitting
        model.fit(X, y)
        assert model.is_fitted
        
        # Test prediction
        predictions = model.predict(X)
        assert len(predictions) == len(y)
        assert set(predictions).issubset({0, 1})
        
        # Test probability prediction
        probas = model.predict_proba(X)
        assert probas.shape == (len(y), 2)
        assert np.all((0 <= probas) & (probas <= 1))
        
        # Test evaluation
        metrics = model.evaluate(X, y)
        assert "accuracy" in metrics
        assert "classification_report" in metrics
        assert 0 <= metrics["accuracy"] <= 1

def test_prepare_data(regression_data):
    """Test data preparation functionality"""
    X, y = regression_data
    data = X.copy()
    data["target"] = y
    
    # Test with default parameters
    X_train, X_test, y_train, y_test = prepare_data(data, "target")
    assert len(X_train) > len(X_test)
    assert len(y_train) == len(X_train)
    assert len(y_test) == len(X_test)
    
    # Test with custom feature list
    features = ["X1"]
    X_train, X_test, y_train, y_test = prepare_data(data, "target", features=features)
    assert list(X_train.columns) == features

def test_invalid_model_type():
    """Test error handling for invalid model type"""
    with pytest.raises(ValueError):
        ClassificationModel(model_type="invalid_type")

def test_predict_before_fit(regression_data):
    """Test error handling when predicting before fitting"""
    X, y = regression_data
    model = RegressionModel()
    
    with pytest.raises(ValueError):
        model.predict(X) 