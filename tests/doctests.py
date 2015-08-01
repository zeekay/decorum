import doctest


def test_readme():
    """README contains doctests, they all pass."""
    result = doctest.testfile('../README.rst')
    assert result.attempted != 0
    assert result.failed == 0
