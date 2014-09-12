from distutils.core import setup

setup(
    name='Decorum',
    version='0.4.2',
    author='Zach Kelling',
    author_email='zk@monoid.io',
    packages=['decorum',],
    license='LICENSE',
    description='Tool for writing simple decorators',
    long_description=open('README.rst').read(),
)
