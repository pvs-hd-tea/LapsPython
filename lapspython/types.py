"""Implements types for parsed primitives and lambda expressions."""

import copy
import inspect
import re
from abc import ABC, abstractmethod

from dreamcoder.frontier import Frontier
from dreamcoder.program import Invented, Primitive
from dreamcoder.type import TypeConstructor, TypeVariable


class ParsedType(ABC):
    """Abstract base class for program parsing."""

    @abstractmethod
    def __init__(self) -> None:  # pragma: no cover
        """Parse input primitive and initialize members."""
        self.name = ''
        self.source = ''
        self.args = []
        self.arg_types = []
        self.returntype = type

    def __str__(self) -> str:
        """Construct clean Python function from object.

        :returns: Function source code
        :rtype: string
        """
        header = f'def {self.name}({", ".join(self.args)}):\n'
        indented_body = re.sub(r'^', '    ', self.source, flags=re.MULTILINE)
        return header + indented_body

    def parse_argument_types(self, arg_types: TypeConstructor) -> list:
        """Flatten inferred nested type structure of primitive.

        :param arg_types:Inferred types.
        :type arg_types: dreamcoder.type.TypeConstructor
        :returns: Flat list of inferred types.
        :rtype: list
        """
        if not isinstance(arg_types, TypeVariable) and arg_types.name == '->':
            arguments = arg_types.arguments
            return [arguments[0]] + self.parse_argument_types(arguments[1])
        else:
            return [arg_types]

    def resolve_lambdas(self) -> Primitive:
        """Remove lambda functions from source and extend list of arguments.

        :returns: New, cleaner parsed primitive
        :rtype: ParsedPrimitive
        """
        new_primitive = copy.copy(self)
        pattern = r'lambda (\S+): '
        new_primitive.args = self.args + re.findall(pattern, self.source)
        new_primitive.source = re.sub(pattern, '', self.source)
        return new_primitive

    def resolve_variables(self, args: list, return_name: str = '') -> str:
        """Substitute default arguments in source.

        :param args: List of new argument names (number must be equal)
        :type args: list
        :param return_name: Variable name to replace the return statement with
        :type return_name: string
        :returns: Source with replaced variable names
        :rtype: string
        """
        if len(args) != len(self.args):
            raise ValueError(f'args length {len(args)} != {len(self.args)}.')

        new_source = self.source
        for i in range(len(args)):
            new_source = re.sub(self.args[i], args[i], new_source)
        if return_name != '':
            new_source = re.sub('return', f'{return_name} =', new_source)
        return new_source


class ParsedPrimitive(ParsedType):
    """Class parsing primitives for translation to clean Python code."""

    def __init__(self, primitive: Primitive) -> None:
        """Construct ParsedPrimitive object with parsed function specs.

        :param primitive: A Primitive object
        :type primitive: dreamcoder.program.Primitive
        """
        implementation = primitive.value

        if inspect.isfunction(implementation):
            args = inspect.getfullargspec(implementation).args
            source = self._parse_source(implementation)
        else:
            args = []
            source = implementation

        dependencies = self._get_dependencies(implementation)
        self.dependencies = {d[1] for d in dependencies if d[0] in source}
        self.name = primitive.name
        self.source = source.strip()
        self.args = args
        self.arg_types = self.parse_argument_types(primitive.tp)
        self.return_type = self.arg_types.pop()

    def _parse_source(self, implementation) -> str:
        """Resolve lambdas and arguments to produce cleaner Python code.

        :param implementation: The function referenced by primitive
        :type implementation: function
        :returns: New source code
        :rtype: string
        """
        source = inspect.getsource(implementation)

        source = source[source.find(':') + 1:]

        indent_match = re.search(r'\w', source)
        if isinstance(indent_match, re.Match):
            indent = indent_match.start()

        if indent == 1:
            source = source[indent:]
        else:
            source = re.sub(r'^\n', '', source)
            source = re.sub(r'^ {4}', '', source, flags=re.MULTILINE)

        return re.sub(' #.+$', '', source)

    def _get_dependencies(self, implementation) -> dict:
        """Find functions called by primities that are not built-ins.

        :param implementation: The function referenced by a primitive
        :type implementation: function
        :returns: A (function name, source) dictionary
        :rtype: dict
        """
        module = inspect.getmodule(implementation)
        functions = inspect.getmembers(module, inspect.isfunction)
        dependent_functions = [f for f in functions if f[0][:2] == '__']
        return [(f[0], inspect.getsource(f[1])) for f in dependent_functions]


class ParsedInvented(ParsedType):
    """Class parsing invented primitives for translation to Python."""

    def __init__(self, invented: Invented, name: str) -> None:
        """Construct ParsedInvented object with parsed specs.

        :param invented: An invented primitive object
        :type invented: dreamcoder.program.Invented
        :param name: A custom name since invented primitives are unnamed
        :type name: string
        """
        self.name = name
        self.handle = str(invented)

        # TODO: parse source and arguments when translation is ready
        self.source = ''
        self.args = []

        self.arg_types = self.parse_argument_types(invented.tp)
        self.return_type = self.arg_types.pop()


class ParsedProgram(ParsedType):
    """Class parsing synthesized programs."""

    # TODO: finalize when translation is ready
    pass


class ParsedGrammar:
    """Data class containing parsed (invented) primitives."""

    def __init__(self, primitives: dict = {}, invented: dict = {}) -> None:
        """Store parsed (invented) primitives in member variables.
        
        :param primitives: A (name, ParsedPrimitive) dictionary.
        :type primitives: dict
        :param invented: A (name, ParsedInvented) dictionary.
        :type invented: dict
        """
        self.primitives: dict = primitives
        self.invented: dict = invented


class CompactFrontier:
    """Data class containing the important specs of extracted frontiers."""

    def __init__(self, frontier: Frontier, annotation: str = '') -> None:
        """Construct condensed frontier object with optional annotation."""
        self.annotation = annotation
        task = frontier.task
        self.name = task.name
        self.requested_types = task.request
        self.examples = task.examples
        entries = sorted(frontier.entries, key=lambda e: -e.logPosterior)
        self.programs = [entry.program for entry in entries]
        # TODO: finalize when translation is ready
        self.translations = []
        self.arguments = []


class CompactResult:
    """Data class containing (compact) extracted frontiers."""

    def __init__(self, hit: dict = {}, miss: dict = {}) -> None:
        """Store HIT and MISS CompactFrontiers in member variables.
        
        :param hit: A (name, HIT CompactFrontier) dictionary.
        :type hit: dict
        :param miss: A (name, MISS CompactFrontier) dictionary.
        :type miss: dict
        """
        self.hit_frontiers: dict = hit
        self.miss_frontiers: dict = miss
