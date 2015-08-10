=======
Decorum
=======

.. image:: https://travis-ci.org/zeekay/decorum.png?branch=master
    :target: https://travis-ci.org/zeekay/decorum

Decorum is a library which aims to make it easier to write flexible and simple
decorators:

* use decorators just like you need: don't bother with parentheses, pass
  options when you need them.

* write decorators just like you think: they get initialized with or without
  options, they wrap a function, they are callables.

* test decorators: it's really easy, you have no excuse!


Inherit from Decorum
====================

In order to write your own decorators, just subclass ``decorum.Decorum``:

.. code:: pycon

   >>> from decorum import Decorum

   >>> class empty_decorator(Decorum):
   ...     """Just inherit from Decorum's builtins."""

Of course you will want to customize decorator's behaviour! There are only
three methods to be aware of:

* ``init()`` setups the decorator itself;

* ``wraps()`` decorates the function;

* ``call()`` runs the wrapped function and returns result.

Here is a simple decorator to illustrate Decorum usage:

.. code:: pycon

   >>> from __future__ import print_function

   >>> class verbose_decorator(Decorum):
   ...    """Print info about decoration process."""
   ...    def init(self, *args, **kwargs):
   ...        print('Initializing decorator with args={} and kwargs={}'
   ...              .format(args, kwargs))
   ...        return super(verbose_decorator, self).init(*args, **kwargs)
   ...
   ...    def wraps(self, f):
   ...        print('Wrapping function "{}"'.format(f.__name__))
   ...        return super(verbose_decorator, self).wraps(f)
   ...
   ...    def call(self, *args, **kwargs):
   ...        print('Running wrapped function with args={} and kwargs={}'
   ...              .format(args, kwargs))
   ...        return super(verbose_decorator, self).call(*args, **kwargs)

Then you can use it as any decorator:

.. code:: pycon

   >>> @verbose_decorator
   ... def foo(x):
   ...     print(x)
   Initializing decorator with args=() and kwargs={}
   Wrapping function "foo"

   >>> foo('bar')
   Running wrapped function with args=('bar',) and kwargs={}
   bar

.. note::

   You can also use ``decorum.decorator`` to turn classes into decorators.

   .. code:: pycon

      >>> from decorum import decorator

      >>> @decorator
      ... class noop:
      ...     """Override init(), wraps() or call() if you like."""

      >>> @noop
      ... def foo():
      ...     """Do nothing."""

   The result is a class that inherits from the original class and Decorum:

   .. code:: pycon

      >>> isinstance(foo, noop)
      True
      >>> isinstance(foo, Decorum)
      True


Don't bother with parentheses
=============================

Decorum lets you write decorators with and without arguments in a unified way.
Then your decorator can be used with or without arguments, called or not, and
it will work the same way:

.. code:: pycon

   >>> @verbose_decorator
   ... def foo(x):
   ...     print(x)
   Initializing decorator with args=() and kwargs={}
   Wrapping function "foo"

Is identical to:

.. code:: pycon

   >>> @verbose_decorator()
   ... def foo(x):
   ...     print(x)
   Initializing decorator with args=() and kwargs={}
   Wrapping function "foo"


Initialize decorator with options
=================================

To implement a decorator that accepts a custom options, just change ``init()``:

.. code:: pycon

   >>> class configurable_decorator(Decorum):
   ...    def init(self, custom_option='default', *args, **kwargs):
   ...        print('Initializing decorator with custom_option="{}"'
   ...              .format(custom_option))
   ...        # Remember the option, typically for use in wraps() or call().
   ...        self.custom_option = custom_option
   ...        # Call super().init() with remaining arguments.
   ...        return super(configurable_decorator, self).init(*args, **kwargs)

As we used a keyword argument, it is optional:

.. code:: pycon

   >>> @configurable_decorator
   ... def foo(x):
   ...     print(x)
   Initializing decorator with custom_option="default"

   >>> foo.custom_option
   'default'

And we can pass this option when decorating a function. Either as positional
argument...

.. code:: pycon

   >>> @configurable_decorator('positional')
   ... def foo(x):
   ...     print(x)
   Initializing decorator with custom_option="positional"

   >>> foo.custom_option
   'positional'

... or keyword argument:

.. code:: pycon

   >>> @configurable_decorator(custom_option='keyword')
   ... def foo(x):
   ...     print(x)
   Initializing decorator with custom_option="keyword"

   >>> foo.custom_option
   'keyword'

Of course, you cannot pass arguments that are not declared as ``init()``
options:

.. code:: pycon

   >>> @configurable_decorator(wrong_option=True)  # doctest: +ELLIPSIS
   ... def foo(x):
   ...     print(x)
   Traceback (most recent call last):
     ...
   TypeError: init() got an unexpected keyword argument 'wrong_option'

.. note::

   In most cases, ``init()`` should accept additional arguments and and proxy
   them to parent via ``super(...).init(*args, **kwargs)``. This way, options
   of ancestor classes are supported.

   As an example, ``Decorum`` base class declares ``assigned`` keyword argument
   in ``init()`` (see section `wrap function <#wrap-function>`_ below).


Wrap function
=============

The ``wraps()`` method allows you to handle the decorated function. It receives
the function to decorate as single positional argument, and returns a callable
(typically ``self``).

In most cases, ``wraps()`` function will ``return super(..., self).wraps(f)``.

By default, the base ``Decorum.wraps()`` will try to keep assign certain
attributes to the wrapped function for you, namely ``__doc__`` and
``__name__``. This feature uses ``functools.wraps``.

.. code:: pycon

   >>> class identity(Decorum):
   ...     """Noop decorator: does nothing!"""

   >>> @identity
   ... def my_function():
   ...     """My function's docstring."""

   >>> print(my_function.__name__)
   my_function
   >>> print(my_function.__doc__)
   My function's docstring.

The optional ``assigned`` keyword argument can be used to specify which
attributes of the original function are assigned directly to the matching
attributes on the wrapper function. This defaults to
``functools.WRAPPER_ASSIGNMENTS``. You can specify ``False`` or ``None`` to
disable this.

.. code:: pycon

   >>> @identity(assigned=None)
   ... def my_function():
   ...     """My function's docstring."""

   >>> print(my_function.__name__)
   identity
   >>> print(my_function.__doc__)
   Noop decorator: does nothing!


Run decorated function
======================

``Decorum.call()`` method receives ``*args`` and ``**kwargs`` as input. It runs
the wrapped function, and returns the result.

Here is a simple decorator that repeats the result of decorated function:

.. code:: pycon

   >>> class repeat(Decorum):
   ...     def call(self, *args, **kwargs):
   ...         result = super(repeat, self).call(*args, **kwargs)
   ...         return ' '.join([result] * 2)

   >>> @repeat
   ... def parrot(word):
   ...     return word

   >>> parrot('hello')
   'hello hello'


Test decorators
===============

Decorum makes it easy to test custom decorators.

Assert a decorator has expected behaviour
-----------------------------------------

Decorators are defined as classes, so you have fine-grained control over what
you test. And your tests can focus on what you customized.

Let's check ``repeat`` decorator from the section before. Since we just
overrode ``call()``, let's focus on it:

.. code:: pycon

   >>> decorator = repeat(lambda x: x.upper())

   >>> result = decorator.call('input')
   >>> assert result == 'INPUT INPUT'

That's quite useful to unit test decorators.


Assert a function has been decorated
------------------------------------

Decorators are instances of ``Decorum`` or subclasses. So you can inspect
decorated functions.

Let's inspect ``my_function`` from the examples above:

.. code:: pycon

   >>> assert isinstance(my_function, Decorum)
   >>> assert isinstance(my_function, identity)


Known limitations
=================

Decorum has little known limitations:

* your decorator's ``init()`` cannot receive a single positional argument that
  is a callable. Decorum will try trigger ``wraps()`` instead of ``init()`` in
  such a case.


About
=====

Decorum project is free software, published under MIT license.

* PyPI: https://pypi.python.org/pypi/Decorum
* Code repository: https://github.com/zeekay/decorum
* Bugtracker: https://github.com/zeekay/decorum/issues
* Continuous integration: https://travis-ci.org/zeekay/decorum
