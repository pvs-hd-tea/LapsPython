"""Unit tests for module lapspython.extraction."""

import pytest

from dreamcoder.type import TypeConstructor
from lapspython.extraction import GrammarParser, ProgramExtractor
from lapspython.types import CompactFrontier
from lapspython.utils import load_checkpoint


class TestGrammarParser:
    """Run tests for lapspython.extraction.GrammarParser."""

    def test_init_default(self):
        """Construct parser with empty grammar."""
        parsed_grammar = GrammarParser().parsed_grammar
        assert parsed_grammar.primitives == {}
        assert parsed_grammar.invented == {}

    def test_init_re2(self):
        """Construct parser with passed grammar."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        parsed_grammar = GrammarParser(grammar).parsed_grammar
        assert parsed_grammar.primitives != {}
        assert parsed_grammar.invented != {}

    def test_invalid_mode(self):
        """Construct parser with an unsupported mode."""
        error_msg = 'mode must be "Python" or "R".'
        with pytest.raises(ValueError, match=error_msg):
            GrammarParser(mode='cpp')

    def test_parse_re2_pattern(self):
        """Extract primitives from an re2 grammar."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        parser = GrammarParser()
        _rvowel = parser.parse(grammar).primitives['_rvowel']
        assert _rvowel.handle == '_rvowel'
        assert _rvowel.name == 'rvowel'
        assert _rvowel.source == '(a|e|i|o|u)'
        assert _rvowel.args == []
        assert _rvowel.arg_types == []
        assert _rvowel.return_type.name == 'tsubstr'

    def test_parse_re2_lambda(self):
        """Extract primitives from an re2 grammar."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        parser = GrammarParser()
        _rconcat = parser.parse(grammar).primitives['_rconcat']
        assert _rconcat.handle == '_rconcat'
        assert _rconcat.name == 'rconcat'
        assert _rconcat.source == 'return s1 + s2'
        assert _rconcat.args == ['s1', 's2']
        assert len(_rconcat.arg_types) == 2
        assert _rconcat.arg_types[0].name == 'tsubstr'
        assert _rconcat.arg_types[1].name == 'tsubstr'
        assert _rconcat.return_type.name == 'tsubstr'

    def test_parse_re2_python(self):
        """Extract Python primitives from an re2 grammar."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        parser = GrammarParser()
        _map = parser.parse(grammar).primitives['map']
        assert _map.name == 'map'
        assert _map.source == 'return list(map(f, l))'
        assert _map.args == ['f', 'l']
        assert len(_map.arg_types) == 2
        assert _map.arg_types[0].name == '->'
        assert _map.arg_types[1].name == 'list'
        assert _map.return_type.name == 'list'

    def test_parse_re2_r(self):
        """Extract R primitives from an re2 grammar."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        parser = GrammarParser(mode='r')
        _map = parser.parse(grammar).primitives['map']
        assert _map.name == 'map'
        assert _map.source == 'return(sapply(l, f))'
        assert _map.args == ['f', 'l']
        assert len(_map.arg_types) == 2
        assert _map.arg_types[0].name == '->'
        assert _map.arg_types[1].name == 'list'
        assert _map.return_type.name == 'list'

    def test_parse_unknown_type(self):
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
        parsed_grammar = parser.parsed_grammar
        for invented in parsed_grammar.invented.values():
            assert invented.name.find('f') == 0
            assert isinstance(invented.arg_types[0], TypeConstructor)
            assert isinstance(invented.return_type, TypeConstructor)

    def test_fix_invented_invalid_keys(self):
        """Override invented primitive from re2 grammar with invalid dict."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        parser = GrammarParser(grammar)
        error_msg = 'Keys of the two grammars are not equal'
        with pytest.raises(ValueError, match=error_msg):
            parser.fix_invented({'key': 'value'})

    def test_fix_invented_valid_keys(self):
        """Override invented primitive from re2 grammar with valid dict."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        parser = GrammarParser(grammar)

        handle = '#(_rsplit _rdot)'

        old_invented = parser.parsed_grammar.invented[handle]
        assert old_invented.name == 'f0'
        assert old_invented.source == "return __regex_split('.', arg1)"
        assert old_invented.args == ['arg1']

        new_invented = {
            handle: {
                'name': 'new name',
                'source': 'new source',
                'args': ['new args'],
                'dependencies': ['new dependencies']
            }
        }

        parser.fix_invented(new_invented)

        override_invented = parser.parsed_grammar.invented[handle]
        assert override_invented.name == 'new name'
        assert override_invented.source == 'new source'
        assert override_invented.args == ['new args']
        assert override_invented.dependencies == ['new dependencies']


class TestProgramExtractor:
    """Run tests for lapspython.extraction.ProgramExtractor."""

    def test_init_default(self):
        """Default constructor."""
        extractor = ProgramExtractor()
        compact_result = extractor.compact_result
        assert compact_result.hit_frontiers == {}
        assert compact_result.miss_frontiers == {}

    def test_init_re2(self):
        """Construct extractor with results."""
        result = load_checkpoint('re2_test')
        extractor = ProgramExtractor(result)
        assert len(extractor.compact_result.hit_frontiers) > 0
        assert len(extractor.compact_result.miss_frontiers) > 0

    def test_extract_hit(self):
        """Extract and validate HIT results."""
        result = load_checkpoint('re2_test')
        extractor = ProgramExtractor()
        compact_result = extractor.extract(result)

        for name in compact_result.hit_frontiers.keys():
            frontier = compact_result.hit_frontiers[name]
            assert isinstance(frontier, CompactFrontier)
            assert frontier.name == name
            assert len(frontier.programs) > 0

    def test_extract_miss(self):
        """Extract and validate MISS results."""
        result = load_checkpoint('re2_test')
        extractor = ProgramExtractor()
        compact_result = extractor.extract(result)

        for name in compact_result.miss_frontiers.keys():
            frontier = compact_result.miss_frontiers[name]
            assert isinstance(frontier, CompactFrontier)
            assert frontier.name == name
            assert len(frontier.programs) == 0
