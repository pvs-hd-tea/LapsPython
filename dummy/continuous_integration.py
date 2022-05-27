"""Dummy code to test the CI pipeline."""

from collections import Counter


def factorial(starting_value: int) -> int:
    """Return the n-th factorial.

    Args:
        - starting_value: n
    Returns:
        - n-th factorial
    """
    if not isinstance(starting_value, int):
        raise TypeError('starting_value must be a positive integer.')
    if starting_value < 0:
        raise ValueError('starting_value must be a positive integer.')

    if starting_value in (0, 1):
        return starting_value
    return starting_value * factorial(starting_value - 1)


def dummy_function(n_values: int = 3) -> bool:
    """Validate linting workflow using pointless computations.

    Args:
        - n_values: list length
    Returns:
        - True (output should never be False)
    """
    if not isinstance(n_values, int):
        raise TypeError('n_values must be an integer.')

    list_of_n = list(range((n_values)))
    list_of_n_counter = Counter(list_of_n)
    accumulated_count = 0

    for value in list_of_n:
        accumulated_count += list_of_n_counter[value]

    return accumulated_count == len(list_of_n)
