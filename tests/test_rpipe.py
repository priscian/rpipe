"""Tests for rpipe functionality."""

import pytest
from rpipe import P
from functools import partial


class TestBasicPipe:
    """Test basic pipe functionality."""

    def test_p_function_call(self):
        """Test P(exp1, exp2, ...) syntax."""
        result = P(range(0, 4), list)
        assert result == [0, 1, 2, 3]

    def test_tuple_pipe(self):
        """Test (exp1, exp2) >> P syntax."""
        result = (range(0, 4), list) >> P
        assert result == [0, 1, 2, 3]

        result = (range(0, 4), list) >> P()
        assert result == [0, 1, 2, 3]

    def test_single_value_pipe(self):
        """Test single value >> P syntax."""
        result = range(0, 4) >> P
        assert list(result) == [0, 1, 2, 3]

        result = range(0, 4) >> P()
        assert list(result) == [0, 1, 2, 3]

    def test_single_element_tuple(self):
        """Test single element tuple variations."""
        result = (range(0, 4)) >> P
        assert list(result) == [0, 1, 2, 3]

        result = (range(0, 4), ) >> P
        assert list(result) == [0, 1, 2, 3]

    def test_pipe_with_functions(self):
        """Test piping with functions."""
        result = (range(0, 4)) >> P(list)
        assert result == [0, 1, 2, 3]

        result = (range(0, 4), ) >> P(list)
        assert result == [0, 1, 2, 3]

    def test_chained_functions(self):
        """Test chaining multiple functions."""
        result = (range(0, 4), list) >> P(len)
        assert result == 4

        # Test with print (capture output)
        result = (range(0, 4), list) >> P(len, str)
        assert result == "4"


class TestAdvancedPipe:
    """Test advanced pipe functionality."""

    def test_complex_pipeline(self):
        """Test complex data transformations."""
        result = range(10) >> P(
            list,
            lambda x: [i**2 for i in x],
            sum
        )
        assert result == 285

    def test_string_operations(self):
        """Test string manipulation in pipes."""
        result = "hello world" >> P(str.upper, str.split, len)
        assert result == 2

    def test_with_partial(self):
        """Test integration with functools.partial."""
        multiply_by = lambda x, y: x * y
        double = partial(multiply_by, 2)
        triple = partial(multiply_by, 3)

        result = 5 >> P(double, triple)
        assert result == 30

    def test_filter_map_operations(self):
        """Test with filter and map."""
        is_even = lambda x: x % 2 == 0
        filter_even = partial(filter, is_even)
        map_square = partial(map, lambda x: x**2)

        result = range(10) >> P(filter_even, map_square, list)
        assert result == [0, 4, 16, 36, 64]

    def test_empty_tuple(self):
        """Test empty tuple handling."""
        result = () >> P
        assert result == ()

        result = () >> P()
        assert result == ()


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_none_value(self):
        """Test piping None."""
        result = None >> P
        assert result is None

        result = None >> P(lambda x: x or "default")
        assert result == "default"

    def test_empty_list(self):
        """Test piping empty list."""
        result = [] >> P(len)
        assert result == 0

    def test_nested_pipes(self):
        """Test nested pipe operations."""
        add_one = lambda x: x + 1
        double = lambda x: x * 2

        pipeline1 = P(add_one, double)
        pipeline2 = P(pipeline1, str)

        result = 5 >> pipeline2
        assert result == "12"


if __name__ == "__main__":
    pytest.main([__file__])
