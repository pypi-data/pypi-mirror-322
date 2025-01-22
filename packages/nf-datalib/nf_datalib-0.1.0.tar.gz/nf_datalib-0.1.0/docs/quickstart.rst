Quickstart Guide
===============

This guide will help you get started with DataLib's main features.

Data Manipulation
---------------

Reading and processing data:

.. code-block:: python

    import pandas as pd
    from datalib.data_manipulation import read_csv, normalize_column

    # Read data
    data = read_csv("data.csv")

    # Normalize a column
    normalized_data = normalize_column(data, "value", method="minmax")

Statistical Analysis
------------------

Performing basic statistical analysis:

.. code-block:: python

    from datalib.statistics import describe_column, correlation_analysis

    # Get basic statistics
    stats = describe_column(data, "value")
    print(f"Mean: {stats['mean']}")
    print(f"Median: {stats['median']}")
    print(f"Standard deviation: {stats['std']}")

    # Calculate correlations
    corr_matrix = correlation_analysis(data)

Data Visualization
----------------

Creating various plots:

.. code-block:: python

    from datalib.visualization import (
        plot_histogram,
        plot_scatter,
        plot_correlation_matrix
    )

    # Create a histogram
    fig = plot_histogram(data, "value")
    fig.savefig("histogram.png")

    # Create a scatter plot
    fig = plot_scatter(data, "x", "y")
    fig.savefig("scatter.png")

    # Create a correlation matrix heatmap
    fig = plot_correlation_matrix(data)
    fig.savefig("correlation.png")

Machine Learning
--------------

Training and evaluating models:

.. code-block:: python

    from datalib.ml import RegressionModel, ClassificationModel, prepare_data

    # Prepare data
    X_train, X_test, y_train, y_test = prepare_data(data, target="target")

    # Regression
    reg_model = RegressionModel()
    reg_model.fit(X_train, y_train)
    reg_metrics = reg_model.evaluate(X_test, y_test)
    print(f"R² score: {reg_metrics['r2']}")

    # Classification
    clf_model = ClassificationModel(model_type="logistic")
    clf_model.fit(X_train, y_train)
    clf_metrics = clf_model.evaluate(X_test, y_test)
    print(f"Accuracy: {clf_metrics['accuracy']}")

Next Steps
---------

* Check out the :doc:`api/index` for detailed documentation of all functions
* Look at :doc:`examples/index` for more complex examples
* Visit our GitHub repository for the latest updates 