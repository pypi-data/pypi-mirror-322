.. _`Installing IMAS-Python`:

Installing IMAS-Python
======================

IMAS-Python is a pure Python package. For full functionality of the package you need
an installation of `the IMAS Core library <https://imas.iter.org/>`_. See
:ref:`IMAS-Python 5 minute introduction` for an overview of functionality which does
(not) require the IMAS Core library available.

To get started, you can install it from `pypi.org <https://pypi.org/project/IMAS-Python>`_:

.. code-block:: bash

    pip install IMAS-Python


Local installation from sources
-------------------------------

We recommend using a :external:py:mod:`venv`. Then, clone the IMAS-Python repository
and run `pip install`:

.. code-block:: bash

    python3 -m venv ./venv
    . venv/bin/activate
    
    git clone ssh://git@github.com:iterorganization/IMAS-Python.git
    cd imas
    pip install --upgrade pip
    pip install --upgrade wheel setuptools
    pip install .


Development installation
------------------------

For development an installation in editable mode may be more convenient, and you
will need some extra dependencies to run the test suite and build documentation.

.. code-block:: bash

    pip install -e .[test,docs]

Test your installation by trying

.. code-block:: bash

    cd ~
    python -c "import imas; print(imas.__version__)"

This is how to run the IMAS-Python test suite:

.. code-block:: bash

    # inside the IMAS-Python git repository
    pytest imas --mini

    # run with a specific backend
    pytest imas --ascii --mini

And to build the IMAS-Python documentation, execute:

.. code-block:: bash

    make -C docs html


