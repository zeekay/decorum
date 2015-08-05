from __future__ import print_function
import functools
import warnings


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
        #: Function name. Can be overriden with decorated function name,
        #: depending on values of :py:attr:`assigned`.
        self.__name__ = self.__class__.__name__

        #: Specify which attributes of the original function are assigned
        #: directly to the matching attributes on the decorator.
        self.assigned = functools.WRAPPER_ASSIGNMENTS
        if 'assigned' in kwargs:
            self.assigned = kwargs['assigned']

        if args and callable(args[0]):
            # used as decorator without being called
            self.init()
            self._wrapped = self.__call__(args[0])
        else:
            # used as decorator and called
            self.init(*args, **kwargs)

    def __call__(self, f=None, *args, **kwargs):
        """Actually run the decorated function.

        Uses :meth:`wrap` to handle decoration. Restores :attr:`__doc__` and
        :attr:`__name__`.

        """
        if not callable(f):
            if f:
                return self._wrapped(f, *args, **kwargs)
            else:
                return self._wrapped(*args, **kwargs)
        else:
            wrapped = self.wraps(f)
            return wrapped

    def wraps(self, f):
        """Wraps the function and returns it"""
        functools.update_wrapper(self, f, self.assigned or (), ())
        return self

    def init(self, *args, **kwargs):
        """Passed any possible arguments to decorator"""
        pass


def decorator(cls):
    warnings.warn("decorum.decorator() will be deprecated. "
                  "Subclass decorum.Decorum instead of decorating classes.",
                  PendingDeprecationWarning)

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
