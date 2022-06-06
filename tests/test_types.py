"""Unit tests for module lapspython.types."""

import pytest

from dreamcoder.type import TypeConstructor
from lapspython.extraction import GrammarParser, ProgramExtractor
from lapspython.types import (CompactFrontier, ParsedInvented, ParsedPrimitive,
                              ParsedType)
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
        for _, _, p in grammar.productions:
            if str(p) == '_rconcat':
                primitive = p
                break
        pp = ParsedPrimitive(primitive)
        assert pp.name == '_rconcat'
        assert pp.source == 'return lambda s2: s1 + s2'
        assert pp.args == ['s1']
        assert pp.arg_types[0].name == 'tsubstr'
        assert pp.arg_types[1].name == 'tsubstr'
        assert pp.return_type.name == 'tsubstr'

    def test_str_raw(self):
        """Test __str__() before simplification."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        for _, _, p in grammar.productions:
            if str(p) == '_rconcat':
                primitive = p
                break
        pp = ParsedPrimitive(primitive)
        assert str(pp) == 'def _rconcat(s1):\n    return lambda s2: s1 + s2'

    def test_resolve_lambdas(self):
        """Simplify primitive returning a lambda function."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        for _, _, p in grammar.productions:
            if str(p) == '_rconcat':
                primitive = p
                break
        pp = ParsedPrimitive(primitive).resolve_lambdas()
        assert pp.name == '_rconcat'
        assert pp.source == 'return s1 + s2'
        assert pp.args == ['s1', 's2']
        assert str(pp) == 'def _rconcat(s1, s2):\n    return s1 + s2'

    def test_resolve_variables_valid(self):
        """Resolution using valid parameters."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        for _, _, p in grammar.productions:
            if str(p) == '_rconcat':
                primitive = p
                break
        pp = ParsedPrimitive(primitive).resolve_lambdas()
        new_args = ['mask0', 'mask1']
        new_source = 'return mask0 + mask1'
        assert pp.resolve_variables(new_args) == new_source

    def test_resolve_variables_identity(self):
        """Resolution using identical arguments."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        for _, _, p in grammar.productions:
            if str(p) == '_rconcat':
                primitive = p
                break
        pp = ParsedPrimitive(primitive).resolve_lambdas()
        args = ['s1', 's2']
        assert pp.resolve_variables(args) == pp.source

    def test_resolve_variables_invalid_args(self):
        """Resolution using invalid arguments."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        for _, _, p in grammar.productions:
            if str(p) == '_rconcat':
                primitive = p
                break
        pp = ParsedPrimitive(primitive)
        expected_message = 'args must be a list or tuple of strings.'
        with pytest.raises(TypeError, match=expected_message):
            pp.resolve_variables('mask')
        with pytest.raises(TypeError, match=expected_message):
            pp.resolve_variables(42)
        with pytest.raises(TypeError, match=expected_message):
            pp.resolve_variables([42])

    def test_resolve_variables_invalid_length(self):
        """Resolution using incomplete arguments."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        for _, _, p in grammar.productions:
            if str(p) == '_rconcat':
                primitive = p
                break
        pp = ParsedPrimitive(primitive)
        expected_message = 'args length 2 != 1.'
        with pytest.raises(ValueError, match=expected_message):
            pp.resolve_variables(['arg0', 'arg1'])


class TestParsedInvented:
    """Run tests for lapspython.types.ParsedInvented."""

    def test_init(self):
        """Constructor."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        parser = GrammarParser(grammar)
        for name in parser.parsed_invented.keys():
            invented = parser.parsed_invented[name]
            assert isinstance(invented, ParsedInvented)
            assert invented.name != name
            assert invented.name.find('f') == 0
            assert str(invented) == 'def f0():\n    '
            assert isinstance(invented.arg_types[0], TypeConstructor)
            assert isinstance(invented.return_type, TypeConstructor)


class TestParsedProgram:
    """Run tests for lapspython.types.ParsedProgram."""

    # TODO: implement when translation is ready
    pass


class TestCompactFrontier:
    """Run tests for lapspython.types.CompactFrontier."""

    def test_init(self):
        """Constructor."""
        result = load_checkpoint('re2_test')
        extractor = ProgramExtractor(result)
        for frontier in extractor.hit_frontiers.values():
            assert isinstance(frontier, CompactFrontier)
            assert isinstance(frontier.name, str)
            assert isinstance(frontier.annotation, str)
            assert len(frontier.programs) > 0
            assert len(frontier.translations) == len(frontier.programs)
        for frontier in extractor.miss_frontiers.values():
            assert isinstance(frontier, CompactFrontier)
            assert isinstance(frontier.name, str)
            assert isinstance(frontier.annotation, str)
            assert len(frontier.programs) == 0
            assert len(frontier.translations) == 0
