from __future__ import print_function


class Decorum(object):
    """Decorator class that simplifies writing and testing decorators."""

    def __init__(self, *args, **kwargs):
        """
        Unifies decorator interface, so that it can be used
        both with and without arguments the same way.

        >>> decor = Decorum()
        >>> decor.assigned
        ('__doc__', '__name__')
        >>> decor = Decorum(assigned=None)
        >>> bool(decor.assigned)
        False

        """
        self.assigned = ('__doc__', '__name__')
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
            if self.assigned:
                for attr in self.assigned:
                    try:
                        setattr(wrapped, attr, getattr(f, attr))
                    except AttributeError:
                        print('oops')
                        pass
            return wrapped

    def wraps(self, f):
        """Wraps the function and returns it"""
        return f

    def init(self, *args, **kwargs):
        """Passed any possible arguments to decorator"""
        pass


def decorator(cls):
    class decorated(cls, Decorum):
        pass
    return decorated
