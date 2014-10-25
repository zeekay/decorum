from distutils.core import setup

setup(
    name='Decorum',
    version='0.5.1',
    author='Zach Kelling',
    author_email='zk@monoid.io',
    packages=['decorum'],
    license='MIT',
    description='Tool for writing simple decorators',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',

        'License :: OSI Approved :: MIT License',
    ],
    keywords='decorator decorators',
)
