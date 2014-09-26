from distutils.core import setup

setup(
    name='Decorum',
    version='0.5.0',
    author='Zach Kelling',
    author_email='zk@monoid.io',
    packages=['decorum'],
    license='LICENSE',
    description='Tool for writing simple decorators',
    long_description=open('README.rst').read(),
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
