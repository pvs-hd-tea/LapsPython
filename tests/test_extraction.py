"""Unit tests for module lapspython.extraction."""

import lapspython.domains.dummy.dummyPrimitives
from lapspython.extraction import PrimitiveExtractor


class TestPrimitiveExtractor:
    """Run tests for lapspython.extraction.PrimitiveExtractor."""

    def test_module_loaded(self):
        """Call a primitive function to verify import."""
        assert lapspython.domains.dummy.dummyPrimitives._identity(True)

    def test_extract_no_primitives(self):
        """Extract primitives from a workspace without primitives."""
        pe = PrimitiveExtractor()
        assert pe.parsed_primitives == {}

    def test_extract_dummy_primitives(self):
        """Extract primitives from a dummy workspace."""
        pe = PrimitiveExtractor()
        primitives = pe.extract()
        assert primitives == pe.parsed_primitives
        assert len(primitives.keys()) == 5

        assert '_addition' in primitives
        assert '_subtraction' in primitives
        assert '_division' in primitives
        assert '_identity' in primitives
        assert '_not' in primitives

        assert primitives['_addition'].source == 'return lambda y: x + y'
        assert primitives['_subtraction'].source == 'return lambda y: x - y'
        assert primitives['_division'].source == 'return lambda y: x / y'
        assert primitives['_identity'].source == 'return x'
        assert primitives['_not'].source == 'return not x'

        assert primitives['_addition'].args == ['x']
        assert primitives['_subtraction'].args == ['x']
        assert primitives['_division'].args == ['x']
        assert primitives['_identity'].args == ['x']
        assert primitives['_not'].args == ['x']

