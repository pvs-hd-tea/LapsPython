"""Unit tests for module dummy.continuous_integration"""

import unittest
from dummy.continuous_integration import factorial, dummy_function


class TestFactorial(unittest.TestCase):
    """Tests for dummy.continuous_integration.factorial(starting_value)"""

    def test_base_case(self):
        """starting_value is 0 or 1"""
        self.assertEqual(factorial(0), 0)
        self.assertEqual(factorial(1), 1)

    def test_samples(self):
        """starting_value is an integer greater than 1"""
        self.assertEqual(factorial(2), 2)
        self.assertEqual(factorial(3), 6)
        self.assertEqual(factorial(4), 24)
        self.assertEqual(factorial(5), 120)

    def test_invalid(self):
        """starting_value is a negative integer"""
        with self.assertRaises(ValueError):
            factorial(-1)


class TestDummyFunction(unittest.TestCase):
    """Tests for dummy.continuous_integration.dummy_function(n_values)"""

    def test_positive(self):
        """n_values is a positive integer"""
        self.assertTrue(dummy_function(1))
        self.assertTrue(dummy_function(2))
        self.assertTrue(dummy_function(3))

    def test_zero(self):
        """n_values is 0"""
        self.assertTrue(dummy_function(0))

    def test_negative(self):
        """n_values is a negative integer"""
        self.assertTrue(dummy_function(-1))
        self.assertTrue(dummy_function(-2))
        self.assertTrue(dummy_function(-3))


if __name__ == "__main__":
    unittest.main()
