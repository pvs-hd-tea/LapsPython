"""Utility functions that do not fit in other modules."""

import json
import os
import re

import dill

from dreamcoder.dreamcoder import ECResult
from lapspython.types import CompactResult, ParsedGrammar


def load_checkpoint(filename: str) -> ECResult:
    """Load training checkpoint.

    :param filename: name of file in checkpoints directory, without extension
    :type filename: string
    :returns: e
    """
    with open(f'checkpoints/{filename}.pickle', 'rb') as handle:
        return dill.load(handle)


def json_dump(
    filename: str,
    grammar: ParsedGrammar,
    result: CompactResult  # = None
) -> None:
    """Store grammar and best results in json file.

    :param filename: File name in checkpoints folder without file extension.
    :type filename: str
    :param grammar: Grammar extracted and parsed from checkpoint.
    :type grammar: ParsedGrammar
    :param result: Result extracted and translated from checkpoint.
    :type result: CompactResult, optional
    """
    json_path = f'checkpoints/{filename}.json'
    json_dict = {
        'grammar': grammar.as_dict(),
        'result': result.get_best()
    }
    with open(json_path, 'w') as json_file:
        try:
            json.dump(json_dict, json_file, indent=4)
        except TypeError:
            os.remove(json_path)
            raise


def json_read(filename: str) -> dict:
    """Read grammar and results from json file.

    :param filename: File name in checkpoints folder without file extension.
    :type filename: str
    :returns: {grammar, result} dictionary
    :rytpe: dict
    """
    json_path = f'checkpoints/{filename}.json'
    try:
        with open(json_path, 'r') as json_file:
            json_dict = json.load(json_file)
        grammar = json_dict['grammar']
        parsed = ParsedGrammar(grammar['primitives'], grammar['invented'])
        json_dict['grammar'] = parsed
        return json_dict
    except FileNotFoundError:
        return {}
