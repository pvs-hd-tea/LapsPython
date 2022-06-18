"""Utility functions that do not fit in other modules."""

import dill

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
    """Translate a sample program."""
    result = load_checkpoint('re2_test')
    grammar = GrammarParser(result.grammars[-1]).parsed_grammar
    translator = Translator(grammar)
    hits = ProgramExtractor(result).compact_result.hit_frontiers
    for _hit in hits.values():
        break
    program = _hit.programs[0]
    translation = translator.translate(program, _hit.name)
    return str(translation) + f"\nprint({_hit.name}('testword'))"


def test_translation_invented():
    """Translate a sample invented primitive."""
    result = load_checkpoint('re2_test')
    grammar = GrammarParser(result.grammars[-1]).parsed_grammar
    translator = Translator(grammar)
    invented = result.grammars[-1].productions[0][2]
    return translator.translate(invented, 'f0')
