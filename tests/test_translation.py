"""Unit tests for module lapspython.translation."""

from lapspython.extraction import GrammarParser
from lapspython.translation import Translator
from lapspython.utils import load_checkpoint


class TestTranslator:
    """Run tests for lapspython.translation.Translator."""

    def test_init_python(self):
        """Load Python grammar."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        parsed_grammar = GrammarParser(grammar).parsed_grammar
        translator = Translator(parsed_grammar)
        assert translator.mode == 'python'

    def test_init_r(self):
        """Load R grammar."""
        grammar = load_checkpoint('re2_test').grammars[-1]
        parsed_grammar = GrammarParser(grammar, 'r').parsed_grammar
        translator = Translator(parsed_grammar)
        assert translator.mode == 'r'
