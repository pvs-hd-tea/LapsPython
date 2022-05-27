"""Unit tests for module lapspython.extraction."""

from lapspython.extraction import PrimitiveExtractor


class TestPrimitiveExtractor:
    """Run tests for lapspython.extraction.PrimitiveExtractor."""

    def test_no_primitives(self):
        """Extract primitives from a workspace without primitives."""
        pe = PrimitiveExtractor()
        assert pe.parsed_primitives == {}

