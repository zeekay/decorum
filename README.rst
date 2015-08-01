=======
Decorum
=======

.. image:: https://travis-ci.org/zeekay/decorum.png?branch=master
    :target: https://travis-ci.org/zeekay/decorum

Decorum is a simple tool which aims to make it easier to write flexible
and simple decorators. It can also act similarly to ``functools.wraps``.

Typical usage looks like this:

.. code:: pycon

   >>> from __future__ import print_function
   >>> from decorum import decorator

   >>> @decorator
   ... class my_decorator:
   ...    def wraps(self, f):
   ...        print("I'm returning the function! You can keep it!")
   ...        return f

Decorum lets you write decorators with and without arguments in a unified way.
Your decorator can be used with or without arguments, called or not, and it
will work the same way:

.. code:: pycon

   >>> @my_decorator
   ... def foo(x):
   ...     print(x)
   I'm returning the function! You can keep it!

   >>> foo('bar')
   bar

Is identical to:

.. code:: pycon

   >>> @my_decorator()
   ... def foo(x):
   ...     print(x)
   I'm returning the function! You can keep it!


Writing decorators
==================

Decorum provides two easy ways to write your own decorators. You can use
``decorum.decorator`` to decorate decorator classes, or you can directly
subclass decorum.Decorum. There are only two methods to be aware of when
writing your own decorators. Define a ``wraps`` method to handle the actual
decoration and return the decorated function, and optionally define an ``init``
method to handle any arguments you want to accept, and handle basic setup (it's
called before decoration by ``__init__``, you can use it in a similar fashion
to a real ``__init__`` method).

Here is a slightly fancier example:

.. code:: pycon

   >>> from decorum import decorator

   >>> @decorator
   ... class fancy:
   ...     def init(self, arg=None):
   ...         self.arg = arg
   ...
   ...     def wraps(self, f):
   ...         if self.arg:
   ...             def newf():
   ...                 print(self.arg)
   ...         else:
   ...             def newf():
   ...                 print('wut')
   ...         return newf

   >>> @fancy
   ... def foo():
   ...     pass

   >>> foo()
   wut

   >>> @fancy('woof')
   ... def foo():
   ...     pass

   >>> foo()
   woof

By default decorum will try to keep assign
certain attributes to the wrapped function for you, namely ``__doc__`` and
``__name__``.

.. code:: pycon

   >>> import decorum

   >>> @decorum.decorator
   ... class identity(object):
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
``functools.WRAPPER_ASSIGNMENTS``. You can specify ``False`` or ``None``
to disable this.

Also the optional ``updated`` keyword argument can be used to specify which
attributes of the decorator are updated with the corresponding attributes from
the original function. This defaults to ``functools.WRAPPER_UPDATES``.
You can specify ``False`` or ``None`` to disable this.


.. code:: pycon

   >>> @identity(assigned=None, updated=None)
   ... def my_function():
   ...     """My function's docstring."""
   >>> print(my_function.__name__)
   identity
   >>> print(my_function.__doc__)
   Noop decorator: does nothing!
