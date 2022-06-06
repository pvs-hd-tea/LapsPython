"""Implements classes to extract primitives and lambda expressions."""

from dreamcoder.grammar import Grammar
from dreamcoder.program import Invented, Primitive
from lapspython.types import ParsedInvented, ParsedPrimitive


class GrammarParser:
    """Extract, parse, and store all primitives from grammar."""

    parsed_primitives: dict = {}
    parsed_invented: dict = {}

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
            if type(primitive) is Primitive:
                name = primitive.name
                if name not in self.parsed_primitives:
                    parsed = ParsedPrimitive(primitive)
                    self.parsed_primitives[name] = parsed.resolve_lambdas()

            elif type(primitive) is not Invented:
                raise TypeError(f'Encountered unknown type {type(primitive)}.')

            elif str(primitive) not in self.parsed_invented:
                name = f'f{len(self.parsed_invented)}'
                parsed = ParsedInvented(primitive, name)
                self.parsed_invented[str(primitive)] = parsed

        return {'primitives': self.parsed_primitives,
                'invented': self.parsed_invented, }
