"""rpipe - R-like pipe functionality for Python using the >> operator."""

from .core import P, PipeClass
from toolz import pipe, thread_first as TF, thread_last as TL
from functools import partial

__version__ = "0.1.0"
__author__ = "Jim Java"
__email__ = "james.j.java@gmail.com"

__all__ = ["P", "PipeClass", "pipe", "TF", "TL", "partial"]
