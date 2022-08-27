"""Collect statistics for program translations."""

from typing import List

import numpy as np
import uniplot
from scipy import stats

from lapspython.types import CompactFrontier, CompactResult


class Statistics:
    """Collect statistics for translated frontiers and results."""

    stats: dict

    def __init__(self, result: CompactResult = None):
        """Construct object and optionally summarized result.

        :param result: Extracted and translated programs.
        :type result: CompactResult, optional
        """
        self.stats = {}

        if result is not None:
            self.summarize(result)

    def __str__(self) -> str:
        """Convert summary to string."""
        return '\n'.join([f'{k}:\t{v}' for k, v in self.stats.items()])

    def summarize(self, result: CompactResult) -> dict:
        """Compute descriptive statistics for given result.

        :param result: Translated checkpoint.
        :type result: lapspython.types.CompactResult
        :returns: Descriptive statistics.
        :rtype: dict
        """
        program_count = self.count_programs(result)
        self.stats.update({'programs': program_count})
        translation_count = self.count_translations(result)
        self.stats.update({'translations': translation_count})

        percentages = self.percentages_result(result)
        n_obs, minmax, mean, var, skew, kurtosis = stats.describe(percentages)
        self.stats.update({'tasks (total)': n_obs})
        self.stats.update({'tasks (solved)': np.count_nonzero(percentages)})
        self.stats.update({'median\t(%)': np.median(percentages)})
        self.stats.update({'min\t(%)': minmax[0]})
        self.stats.update({'max\t(%)': minmax[1]})
        self.stats.update({'mean\t(%)': mean})
        self.stats.update({'std\t(%)': np.sqrt(var)})

        return self.stats

    def plot_histogram(self, result: CompactResult) -> None:
        """Print histogram of percentages to terminal.

        :param result: Translated checkpoint.
        :type result: CompactResult
        """
        percentages = self.percentages_result(result)
        uniplot.histogram(percentages)

    def count_programs(self, result: CompactResult) -> int:
        """Count totals number of programs across all tasks.

        :param result: Translated checkpoint.
        :type result: lapspython.types.CompactResult
        :rtype: int
        """
        program_count: int = 0
        for frontier in result.hit_frontiers.values():
            program_count += len(frontier.programs)
        return program_count

    def count_translations(self, result: CompactResult) -> int:
        """Count total number of correct translations across all tasks.

        :param result: Translated checkpoint.
        :type result: lapspython.types.CompactResult
        :rtype: int
        """
        translation_count: int = 0
        for frontier in result.hit_frontiers.values():
            translation_count += len(frontier.translations)
        return translation_count

    def percentages_result(self, result: CompactResult) -> List[float]:
        """Return percentage of correctly translated programs per frontier.

        :param result: Translated checkpoint.
        :type result: lapspython.types.CompactResult
        :rtype: List[float]
        """
        percentages: list = []
        for frontier in result.hit_frontiers.values():
            percentages.append(self.percentage_frontier(frontier))
        return percentages

    def percentage_frontier(self, frontier: CompactFrontier) -> float:
        """Return percentage of correctly translated programs.

        :param result: Translated frontier (task).
        :type result: lapspython.types.CompactFrontier
        :rtype: float
        """
        return len(frontier.translations) / len(frontier.programs) * 100
