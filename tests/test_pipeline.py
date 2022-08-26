"""Unit tests for module lapspython.translation."""

import pytest

from lapspython.pipeline import Pipeline
from lapspython.types import CompactResult


class TestPipeline:
    """Run tests for lapspython.translation.Translator."""

    def test_from_checkpoint_python(self):
        """Load checkpoint in Python mode."""
        result = Pipeline.from_checkpoint('re2_test', save=False)
        assert isinstance(result, CompactResult)

    def test_from_checkpoint_r(self):
        """Load checkpoint in R mode."""
        result = Pipeline.from_checkpoint('re2_test', 'r', False, False)
        assert isinstance(result, CompactResult)

    def test_invalid_mode(self):
        """Load checkpoint in invalid mode."""
        error_msg = 'mode must be "Python" or "R".'
        with pytest.raises(ValueError, match=error_msg):
            Pipeline.from_checkpoint('re2_test', 'cpp')
