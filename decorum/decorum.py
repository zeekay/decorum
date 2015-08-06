from __future__ import print_function
import functools


class Decorum(object):
    """Decorator class that simplifies writing and testing decorators."""

    def __init__(self, *args, **kwargs):
        """
        Unifies decorator interface, so that it can be used
        both with and without arguments the same way.

        >>> decor = Decorum()
        >>> decor.assigned == functools.WRAPPER_ASSIGNMENTS
        True
        >>> decor = Decorum(assigned=None)
        >>> bool(decor.assigned)
        False

        """
        #: Wrapped function.
        self._wrapped = None

        #: Function name. Can be overriden with decorated function name,
        #: depending on values of :py:attr:`assigned`.
        self.__name__ = self.__class__.__name__

        #: Specify which attributes of the original function are assigned
        #: directly to the matching attributes on the decorator.
        self.assigned = functools.WRAPPER_ASSIGNMENTS
        if 'assigned' in kwargs:
            self.assigned = kwargs.pop('assigned')

        if args and callable(args[0]):
            # used as decorator without being called
            self.init()
            self.wraps(args[0])
        else:
            # used as decorator and called
            self.init(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        """Actually run the decorated function.

        Uses :meth:`wrap` to handle decoration. Restores :attr:`__doc__` and
        :attr:`__name__`.

        """
        if self._wrapped:
            return self.call(*args, **kwargs)
        else:
            f = args[0]
            return self.wraps(f)

    def wraps(self, f):
        """Wraps the function and returns it"""
        self._wrapped = f
        functools.update_wrapper(self, f, self.assigned or (), ())
        return self

    def init(self):
        """Passed any possible arguments to decorator"""

    def call(self, *args, **kwargs):
        return self._wrapped(*args, **kwargs)


def decorator(cls):
    class decorated(cls, Decorum):
        def __init__(self, *args, **kwargs):
            Decorum.__init__(self, *args, **kwargs)
            for attribute in functools.WRAPPER_ASSIGNMENTS:
                if not self.assigned or attribute not in self.assigned:
                    try:
                        setattr(self, attribute, getattr(cls, attribute))
                    except AttributeError:
                        pass
    return decorated
