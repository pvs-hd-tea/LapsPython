"""Utility functions that do not fit in other modules."""

import dill
import re

from dreamcoder.dreamcoder import ECResult
from lapspython.extraction import GrammarParser, ProgramExtractor
from lapspython.translation import Translator


def load_checkpoint(filename: str) -> ECResult:
    """Load training checkpoint.

    :param filename: name of file in checkpoints directory, without extension
    :type filename: string
    :returns: e
    """
    with open('checkpoints/' + filename + '.pickle', 'rb') as handle:
        return dill.load(handle)

def test_translation_abstraction():
    result = load_checkpoint('re2_test')
    grammar = GrammarParser(result.grammars[-1]).parsed_grammar
    translator = Translator(grammar)
    hits = ProgramExtractor(result).compact_result.hit_frontiers
    for hit in hits.values():
        break
    program = hit.programs[0]
    print()
    print(program)
    translation = translator.translate(program, hit.name)
    print()
    print(translation)
    e = translation + f"\nprint(re2_train_0_if_the_word_ends_with_any_letter_add_w_after_that('testword'))"
    exec(e)

def test_translation_invented():
    result = load_checkpoint('re2_test')
    grammar = GrammarParser(result.grammars[-1]).parsed_grammar
    translator = Translator(grammar)
    invented = result.grammars[-1].productions[0][2]
    translation = translator.translate(invented)
    return translation

t = test_translation_invented()
print(t)