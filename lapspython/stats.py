"""Collect statistics for program translations."""

import numpy as np
from scipy import stats

from lapspython.types import CompactFrontier, CompactResult


class Statistics:
    """Collect statistics for translated frontiers and results."""

    stats: dict = {}

    def __str__(self) -> str:
        """Print summary as string."""
        return '\n'.join([f'{k}: {v}' for k, v in self.stats.items()])

    def summarize(self, result: CompactResult) -> dict:
        """Descriptive statistics for result."""
        program_count = self.count_programs(result)
        self.stats.update({'programs': program_count})
        translation_count = self.count_translations(result)
        self.stats.update({'translations': translation_count})

        percentages = self.percentages_result(result)
        nobs, minmax, mean, var, skew, kurtosis = stats.describe(percentages)
        self.stats.update({'frontiers': nobs})
        self.stats.update({'solved': np.count_nonzero(percentages)})
        self.stats.update({'min': minmax[0], 'max': minmax[1]})
        self.stats.update({'median': np.median(percentages)})
        self.stats.update({'mean': mean})
        self.stats.update({'var': var})
        self.stats.update({'std': np.sqrt(var)})
        self.stats.update({'skewness': skew})
        self.stats.update({'kurtosis': kurtosis})

        return self.stats

    def count_programs(self, result: CompactResult) -> int:
        """Count totals number of programs across all tasks."""
        program_count: int = 0
        for frontier in result.hit_frontiers.values():
            program_count += len(frontier.programs)
        return program_count

    def count_translations(self, result: CompactResult) -> int:
        """Count total number of correct translations across all tasks."""
        translation_count: int = 0
        for frontier in result.hit_frontiers.values():
            translation_count += len(frontier.translations)
        return translation_count

    def percentages_result(self, result: CompactResult) -> list:
        """Return percentage of correctly translated programs per frontier."""
        percentages: list = []
        for frontier in result.hit_frontiers.values():
            percentages.append(self.percentage_frontier(frontier))
        return percentages

    def percentage_frontier(self, frontier: CompactFrontier) -> float:
        """Return percentage of correctly translated programs."""
        return len(frontier.translations) / len(frontier.programs)
