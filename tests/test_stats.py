"""Unit tests for module lapspython.stats."""

from lapspython.pipeline import Pipeline
from lapspython.stats import Statistics


class TestStatistics:
    """Tests for lapspython.stats.Statistics."""

    def test_init_empty(self):
        """Constructor without result input."""
        assert Statistics().stats == {}

    def test_re2_small(self):
        """Constructor with mock results."""
        result = Pipeline.from_checkpoint(
            're2_test', verbose=False, save=False
        )

        stats = Statistics().summarize(result)
        assert stats['programs'] == stats['translations'] == 75
        assert stats['tasks (total)'] == stats['tasks (solved)'] == 18
        assert stats['median\t(%)'] == stats['mean\t(%)'] == 100.0
        assert stats['min\t(%)'] == stats['max\t(%)'] == 100.0
        assert stats['std\t(%)'] == 0.0
