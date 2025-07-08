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
                    return self._apply_funcs(other[0])
                else:
                    return other[0]
            else:
                # Multiple elements tuple
                if self.funcs:
                    return self._apply_funcs(toolz.pipe(*other))
                else:
                    return toolz.pipe(*other)
        else:
            # Single value (not a tuple)
            if self.funcs:
                return self._apply_funcs(other)
            else:
                return other

    def _apply_funcs(self, data):
        """Apply the stored functions to data, handling nested PipeClass instances."""
        result = data
        for func in self.funcs:
            if isinstance(func, PipeClass):
                # If it's a PipeClass, apply its functions
                result = func._apply_funcs(result)
            else:
                # Regular function
                result = func(result)
        return result


# Create the P instance
P = PipeClass()
