"""Utility functions that do not fit in other modules."""

import dill

from dreamcoder.dreamcoder import ECResult


def load_checkpoint(filename: str) -> ECResult:
    """Load training checkpoint.

    :param filename: name of file in checkpoints directory, without extension
    :type filename: string
    :returns: e
    """
    with open('checkpoints/' + filename + '.pickle', 'rb') as handle:
        return dill.load(handle)
