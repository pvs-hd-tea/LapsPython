"""Implements classes to extract primitives and lambda expressions."""

from dreamcoder.dreamcoder import ECResult
from dreamcoder.grammar import Grammar
from dreamcoder.program import Invented, Primitive
from lapspython.types import CompactFrontier, ParsedInvented, ParsedPrimitive


class GrammarParser:
    """Extract, parse, and store all primitives from grammar."""

    parsed_primitives: dict = {}
    parsed_invented: dict = {}

    def __init__(self, grammar: Grammar = None):
        """Optionally parse grammar if passed during construction.

        :param grammar: A grammar induced inside main() or ecIterator().
        :type grammar: dreamcoder.grammar.Grammar, optional
        """
        if grammar is not None:
            self.parse_grammar(grammar)

    def parse_grammar(self, grammar: Grammar) -> dict:
        """Convert Primitive objects to simplified ParsedPrimitive objects.

        :param grammar: A grammar induced inside main() or ecIterator().
        :type grammar: dreamcoder.grammar.Grammar
        :returns: A dictionary of ParsedPrimitive objects
        :rtype: dict
        """
        for _, _, primitive in grammar.productions:
            if isinstance(primitive, Primitive):
                name = primitive.name
                if name not in self.parsed_primitives:
                    parsed_primitive = ParsedPrimitive(primitive)
                    parsed_primitive = parsed_primitive.resolve_lambdas()
                    self.parsed_primitives[name] = parsed_primitive

            elif not isinstance(primitive, Invented):
                raise TypeError(f'Encountered unknown type {type(primitive)}.')

            elif str(primitive) not in self.parsed_invented:
                name = f'f{len(self.parsed_invented)}'
                parsed_invented = ParsedInvented(primitive, name)
                self.parsed_invented[str(primitive)] = parsed_invented

        return {'primitives': self.parsed_primitives,
                'invented': self.parsed_invented, }


class ProgramExtractor:
    """Extract and process synthesized programs."""

    hit_frontiers: dict = {}
    miss_frontiers: dict = {}

    def __init__(self, result: ECResult = None):
        """Optionally extract programs if passed during construction.

        :param result: A result produced by LAPS or checkpoint.
        :type result: dreamcoder.dreamcoder.ECResult, optional
        """
        if result is not None:
            self.extract(result)

    def extract(self, result: ECResult) -> dict:
        """Extract all frontiers with descriptions and frontiers.

        :param result: result of dreamcoder execution (checkpoint)
        :type result: dreamcoder.dreamcoder.ECResult
        :returns: A dictionary of extracted frontiers
        :rtype: dict
        """
        for frontier in result.allFrontiers.values():
            name = frontier.task.name
            annotation = result.taskLanguage.get(name, '')[0]
            compact_frontier = CompactFrontier(frontier, annotation)
            if frontier.empty:
                self.miss_frontiers[name] = compact_frontier
            else:
                self.hit_frontiers[name] = compact_frontier

        return {'hit': self.hit_frontiers, 'miss': self.miss_frontiers, }
