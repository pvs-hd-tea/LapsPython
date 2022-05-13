"""Dummy code to test the Pylint/Flake8 workflow of the CI pipeline."""

from collections import Counter


def dummy_function(list_length: int = 3) -> bool:
    """Create a list of n increasing values and verify that they are distinct
    by accumulating the counts of each value and comparing them the list
    length.
    """
    list_of_n = list(range((list_length)))
    list_counter = Counter(list_of_n)
    accumulated_count = 0

    for element in list_of_n:
        accumulated_count += list_counter[element]

    return accumulated_count == len(list_of_n)


if dummy_function():
    print("Dummy successful!")
