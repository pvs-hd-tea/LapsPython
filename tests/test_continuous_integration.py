"""Unit tests for module dummy.continuous_integration."""

import pytest

from dummy.continuous_integration import dummy_function, factorial


class TestFactorial:
    """Run tests for dummy.continuous_integration.factorial(int)."""

    def test_base_case(self):
        """starting_value is 0 or 1."""
        assert factorial(0) == 0
        assert factorial(1) == 1

    def test_samples(self):
        """starting_value is an integer greater than 1."""
        assert factorial(2) == 2
        assert factorial(3) == 6
        assert factorial(4) == 24
        assert factorial(5) == 120

    def test_invalid_type(self):
        """starting_value is not int."""
        expected_message = 'starting_value must be a positive integer.'
        with pytest.raises(TypeError, match=expected_message):
            factorial(float)

    def test_invalid_value(self):
        """starting_value is a negative integer."""
        expected_message = 'starting_value must be a positive integer.'
        with pytest.raises(ValueError, match=expected_message):
            factorial(-1)


class TestDummyFunction:
    """Run tests for dummy.continuous_integration.dummy_function(int)."""

    def test_positive(self):
        """n_values is a positive integer."""
        for i in range(1, 11):
            assert dummy_function(i)

    def test_zero(self):
        """n_values is 0."""
        assert dummy_function(0)

    def test_negative(self):
        """n_values is a negative integer."""
        for i in range(-1, -11, -1):
            assert dummy_function(i)

    def test_invalid_type(self):
        """n_values is not int."""
        expected_message = 'n_values must be an integer.'
        with pytest.raises(TypeError, match=expected_message):
            dummy_function(float)
