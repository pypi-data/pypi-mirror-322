Installation Guide
=================

Requirements
-----------

DataLib requires Python 3.8 or later. The package has the following dependencies:

* numpy
* pandas
* matplotlib
* scikit-learn
* scipy
* seaborn

Installing with pip
------------------

The easiest way to install DataLib is using pip:

.. code-block:: bash

   pip install datalib

This will automatically install DataLib and all its dependencies.

Installing from source
--------------------

To install DataLib from source, first clone the repository:

.. code-block:: bash

   git clone https://github.com/yourusername/datalib.git
   cd datalib
   pip install -e .

Development installation
----------------------

If you want to contribute to DataLib, you can install it with development dependencies:

.. code-block:: bash

   pip install -e ".[test,doc]"

This will install additional packages needed for testing and building documentation:

* pytest
* pytest-cov
* sphinx
* sphinx-rtd-theme 