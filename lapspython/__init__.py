"""Extends LAPS with translation from lambda calculus to Python."""

from lapspython.pipeline import Pipeline
from lapspython.stats import Statistics

results_test = Pipeline.from_checkpoint('re2_best_dsl_language')
stats_test = Statistics()
stats_test.summarize(results_test)
