Getting Started
===============

.. _demo:

1-Click-Demo
------------

Requirements: `Conda <https://docs.conda.io/en/latest/>`_ (or equivalent), bash

.. code-block:: console

   $ bash 1-click-demo.sh

This serves as a setup script that also runs the main functionality of LapsPython in a virtual environment. It executes the following steps:

#. Create and activate a Conda environment **lapspython** running on Python 3.7
#. Install all LAPS requirements and used dev packages in a local Pipenv environment
#. Run CI scripts (see Section :ref:`Continuous Integration <ci>` for detailed information)

   * Linting
   
   * Static Typechecking
   
   * Unit Tests (generating coverage report in `LapsPython/coverage/index.html <../../../coverage/index.html>`_)
   
#. Run a demo program launching the LapsPython pipeline for LAPS checkpoints in the **re2** domain in Python mode and in R mode

Section :ref:`Manual Installation <installation>` describes this process as well as design decisions in more detail. Delete the Pipenv environment (~1.8 GB) by removing the contents of **LapsPython/.venv/**. Delete the Conda environment (~218 MB) by running 

.. code-block:: console

   $ conda env remove --name lapspython


.. _installation:

Manual Installation
-------------------

If you do not want to use the recommended demo script, you can install the requirements manually in a **Python 3.7** environment of your choice (here: **lapspython**):

.. code-block:: console

   (lapspython) $ git submodule init
   (lapspython) $ git submodule update
   (lapspython) $ conda install swig pipenv
   (lapspython) $ pipenv sync

The **pipenv sync** command installs all Python modules required by **LAPS** locally in **LapsPython/.venv/**, as well as `uniplot <https://pypi.org/project/uniplot/>`_ and the dev packages used in Section :ref:`Continuous Integration <ci>`.

The demo program can then be run through Pipenv:

.. code-block:: console

   (lapspython) $ pipenv run demo.py
   
Using Pipenv is recommended and the only verified way to get LapsPython running, since the portable **Pipfile.lock** allows to reproduce the exact virtual environment used on my Ubuntu 20.04 machine. If you do not want to use Pipenv, **requirements.txt** and **requirements-dev.txt** are provided and can be installed by running

.. code-block:: console

   (lapspython) $ pip install -r requirements.txt
   (lapspython) $ pip install -r requirements-dev.txt
   
If you do not want to use Conda, **swig** needs to be installed through a package manger such as **apt-get**, which might require superuser rights.
   
.. _ci:

Continuous Integration
----------------------

You can run the following Pipenv scripts to execute the CI workflows also used by Github upon pushs and pull requests.

.. code-block:: console

   (lapspython) $ pipenv run tests

This script runs unit tests implemented with `pytest <https://docs.pytest.org/en/7.1.x/>`_. In addition, it uses `pytest-cov <https://pytest-cov.readthedocs.io/en/latest/>`_ to generate a coverage report which will then be printed to the terminal and stored as HTML in `LapsPython/coverage/index.html <../../../coverage/index.html>`_.


.. code-block:: console

   (lapspython) $ pipenv run typechecks

This script runs static typechecks using `Mypy <http://www.mypy-lang.org/>`_.


.. code-block:: console

   (lapspython) $ pipenv run linting

This script runs the PEP-8 compliant linter `Flake8 <https://flake8.pycqa.org/en/latest/>`_ with a large selection of extensions enforcing stricter conventions in compliance with modern Python standards, simplifying complex code, as well as preventing bugs and security issues.
