"""Extends LAPS with translation from lambda calculus to Python."""

from lapspython.pipeline import Pipeline

results_test = Pipeline.from_checkpoint('re2_best_dsl_language', 'r')
