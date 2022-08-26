"""Unit tests for module lapspython.types."""

import pytest

from dreamcoder.type import TypeConstructor
from lapspython.extraction import GrammarParser, ProgramExtractor
from lapspython.translation import Translator
from lapspython.types import (CompactFrontier, CompactResult, ParsedInvented,
                              ParsedPrimitive, ParsedRInvented,
                              ParsedRPrimitive, ParsedType)
from lapspython.utils import load_checkpoint


class TestParsedType:
    """Run tests for lapspython.types.ParsedType."""

    def test_init(self):
        """Constructor of abstract base class."""
        expected_message = "Can't instantiate .* ParsedType .* __init__"
        with pytest.raises(TypeError, match=expected_message):
            ParsedType()


class TestParsedPrimitive:
    """Run tests for lapspython.types.ParsedPrimitive."""

    def test_init(self):
        """Constructor."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        for _, _, primitive in grammar.productions:
            if str(primitive) == '_rconcat':
                break
        pp = ParsedPrimitive(primitive)
        assert pp.handle == '_rconcat'
        assert pp.name == 'rconcat'
        assert pp.source == 'return lambda s2: s1 + s2'
        assert pp.args == ['s1']
        assert pp.arg_types[0].name == 'tsubstr'
        assert pp.arg_types[1].name == 'tsubstr'
        assert pp.return_type.name == 'tsubstr'
        assert pp.imports == {'re'}
        assert pp.dependencies == set()

    def test_str_raw(self):
        """Test __str__() before simplification."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        for _, _, primitive in grammar.productions:
            if str(primitive) == '_rconcat':
                break
        pp = ParsedPrimitive(primitive)
        assert str(pp) == 'def rconcat(s1):\n    return lambda s2: s1 + s2\n'

    def test_resolve_lambdas(self):
        """Simplify primitive returning a lambda function."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        for _, _, primitive in grammar.productions:
            if str(primitive) == '_rconcat':
                break
        pp = ParsedPrimitive(primitive).resolve_lambdas()
        assert pp.handle == '_rconcat'
        assert pp.name == 'rconcat'
        assert pp.source == 'return s1 + s2'
        assert pp.args == ['s1', 's2']
        assert str(pp) == 'def rconcat(s1, s2):\n    return s1 + s2\n'

    def test_resolve_variables_valid(self):
        """Resolution using valid parameters."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        for _, _, primitive in grammar.productions:
            if str(primitive) == '_rconcat':
                break
        pp = ParsedPrimitive(primitive).resolve_lambdas()
        new_args = ['mask0', 'mask1']
        new_source = 'masked = mask0 + mask1'
        assert pp.resolve_variables(new_args, 'masked') == new_source

    def test_resolve_variables_no_return_name(self):
        """Resolution using valid parameters and no return replacement."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        for _, _, primitive in grammar.productions:
            if str(primitive) == '_rconcat':
                break
        pp = ParsedPrimitive(primitive).resolve_lambdas()
        new_args = ['mask0', 'mask1']
        new_source = 'return mask0 + mask1'
        assert pp.resolve_variables(new_args, '') == new_source

    def test_resolve_variables_identity(self):
        """Resolution using identical arguments."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        for _, _, primitive in grammar.productions:
            if str(primitive) == '_rconcat':
                break
        pp = ParsedPrimitive(primitive).resolve_lambdas()
        args = ['s1', 's2']
        new_source = 's1s2 = s1 + s2'
        assert pp.resolve_variables(args, 's1s2') == new_source

    def test_resolve_variables_invalid_length(self):
        """Resolution using incomplete arguments."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        for _, _, primitive in grammar.productions:
            if str(primitive) == '_rconcat':
                break
        pp = ParsedPrimitive(primitive)
        expected_message = r'Wrong number of arguments .+'
        with pytest.raises(ValueError, match=expected_message):
            pp.resolve_variables(['arg0', 'arg1'], 'return_name')

    def test_as_dict(self):
        """Transform parsed primitive to dict."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        for _, _, primitive in grammar.productions:
            if str(primitive) == '_rconcat':
                break
        p_dict = ParsedPrimitive(primitive).as_dict()
        assert p_dict['name'] == 'rconcat'
        assert p_dict['handle'] == '_rconcat'
        assert p_dict['source'] == 'return lambda s2: s1 + s2'
        assert p_dict['args'] == ['s1']
        assert p_dict['imports'] == ['re']
        assert p_dict['dependencies'] == []


class TestParsedRPrimitive:
    """Run tests for lapspython.types.ParsedRType."""

    def test_function_primitive(self):
        """Constructor."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        for _, _, primitive in grammar.productions:
            if str(primitive) == '_rconcat':
                break
        pp = ParsedRPrimitive(primitive)
        assert pp.handle == '_rconcat'
        assert pp.name == 'rconcat'
        assert pp.source == 'return(paste(s1, s2, sep = ""))'
        assert pp.args == ['s1', 's2']
        assert pp.arg_types[0].name == 'tsubstr'
        assert pp.arg_types[1].name == 'tsubstr'
        assert pp.return_type.name == 'tsubstr'
        assert pp.imports == {'glue', 'stringr'}
        assert pp.dependencies == set()

    def test_string_primitive(self):
        """Parse a primitive that is not a function."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        for _, _, primitive in grammar.productions:
            if str(primitive) == '_rdot':
                break
        pp = ParsedRPrimitive(primitive)
        assert pp.handle == '_rdot'
        assert pp.name == 'rdot'
        assert pp.source == '.'
        assert pp.args == []
        assert pp.arg_types == []
        assert str(pp.return_type) == 'tsubstr'
        assert pp.imports == set()
        assert pp.dependencies == set()

    def test_str(self):
        """Test __str__()."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        for _, _, primitive in grammar.productions:
            if str(primitive) == '_rmatch':
                break
        pp = ParsedRPrimitive(primitive)
        s = 'rmatch <- function(s1, s2) {\n    return(ismatch(s1, s2))\n}\n'
        assert str(pp) == s

    def test_resolve_lambdas(self):
        """Simplify primitive returning a lambda function."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        for _, _, primitive in grammar.productions:
            if str(primitive) == '_rconcat':
                break
        pp = ParsedRPrimitive(primitive)
        assert pp == pp.resolve_lambdas()

    def test_resolve_variables_valid(self):
        """Resolution using valid parameters."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        for _, _, primitive in grammar.productions:
            if str(primitive) == '_rconcat':
                break
        pp = ParsedRPrimitive(primitive).resolve_lambdas()
        new_args = ['mask0', 'mask1']
        new_source = 'masked <- paste(mask0, mask1, sep = "")'
        assert pp.resolve_variables(new_args, 'masked') == new_source


class TestParsedInvented:
    """Run tests for lapspython.types.ParsedInvented."""

    def test_init_re2(self):
        """Constructor with re2 checkpoint."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        parsed_grammar = GrammarParser(grammar).parsed_grammar
        handle = '#(_rsplit _rdot)'
        invented = parsed_grammar.invented[handle]
        assert isinstance(invented, ParsedInvented)
        assert invented.name != handle
        assert invented.name.find('f') == 0
        assert invented.handle == handle
        assert invented.args == ['arg1']
        trans = "def f0(arg1):\n    return __regex_split('.', arg1)\n"
        assert str(invented) == trans
        assert isinstance(invented.arg_types[0], TypeConstructor)
        assert isinstance(invented.return_type, TypeConstructor)

    def test_resolve_variables(self):
        """Resolution using valid parameters."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        parsed_grammar = GrammarParser(grammar).parsed_grammar
        invented = parsed_grammar.invented['#(_rsplit _rdot)']
        output = invented.resolve_variables(['mask0'], 'var')
        assert output == 'var = f0(mask0)'


class TestParsedRInvented:
    """Run tests for lapspython.types.ParsedInvented."""

    def test_init_re2(self):
        """Constructor with re2 checkpoint."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        parser = GrammarParser(grammar, mode='r')
        parsed_grammar = parser.parsed_grammar
        handle = '#(_rsplit _rdot)'
        invented = parsed_grammar.invented[handle]
        assert isinstance(invented, ParsedRInvented)
        assert invented.name != handle
        assert invented.name.find('f') == 0
        assert invented.handle == handle
        assert invented.args == ['arg1']
        assert isinstance(invented.arg_types[0], TypeConstructor)
        assert isinstance(invented.return_type, TypeConstructor)

    def test_resolve_variables(self):
        """Resolution using valid parameters."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        parser = GrammarParser(grammar, mode='r')
        parsed_grammar = parser.parsed_grammar
        invented = parsed_grammar.invented['#(_rsplit _rdot)']
        output = invented.resolve_variables(['mask0'], 'var')
        assert output == 'var <- f0(mask0)'


class TestParsedGrammar:
    """Run tests for lapspython.types.ParsedGrammar."""

    def test_init(self):
        """Constructor."""
        result = load_checkpoint('re2_test')
        grammar = GrammarParser(result.grammars[-1]).parsed_grammar
        assert len(grammar.primitives) > 0
        assert len(grammar.invented) == 1

    def test_as_dict(self):
        """Transform parsed grammar into dict."""
        result = load_checkpoint('re2_test')
        grammar = GrammarParser(result.grammars[-1]).parsed_grammar
        g_dict = grammar.as_dict()
        assert len(g_dict['primitives']) > 0
        assert isinstance(g_dict['primitives']['_rdot'], dict)
        assert len(g_dict['invented']) > 0
        assert isinstance(g_dict['invented']['#(_rsplit _rdot)'], dict)


class TestCompactFrontier:
    """Run tests for lapspython.types.CompactFrontier."""

    def test_init(self):
        """Constructor."""
        result = load_checkpoint('re2_test')
        grammar = GrammarParser(result.grammars[-1]).parsed_grammar
        translator = Translator(grammar)
        extractor = ProgramExtractor(result, translator)
        compact_result = extractor.compact_result
        for frontier in compact_result.hit_frontiers.values():
            assert isinstance(frontier, CompactFrontier)
            assert isinstance(frontier.name, str)
            assert isinstance(frontier.annotation, str)
            assert len(frontier.programs) > 0
            total_attempts = len(frontier.translations) + len(frontier.failed)
            assert total_attempts == len(frontier.programs)
        for frontier in compact_result.miss_frontiers.values():
            assert isinstance(frontier, CompactFrontier)
            assert isinstance(frontier.name, str)
            assert isinstance(frontier.annotation, str)
            assert len(frontier.programs) == 0
            assert len(frontier.translations) == 0


class TestCompactResult:
    """Run tests for lapspython.types.CompactResult."""

    def test_init_empty(self):
        """Constructor."""
        cr = CompactResult({}, {})
        assert cr.hit_frontiers == {}
        assert cr.miss_frontiers == {}

    def test_get_best_empty(self):
        """Return best posterior hit frontier of empty result."""
        cr = CompactResult({}, {})
        assert cr.get_best() == []

    def test_sample_empty(self):
        """Sample valid translation of empty result."""
        cr = CompactResult({}, {})
        assert cr.sample() == {}
