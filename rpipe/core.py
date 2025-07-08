"""Core implementation of the rpipe functionality."""

import toolz


class PipeClass:
    """A class that enables R-like piping using the >> operator."""

    def __init__(self, *funcs):
        self.funcs = funcs

    def __call__(self, *args):
        if not args:
            # P() case - return self to handle >> operator
            return self

        # Check if all arguments are callable (functions)
        if all(callable(arg) for arg in args):
            # Return a new PipeClass instance with these functions
            return PipeClass(*args)
        else:
            # If any argument is not callable, treat as data and pipe through
            return toolz.pipe(*args)

    def __rrshift__(self, other):
        # Handle the >> operator
        if isinstance(other, tuple):
            if len(other) == 0:
                # Empty tuple case
                return other
            elif len(other) == 1:
                # Single element tuple
                if self.funcs:
                    return toolz.pipe(other[0], *self.funcs)
                else:
                    return other[0]
            else:
                # Multiple elements tuple
                if self.funcs:
                    return toolz.pipe(*other, *self.funcs)
                else:
                    return toolz.pipe(*other)
        else:
            # Single value (not a tuple)
            if self.funcs:
                return toolz.pipe(other, *self.funcs)
            else:
                return other


# Create the P instance
P = PipeClass()
