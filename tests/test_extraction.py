"""Unit tests for module lapspython.extraction."""

import pytest

from lapspython.extraction import GrammarParser
from lapspython.utils import load_checkpoint


class TestPrimitiveExtractor:
    """Run tests for lapspython.extraction.PrimitiveExtractor."""

    def test_init_no_grammar(self):
        """Construct parser with empty grammar."""
        parser = GrammarParser()
        assert parser.parsed_primitives == {}

    def test_init_re2(self):
        """Construct parser with passed grammar."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        parser = GrammarParser(grammar)
        assert parser.parsed_primitives != {}

    def test_parse_grammar_re2(self):
        """Extract primitives from an re2 grammar."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        parser = GrammarParser()
        parser.parse_grammar(grammar)

        assert '_rvowel' in parser.parsed_primitives
        assert '_rconcat' in parser.parsed_primitives
        assert 'map' in parser.parsed_primitives

        _rvowel = parser.parsed_primitives['_rvowel']
        assert _rvowel.name == '_rvowel'
        assert _rvowel.source == '(a|e|i|o|u)'
        assert _rvowel.args == []
        assert _rvowel.arg_types == []
        assert _rvowel.return_type.name == 'tsubstr'

        _rconcat = parser.parsed_primitives['_rconcat']
        assert _rconcat.name == '_rconcat'
        assert _rconcat.source == 'return s1 + s2'
        assert _rconcat.args == ['s1', 's2']
        assert len(_rconcat.arg_types) == 2
        assert _rconcat.arg_types[0].name == 'tsubstr'
        assert _rconcat.arg_types[1].name == 'tsubstr'
        assert _rconcat.return_type.name == 'tsubstr'

        _map = parser.parsed_primitives['map']
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
