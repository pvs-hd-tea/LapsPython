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
        self.name: str = ''
        self.handle: str = ''
        self.source: str = ''
        self.args: list = []
        self.arg_types: list = []
        self.returntype = type

    def __str__(self) -> str:
        """Construct clean Python function from object.

        :returns: Function source code
        :rtype: string
        """
        header = f'def {self.name}({", ".join(self.args)}):\n'
        indented_body = re.sub(r'^', '    ', self.source, flags=re.MULTILINE)
        return header + indented_body + '\n'

    @classmethod
    def parse_argument_types(cls, arg_types: TypeConstructor) -> list:
        """Flatten inferred nested type structure of primitive.

        :param arg_types:Inferred types.
        :type arg_types: dreamcoder.type.TypeConstructor
        :returns: Flat list of inferred types.
        :rtype: list
        """
        if not isinstance(arg_types, TypeVariable) and arg_types.name == '->':
            arguments = arg_types.arguments
            return [arguments[0]] + cls.parse_argument_types(arguments[1])
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
            func = f'{self.name}({", ".join(self.args)})'
            raise ValueError(f'Wrong number of arguments for {func}: {args}.')

        new_source = self.source
        for i in range(len(args)):
            pattern = fr'(\(|\[| )({self.args[i]})(,| |\)|\[|\]|$)'
            fstring_pattern = '{' + str(self.args[i]) + '}'
            repl = fr'\1{args[i]}\3'
            new_source = re.sub(pattern, repl, new_source)
            new_source = re.sub(fstring_pattern, str(args[i]), new_source)
        if return_name != '':
            return re.sub('return', f'{return_name} =', new_source)
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
        self.handle = primitive.name
        self.name = re.sub(r'^[^a-z]+', '', self.handle)
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

    def _get_dependencies(self, implementation) -> list:
        """Find functions called by primities that are not built-ins.

        :param implementation: The function referenced by a primitive
        :type implementation: function
        :returns: A list of (function name, source) tuples
        :rtype: list
        """
        module = inspect.getmodule(implementation)
        functions = inspect.getmembers(module, inspect.isfunction)
        dependent_functions = [f for f in functions if f[0][:2] == '__']
        return [(f[0], inspect.getsource(f[1])) for f in dependent_functions]


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
        self.handle = str(invented)
        self.program = invented

        # To avoid circular imports, source translation is only handled by
        # lapspython.extraction.GrammarParser instead of during construction.
        self.source = ''
        self.args: list = []
        self.dependencies: list = []

        self.arg_types = self.parse_argument_types(invented.tp)
        self.return_type = self.arg_types.pop()

    def resolve_variables(self, args: list, return_name: str = '') -> str:
        """Instead arguments in function call rather than definition."""
        if return_name == '':
            head = 'return '
        else:
            head = f'{return_name} = '
        body = f'{self.name}({", ".join(args)})'
        return f'{head}{body}'


class ParsedProgram(ParsedType):
    """Class parsing synthesized programs."""

    imports = ['re']

    def __init__(self, name: str, source: str, args: list, dependencies: set):
        """Store Python program with dependencies, arguments, and name.

        :param name: Task name or invented primitive handle
        :type name: string
        :param source: The Python translation of a given program
        :type source: string
        :param args: List of arguments to be resolved when used
        :type args: list
        :param dependencies: Source codes of called functions
        :type dependencies: set
        """
        self.name = name
        self.handle = name
        self.source = source
        self.args = args
        self.dependencies = dependencies

    def __str__(self) -> str:
        """Return dependencies and source code as string.

        :returns: Full source code of translated program
        :rtype: string
        """
        imports = '\n'.join([f'import {module}' for module in self.imports])
        dependencies = '\n'.join(self.dependencies) + '\n'
        header = f'def {self.name}({", ".join(self.args)}):\n'
        indent_source = re.sub(r'^', '    ', self.source, flags=re.MULTILINE)
        return imports + '\n\n' + dependencies + header + indent_source

    def verify(self, examples: list) -> bool:
        """Verify code for a list of examples from task.

        :param examples: A list of (input, output) tuples
        :type examples: list
        :returns: Whether the translated program is correct.
        :rtype: bool
        """
        exec_translation = str(self) + '\n\n'

        for example in examples:
            example_inputs = [f"'{x}'" for x in example[0]]
            example_output = str(example[1])

            joined_inputs = ', '.join(example_inputs)
            exec_example = f'python_output = {self.name}({joined_inputs})'
            exec_string = exec_translation + exec_example

            loc: dict = {}
            try:
                exec(exec_string, loc)
                if loc['python_output'] != example_output:
                    return False
            except BaseException:
                raise BaseException('\n' + exec_string)
        return True


class ParsedGrammar:
    """Data class containing parsed (invented) primitives."""

    def __init__(self, primitives: dict, invented: dict) -> None:
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
        # To avoid circular imports, source translation is handled by
        # lapspython.extraction.ProgramExtractor instead of the constructor.
        self.translations: list = []
        self.failed: list = []


class CompactResult:
    """Data class containing (compact) extracted frontiers."""

    def __init__(self, hit: dict, miss: dict) -> None:
        """Store HIT and MISS CompactFrontiers in member variables.

        :param hit: A (name, HIT CompactFrontier) dictionary.
        :type hit: dict
        :param miss: A (name, MISS CompactFrontier) dictionary.
        :type miss: dict
        """
        self.hit_frontiers: dict = hit
        self.miss_frontiers: dict = miss

    def best(self):
        """Return the HIT frontiers with best posteriors.

        :returns: A (name, HIT CompactFrontier) dictionary.
        :rtype: dict
        """
        # TODO: Copy frontiers to only contain 1 program
        return {k: v for k, v in self.hit_frontiers.items()}
