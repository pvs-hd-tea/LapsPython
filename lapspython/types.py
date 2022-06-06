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
    def __init__(self):
        """Parse input primitive and initialize members."""
        self.name = ''
        self.source = ''
        self.args = []
        self.arg_types = []
        self.returntype = type

    def __str__(self):
        """Construct clean Python function from object.

        :returns: function source code
        :rtype: string
        """
        header = f'def {self.name}({", ".join(self.args)}):\n'
        indented_body = re.sub(r'^', '    ', self.source, flags=re.MULTILINE)
        return header + indented_body

    def parse_argument_types(self, arg_types: TypeConstructor) -> list:
        """Flatten inferred nested type structure of primitive.

        :param arg_types: arg_types: Inferred types.
        :type arg_types: dreamcoder.type.TypeConstructor
        :returns: Flat list of inferred types.
        :rtype: list
        """
        if type(arg_types) is not TypeVariable and arg_types.name == '->':
            arguments = arg_types.arguments
            return [arguments[0]] + self.parse_argument_types(arguments[1])
        else:
            return [arg_types]

    def resolve_lambdas(self):
        """Remove lambda functions from source and extend list of arguments.

        :returns: new, cleaner parsed primitive
        :rtype: ParsedPrimitive
        """
        new_primitive = copy.copy(self)
        pattern = r'lambda (\S+): '
        new_primitive.args = self.args + re.findall(pattern, self.source)
        new_primitive.source = re.sub(pattern, '', self.source)
        return new_primitive

    def resolve_variables(self, args: list) -> str:
        """Substitute default arguments in source.

        :param args: list of argument names (number must be equal)
        :type args: list
        """
        if type(args) not in (list, tuple):
            raise TypeError('args must be a list or tuple of strings.')
        if not all(type(arg) == str for arg in args):
            raise TypeError('args must be a list or tuple of strings.')
        if len(args) != len(self.args):
            raise ValueError(f'args length {len(args)} != {len(self.args)}.')

        new_source = self.source
        for i in range(len(args)):
            new_source = re.sub(self.args[i], args[i], new_source)
        return new_source


class ParsedPrimitive(ParsedType):
    """Class parsing primitives for translation to clean Python code."""

    def __init__(self, primitive: Primitive):
        """Construct ParsedPrimitive object with parsed function specs.

        :param primitive: A Primitive object
        :type primitive: dreamcoder.program.Primitive
        """
        implementation = primitive.value

        if inspect.isfunction(implementation):
            args = inspect.getfullargspec(implementation).args
            source = inspect.getsource(implementation)

            source = source[source.find(':') + 1:]
            indent_match = re.search(r'\w', source)
            if type(indent_match) is re.Match:
                indent = indent_match.start()
            if indent == 1:
                source = source[indent:]
            else:
                source = re.sub(r'^\n', '', source)
                source = re.sub(r'^ {4}', '', source, flags=re.MULTILINE)
        else:
            args = []
            source = implementation

        self.name = primitive.name
        self.source = source.strip()
        self.args = args
        self.arg_types = self.parse_argument_types(primitive.tp)
        self.return_type = self.arg_types.pop()


class ParsedInvented(ParsedType):
    """Class parsing invented primitives for translation to Python."""

    def __init__(self, invented: Invented, name: str):
        """Construct ParsedInvented object with parsed specs.

        :param invented: An invented primitive object
        :type invented: dreamcoder.program.Invented
        :param name: A custom name since invented primitives are unnamed
        :type name: string
        """
        self.name = name

        # TODO: parse source and arguments when translation is ready
        self.source = ''
        self.args = []

        self.arg_types = self.parse_argument_types(invented.tp)
        self.return_type = self.arg_types.pop()


class TranslatedProgram(ParsedType):
    """Class parsing synthesized programs."""

    # TODO: finalize when translation is ready
    pass


class CompactFrontier:
    """Data class containing the important specs of extracted frontiers."""

    def __init__(self, frontier: Frontier, annotation: str = ''):
        """Construct condensed frontier object with optional annotation."""
        self.annotation = annotation
        task = frontier.task
        self.name = task.name
        self.requested_types = task.request
        self.examples = task.examples
        entries = sorted(frontier.entries, key=lambda e: -e.logPosterior)
        self.programs = [entry.program for entry in entries]
        # TODO: finalize when translation is ready
        self.translations = None
