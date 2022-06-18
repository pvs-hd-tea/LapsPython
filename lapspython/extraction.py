"""Implements classes to extract primitives and lambda expressions."""

from dreamcoder.dreamcoder import ECResult
from dreamcoder.grammar import Grammar
from dreamcoder.program import Invented, Primitive
from lapspython.translation import Translator
from lapspython.types import (CompactFrontier, CompactResult, ParsedGrammar,
                              ParsedInvented, ParsedPrimitive)


class GrammarParser:
    """Extract, parse, and store all primitives from grammar."""

    def __init__(self, grammar: Grammar = None) -> None:
        """Optionally parse grammar if passed during construction.

        :param grammar: A grammar induced inside main() or ecIterator().
        :type grammar: dreamcoder.grammar.Grammar, optional
        """
        if grammar is not None:
            self.parse(grammar)
        else:
            self.parsed_grammar = ParsedGrammar({}, {})

    def parse(self, grammar: Grammar) -> ParsedGrammar:
        """Convert Primitive objects to simplified ParsedPrimitive objects.

        :param grammar: A grammar induced inside main() or ecIterator().
        :type grammar: dreamcoder.grammar.Grammar
        :returns: A ParsedGrammar object
        :rtype: ParsedGrammar
        """
        parsed_primitives: dict = {}
        parsed_invented: dict = {}

        for _, _, primitive in grammar.productions:
            if isinstance(primitive, Primitive):
                name = primitive.name
                if name not in parsed_primitives:
                    parsed_primitive = ParsedPrimitive(primitive)
                    parsed_primitive = parsed_primitive.resolve_lambdas()
                    parsed_primitives[name] = parsed_primitive

            elif not isinstance(primitive, Invented):
                raise TypeError(f'Encountered unknown type {type(primitive)}.')

            elif str(primitive) not in parsed_invented:
                handle = str(primitive)
                name = f'f{len(parsed_invented)}'
                parsed_invented[handle] = ParsedInvented(primitive, name)

        self.parsed_grammar = ParsedGrammar(parsed_primitives, parsed_invented)

        translator = Translator(self.parsed_grammar)
        for invented in self.parsed_grammar.invented.values():
            trans = translator.translate(invented.program, invented.name)
            invented.source = trans.source
            invented.dependencies = trans.dependencies

        return self.parsed_grammar


class ProgramExtractor:
    """Extract and process synthesized programs."""

    def __init__(self, result: ECResult = None) -> None:
        """Optionally extract programs if passed during construction.

        :param result: A result produced by LAPS or checkpoint.
        :type result: dreamcoder.dreamcoder.ECResult, optional
        """
        if result is not None:
            self.extract(result)
        else:
            self.compact_result = CompactResult({}, {})

    def extract(self, result: ECResult) -> CompactResult:
        """Extract all frontiers with descriptions and frontiers.

        :param result: result of dreamcoder execution (checkpoint)
        :type result: dreamcoder.dreamcoder.ECResult
        :returns: A CompactResult object
        :rtype: CompactResult
        """
        hit_frontiers = {}
        miss_frontiers = {}

        grammar = GrammarParser(result.grammars[-1]).parsed_grammar
        translator = Translator(grammar)

        for frontier in result.allFrontiers.values():
            name = frontier.task.name
            annotation = result.taskLanguage.get(name, '')[0]
            compact_frontier = CompactFrontier(frontier, annotation)
            if frontier.empty:
                miss_frontiers[name] = compact_frontier
            else:
                hit_frontiers[name] = compact_frontier
                for program in compact_frontier.programs:
                    trans = translator.translate(program, name)
                    compact_frontier.translations.append(trans.source)
                    compact_frontier.args.append(trans.args)

        self.compact_result = CompactResult(hit_frontiers, miss_frontiers)
        return self.compact_result
