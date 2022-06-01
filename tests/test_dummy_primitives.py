"""Unit tests for module lapspython.domains.dummy.dummyPrimitives."""

import pytest

from lapspython.domains.dummy.dummyPrimitives import (_addition, _division,
                                                      _identity, _not,
                                                      _subtraction,
                                                      not_a_primitive)


class TestDummyPrimitives:
    """Run tests for lapspython.domains.dummy.dummyPrimitives."""

    def test_addition(self):
        """Run tests for addition primitive and different data types."""
        assert _addition(1)(2) == 3
        assert _addition(1.0)(1.5) == 2.5
        assert _addition('a')('b') == 'ab'
        assert _addition(True)(False)

    def test_subtraction(self):
        """Run tests for subtraction primitive and different data types."""
        assert _subtraction(1)(2) == -1
        assert _subtraction(1.0)(1.5) == -0.5
        assert _subtraction(True)(False)
        expected_msg = r"unsupported operand type\(s\) for -: 'str' and 'str'"
        with pytest.raises(TypeError, match=expected_msg):
            assert _subtraction('a')('b') == 'ab'

    def test_division(self):
        """Run tests for division primitive and different data types."""
        assert _division(1)(2) == 0.5
        assert _division(1.0)(1.5) == 2 / 3
        with pytest.raises(ZeroDivisionError, match='division by zero'):
            assert _division(True)(False)
        expected_msg = r"unsupported operand type\(s\) for /: 'str' and 'str'"
        with pytest.raises(TypeError, match=expected_msg):
            assert _division('a')('b') == 'ab'

    def test_identity(self):
        """Run tests for identity primitive and different data types."""
        assert _identity(1) == 1
        assert _identity(1.5) == 1.5
        assert _identity(True)
        assert _identity('abc') == 'abc'

    def test_not(self):
        """Run tests for not primitive and different data types."""
        assert _not(1) is False
        assert _not(1.5) is False
        assert _not(False)
        assert _not('abc') is False

    def test_not_a_primitive(self):
        """Run tests for imposter function."""
        assert not_a_primitive(None) is None

