"""Unit tests for module lapspython.stats."""

from lapspython.stats import Statistics


class TestStatistics:
    """Tests for lapspython.stats.Statistics."""

    def test_init_empty(self):
        """Constructor without result input."""
        assert Statistics().stats == {}
