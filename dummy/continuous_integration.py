"""Dummy code to test the CI pipeline."""

from collections import Counter


def factorial(starting_value: int) -> int:
    """Returns the n-th factorial."""

    if not isinstance(starting_value, int):
        raise TypeError("starting_value must be a positive integer.")
    if starting_value < 0:
        raise ValueError("starting_value must be a positive integer.")

    if starting_value in (0, 1):
        return starting_value
    return starting_value * factorial(starting_value-1)


def dummy_function(n_values: int = 3) -> bool:
    """Create a list of n increasing or decreasing values and verify that they
    are distinct by accumulating the counts of each value and comparing them to
    the list length.
    """
    if not isinstance(n_values, int):
        raise TypeError("n_values must be an integer.")

    list_of_n = list(range((n_values)))
    list_of_n_counter = Counter(list_of_n)
    accumulated_count = 0

    for value in list_of_n:
        accumulated_count += list_of_n_counter[value]

    return accumulated_count == len(list_of_n)


if __name__ == '__main__':
    if dummy_function():
        print("Dummy successful!")
