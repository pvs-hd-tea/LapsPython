"""Utility functions that do not fit in other modules."""

import json
import os
import re

import dill

from dreamcoder.dreamcoder import ECResult
from dreamcoder.program import Program
from lapspython.extraction import GrammarParser, ProgramExtractor
from lapspython.translation import Translator
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


def get_source_similarity(source1: str, source2: str) -> float:
    """Compute Jaccard similarity of two translated programs."""
    set1 = tokenize_source(source1)
    set2 = tokenize_source(source2)
    return jaccard_similarity(set1, set2)


def tokenize_program(program: Program) -> list:
    """Tokenize synthesized program."""
    return re.split(r'[()]', str(program))


def tokenize_source(source: str) -> list:
    """Tokenize translated program for similarity computation.

    :param source: Translated program.
    :type source: string
    :returns: List of tokens longer excluding special symbols
    :rtype: list
    """
    tokens = re.split(r'\s', source)
    tokens_nonempty = [t for t in tokens if t != '']
    return [t for t in tokens_nonempty if not re.match(r'[^A-z]+', t)]


def jaccard_similarity(tokens1: list, tokens2: list) -> float:
    """Compute Jaccard similarity index of 2 sets."""
    set1 = set(tokens1)
    set2 = set(tokens2)
    return len(set1.intersection(set2)) / len(set1.union(set2))


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


# All subsequent functions are temporary for debugging purposes
def test_translation_invented():
    """Translate a sample invented primitive."""
    result = load_checkpoint('re2_test')
    grammar = GrammarParser(result.grammars[-1]).parsed_grammar
    translator = Translator(grammar)
    invented = result.grammars[-1].productions[0][2]
    return translator.translate(invented, 'f0')


def testg(i):
    """Extract grammar, translating all invented primitives."""
    result = load_checkpoint('re2_best_dsl_language')
    return result.grammars[-1].productions[i][-1]


def testgif():
    """Extract an invented primitive containing an if statement."""
    result = load_checkpoint('re2_best_dsl_language')
    p = result.grammars[-1].productions[4][-1]
    first_application = p.body.body.body.body.body
    next_abstraction_layer = first_application.f.f.f.body
    if_application = next_abstraction_layer.body.body.body
    return if_application.x


def testa(i):
    """Extract a sample program."""
    result = load_checkpoint('re2_test')
    hits = ProgramExtractor(result).compact_result.hit_frontiers
    for _hit in hits.values():
        i -= 1
        if not i:
            break
    return _hit.programs[0]


def testr():
    """Extract a sample result."""
    result = load_checkpoint('re2_test')
    grammar = GrammarParser(result.grammars[-1]).parsed_grammar
    translator = Translator(grammar)
    return ProgramExtractor(result, translator).compact_result


def testf():
    """Example a sample frontier."""
    result = testr()
    hf = result.hit_frontiers
    return hf[list(hf.keys())[0]]


def testv():
    """Test code validation."""
    f = testf()
    return f.translations[0].verify(f.examples)
