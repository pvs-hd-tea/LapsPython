"""Implements classes to extract primitives and lambda expressions."""

from dreamcoder.grammar import Grammar
from lapspython.types import ParsedPrimitive


class GrammarParser:
    """Extract, parse, and store all primitives from grammar."""

    parsed_primitives: dict = {}

    def __init__(self, grammar: Grammar = None):
        """Optionally parse grammar if passed during construction.

        :param grammar: A grammar induced inside main() or ecIterator().
        :type grammar: Grammar, optional
        """
        if grammar is not None:
            self.parse_grammar(grammar)

    def parse_grammar(self, grammar: Grammar) -> dict:
        """Convert Primitive objects to simplified ParsedPrimitive objects.

        :param grammar: A grammar induced inside main() or ecIterator().
        :type grammar: Grammar
        :returns: A dictionary of ParsedPrimitive objects
        :rtype: dict
        """
        for _, _, primitive in grammar.productions:
            name = primitive.name

            if name not in self.parsed_primitives:
                parsed = ParsedPrimitive(primitive)
                self.parsed_primitives[name] = parsed.resolve_lambdas()

        return self.parsed_primitives
