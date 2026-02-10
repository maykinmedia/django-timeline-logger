.. _contributing:

============
Contributing
============

To get up and running quickly, fork the github repository and make all
your changes in your local clone.

Pull requests must be made against the ``main`` branch and should always have tests,
and if relevant, documentation updates.

Feel free to create unfinished pull-requests to get the tests to build
and get work going, someone else might always want to pick up the tests
and/or documentation.

Testing
=======

To run the tests in your (virtual) environment, execute

.. code-block:: sh

    pytest

This will run the tests with the current python version and Django version
installed in your virtual environment.

To run the tests on all supported python/Django versions, use tox_.

.. code-block:: sh

    uv pip install tox
    tox

Documentation
=============

The documentation is built with Sphinx. Use ``make`` to build the documentation:

.. code-block:: sh

    cd docs/
    make html

You can now open ``_build/index.html``.


Coding style
============

In general, we adhere to Django's coding style. Additionally, code is formatted and
linted with Ruff_.

.. _tox: https://tox.readthedocs.io/en/latest/
.. _Ruff: https://docs.astral.sh/ruff/
