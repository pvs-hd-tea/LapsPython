"""Unit tests for module lapspython.extraction."""

import pytest

from dreamcoder.type import TypeConstructor
from lapspython.extraction import GrammarParser, ProgramExtractor
from lapspython.types import CompactFrontier
from lapspython.utils import load_checkpoint


class TestPrimitiveExtractor:
    """Run tests for lapspython.extraction.PrimitiveExtractor."""

    def test_init_default(self):
        """Construct parser with empty grammar."""
        parser = GrammarParser()
        assert parser.parsed_primitives == {}
        assert parser.parsed_invented == {}

    def test_init_re2(self):
        """Construct parser with passed grammar."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        parser = GrammarParser(grammar)
        assert parser.parsed_primitives != {}
        assert parser.parsed_invented != {}

    def test_parse_grammar_re2_pattern(self):
        """Extract primitives from an re2 grammar."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        parser = GrammarParser()
        _rvowel = parser.parse_grammar(grammar)['primitives']['_rvowel']
        assert _rvowel.name == '_rvowel'
        assert _rvowel.source == '(a|e|i|o|u)'
        assert _rvowel.args == []
        assert _rvowel.arg_types == []
        assert _rvowel.return_type.name == 'tsubstr'

    def test_parse_grammar_re2_lambda(self):
        """Extract primitives from an re2 grammar."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        parser = GrammarParser()
        _rconcat = parser.parse_grammar(grammar)['primitives']['_rconcat']
        assert _rconcat.name == '_rconcat'
        assert _rconcat.source == 'return s1 + s2'
        assert _rconcat.args == ['s1', 's2']
        assert len(_rconcat.arg_types) == 2
        assert _rconcat.arg_types[0].name == 'tsubstr'
        assert _rconcat.arg_types[1].name == 'tsubstr'
        assert _rconcat.return_type.name == 'tsubstr'

    def test_parse_grammar_re2_python(self):
        """Extract primitives from an re2 grammar."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        parser = GrammarParser()
        _map = parser.parse_grammar(grammar)['primitives']['map']
        assert _map.name == 'map'
        assert _map.source == 'return list(map(f, l))'
        assert _map.args == ['f', 'l']
        assert len(_map.arg_types) == 2
        assert _map.arg_types[0].name == '->'
        assert _map.arg_types[1].name == 'list'
        assert _map.return_type.name == 'list'

    def test_parse_grammar_unknown_type(self):
        """Test grammar with unexpected type."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        grammar.productions = [(None, None, None)]
        expected_message = "Encountered unknown type <class 'NoneType'>."
        with pytest.raises(TypeError, match=expected_message):
            GrammarParser(grammar)

    def test_parse_invented(self):
        """Extract invented primitive from re2 grammar."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        parser = GrammarParser(grammar)
        for invented in parser.parsed_invented.values():
            assert invented.name.find('f') == 0
            assert isinstance(invented.arg_types[0], TypeConstructor)
            assert isinstance(invented.return_type, TypeConstructor)


class TestProgramExtractor:
    """Run tests for lapspython.extraction.ProgramExtractor."""

    def test_init_default(self):
        """Default constructor."""
        extractor = ProgramExtractor()
        assert len(extractor.hit_frontiers) == 0
        assert len(extractor.miss_frontiers) == 0

    def test_init_re2(self):
        """Construct extractor with results."""
        result = load_checkpoint('re2_test')
        extractor = ProgramExtractor(result)
        assert len(extractor.hit_frontiers) > 0
        assert len(extractor.miss_frontiers) > 0

    def test_extract_hit(self):
        """Extract and validate HIT results."""
        result = load_checkpoint('re2_test')
        extractor = ProgramExtractor()
        extractor.extract(result)

        for name in extractor.hit_frontiers.keys():
            frontier = extractor.hit_frontiers[name]
            assert isinstance(frontier, CompactFrontier)
            assert frontier.name == name
            assert len(frontier.programs) > 0

    def test_extract_miss(self):
        """Extract and validate MISS results."""
        result = load_checkpoint('re2_test')
        extractor = ProgramExtractor()
        extractor.extract(result)

        for name in extractor.miss_frontiers.keys():
            frontier = extractor.miss_frontiers[name]
            assert isinstance(frontier, CompactFrontier)
            assert frontier.name == name
            assert len(frontier.programs) == 0
