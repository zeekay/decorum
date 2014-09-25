import os

import doctest

here = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(here)


def test_doctests():
    doctest.testfile('../README.rst')
