#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Python packaging."""
import os
import sys

from setuptools import setup


#: Absolute path to directory containing setup.py file.
here = os.path.abspath(os.path.dirname(__file__))
#: Boolean, ``True`` if environment is running Python version 2.
IS_PYTHON2 = sys.version_info[0] == 2


# Data for use in setup.
NAME = 'Decorum'
DESCRIPTION = 'Tool for writing simple decorators.'
README = open(os.path.join(here, 'README.rst')).read()
AUTHOR = u'Zach Kelling'
EMAIL = 'zk@monoid.io'
LICENSE = 'MIT'
URL = 'https://pypi.python.org/pypi/{name}'.format(name=NAME)
CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'License :: OSI Approved :: MIT License',
    'Intended Audience :: Developers',
]
KEYWORDS = [
    'decorator',
    'decorators',
]
PACKAGES = ['decorum']
REQUIREMENTS = []
SETUP_REQUIREMENTS = [
    'setuptools',
]
ENTRY_POINTS = {}


if __name__ == '__main__':  # Don't run setup() when we import this module.
    setup(
        author=AUTHOR,
        author_email=EMAIL,
        classifiers=CLASSIFIERS,
        description=DESCRIPTION,
        entry_points=ENTRY_POINTS,
        include_package_data=True,
        install_requires=REQUIREMENTS,
        keywords=' '.join(KEYWORDS),
        license=LICENSE,
        long_description=README,
        name=NAME,
        packages=PACKAGES,
        setup_requires=SETUP_REQUIREMENTS,
        url=URL,
        version='1.0.1.dev0',
        zip_safe=False,
    )
