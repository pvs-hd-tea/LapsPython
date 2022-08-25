"""Implements types for parsed primitives and lambda expressions."""

import copy
import inspect
import random
import re
from abc import ABC, abstractmethod
from typing import Dict, List

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
        self.imports: set = set()
        self.dependencies: set = set()
        self.arg_types: list = []
        self.return_type = type

    @abstractmethod
    def __str__(self) -> str:  # pragma: no cover
        """Convert object to clean code."""
        pass

    def as_dict(self) -> dict:
        """Return member attributes as dict for json dumping."""
        return {
            'name': self.name,
            'handle': self.handle,
            'source': self.source,
            'args': self.args,
            'imports': list(self.imports),
            'dependencies': list(self.dependencies)
        }

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

    def resolve_variables(self, args: list, return_name: str) -> str:
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
            return self.replace_return_statement(return_name, new_source)
        return new_source

    def replace_return_statement(self, return_name, source):
        """Substiture return with variable assignment."""
        pass


class ParsedPythonType(ParsedType):
    """Abstract base class for python parsing."""

    def __str__(self) -> str:
        """Construct clean Python function from object.

        :returns: Function source code
        :rtype: string
        """
        header = f'def {self.name}({", ".join(self.args)}):\n'
        indented_body = re.sub(r'^', '    ', self.source, flags=re.MULTILINE)
        return header + indented_body + '\n'

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

    def replace_return_statement(self, return_name, source):
        """Substiture return with variable assignment."""
        return re.sub('return', f'{return_name} =', source)


class ParsedRType(ParsedType):
    """Abstract base class for R parsing."""

    def __str__(self) -> str:
        """Return parsed primitive as R code.

        :returns: R source code
        :rtype: string
        """
        header = f'{self.name} <- function({", ".join(self.args)} \u007b\n'
        indented_body = re.sub(r'^', '    ', self.source, flags=re.MULTILINE)
        return header + indented_body + '\n}\n'

    def resolve_lambdas(self):
        """No lambdas in R, but required for backwards compatibility."""
        return self

    def replace_return_statement(self, return_name, source):
        """Substiture return with variable assignment."""
        return re.sub(r'return\((.+)\)', fr'{return_name} <- \1', source)


class ParsedPrimitive(ParsedPythonType):
    """Class parsing primitives for translation to clean Python code."""

    def __init__(self, primitive: Primitive) -> None:
        """Construct ParsedPrimitive object with parsed function specs.

        :param primitive: A Primitive object
        :type primitive: dreamcoder.program.Primitive
        """
        implementation = primitive.value

        if inspect.isfunction(implementation):
            args = inspect.getfullargspec(implementation).args
            source = self.parse_source(implementation)
            imports = self.get_imports(implementation)
            dependencies = self.get_dependencies(implementation)
        else:
            args = []
            source = implementation
            imports = set()
            dependencies = []

        self.handle = primitive.name
        self.name = re.sub(r'^[^a-z]+', '', self.handle)
        self.imports = {module for module in imports if module in source}
        self.dependencies = {d[1] for d in dependencies if d[0] in source}
        self.source = source.strip()
        self.args = args
        self.arg_types = self.parse_argument_types(primitive.tp)
        self.return_type = self.arg_types.pop()

    def parse_source(self, implementation) -> str:
        """Resolve lambdas and arguments to produce cleaner Python code.

        :param implementation: The function referenced by primitive
        :type implementation: callable
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

    def get_imports(self, implementation) -> set:
        """Find import modules that might be required by primitives.

        :param implementation: The function referenced by a primitive
        :type implementation: function
        :returns: A set of module names as strings
        :rtype: set
        """
        main_module = inspect.getmodule(implementation)
        imports = inspect.getmembers(main_module, inspect.ismodule)
        return {module[0] for module in imports}

    def get_dependencies(self, implementation) -> list:
        """Find functions called by primitives that are not built-ins.

        :param implementation: The function referenced by a primitive
        :type implementation: function
        :returns: A list of (function name, source) tuples
        :rtype: list
        """
        module = inspect.getmodule(implementation)
        functions = inspect.getmembers(module, inspect.isfunction)
        dependent_functions = [f for f in functions if f[0][:2] == '__']
        return [(f[0], inspect.getsource(f[1])) for f in dependent_functions]


class ParsedRPrimitive(ParsedRType):
    """Abstract base class for R program parsing."""

    def __init__(self, primitive: Primitive):
        """Extract name, path and source of R primitive.

        :param primitive: A primitive extracted from LAPS.
        :type primitive: dreamcoder.program.Primitive
        """
        self.handle = primitive.name
        self.name = re.sub(r'^[^a-z]+', '', self.handle)
        py_implementation = primitive.value

        if inspect.isfunction(py_implementation):
            py_path = inspect.getsourcefile(py_implementation)
            if not isinstance(py_path, str):
                msg = f'Cannot get source of primitive {self.name}.'
                raise ValueError(msg)
            self.path = py_path[:-2] + 'R'
            source = self.parse_source(self.name, self.path)
            imports = self.get_imports(self.path)
            dependencies = self.get_dependencies(primitive.value)
        else:
            source = py_implementation
            imports = set()
            dependencies = set()
            self.args = []

        self.imports = imports
        self.dependencies = {d[1] for d in dependencies if d[0] in source}
        self.source = source.strip()
        self.arg_types = self.parse_argument_types(primitive.tp)
        self.return_type = self.arg_types.pop()

    def parse_source(self, name: str, path: str, is_dep=False) -> str:
        """Extract source code of primitive from R file.

        :param handle: Function name in source file.
        :type handle: string
        :returns: Source code of corresponding function.
        :rtype: string
        """
        with open(path, 'r') as r_file:
            lines = r_file.readlines()

        pattern = f'{name} <- '

        for i in range(len(lines)):
            line = lines[i]
            if line.startswith(pattern):
                if not line.endswith('{\n'):
                    self.args = []
                    return re.sub(pattern, '', line)
                if not is_dep:
                    self.args = self.get_args(line)
                cutoff_lines = lines[i + 1 - is_dep:]
                break

        for j in range(len(cutoff_lines)):
            if cutoff_lines[j] == '}\n':
                return ''.join(cutoff_lines[:j + is_dep])

        raise ValueError(f'No primitive {self.name} found in {self.path}.')

    def get_imports(self, path) -> set:
        """Find import modules that might be required by primitives.

        :param implementation: The function referenced by a primitive
        :type implementation: function
        :returns: A set of module names as strings
        :rtype: set
        """
        pattern = r'library\((.+)\)'
        with open(path, 'r') as r_file:
            return set(re.findall(pattern, r_file.read()))

    def get_dependencies(self, implementation):
        """Find functions called by primitives that are not built-ins.

        :param implementation: The function referenced by a primitive
        :type implementation: function
        :returns: A list of (function name, source) tuples
        :rtype: list
        """
        module = inspect.getmodule(implementation)
        functions = inspect.getmembers(module, inspect.isfunction)
        dependent_functions = [(f[0], f[1])
                               for f in functions if f[0][:2] == '__']
        dependencies = []
        for f in dependent_functions:
            if inspect.isfunction(f[1]):
                path = inspect.getsourcefile(f[1])[:-2] + 'R'
                dependencies.append(
                    (f[0][2:], self.parse_source(f[0][2:], path, True)))
            else:
                dependencies.append((f[0][2:], f[1]))

        return dependencies

    def get_args(self, header: str):
        """Get list of arguments from function code.

        :param source: Function code
        :type source: string
        """
        match = re.search(r'\(.+\)', header)
        if match is None:
            return []
        args = match[0][1:-1]
        return args.split(', ')


class ParsedInvented(ParsedPythonType):
    """Class parsing invented primitives for translation to Python."""

    def __init__(self, invented: Invented, name: str):
        """Construct ParsedInvented object with parsed specs.

        :param invented: An invented primitive object
        :type invented: dreamcoder.program.Invented
        :param name: A custom name since invented primitives are unnamed
        :type name: string
        """
        self.handle = str(invented)
        self.name = name
        self.program = invented
        self.arg_types = self.parse_argument_types(invented.tp)
        self.return_type = self.arg_types.pop()

        # To avoid circular imports, source translation is only handled by
        # lapspython.extraction.GrammarParser instead of during construction.
        self.source = ''
        self.args: list = []
        self.imports: set = set()
        self.dependencies: set = set()

    def resolve_variables(self, args: list, return_name: str) -> str:
        """Instead arguments in function call rather than definition."""
        head = f'{return_name} = '
        body = f'{self.name}({", ".join(args)})'
        return f'{head}{body}'


class ParsedRInvented(ParsedRType):
    """Class parsing invented primitives for translation to R."""

    def __init__(self, invented: Invented, name: str):
        """Construct ParsedRInvented object with parsed specs.

        :param invented: An invented primitive object
        :type invented: dreamcoder.program.Invented
        :param name: A custom name since invented primitives are unnamed
        :type name: string
        """
        self.handle = str(invented)
        self.name = name
        self.program = invented
        self.arg_types = self.parse_argument_types(invented.tp)
        self.return_type = self.arg_types.pop()

        # To avoid circular imports, source translation is only handled by
        # lapspython.extraction.GrammarParser instead of during construction.
        self.source = ''
        self.args: list = []
        self.imports: set = set()
        self.dependencies: set = set()

    def resolve_variables(self, args: list, return_name: str) -> str:
        """Instead arguments in function call rather than definition."""
        head = f'{return_name} <- '
        body = f'{self.name}({", ".join(args)})'
        return f'{head}{body}'


class ParsedProgramBase(ParsedType):
    """Class parsing synthesized programs."""

    def __init__(
        self,
        name: str,
        source: str,
        args: list,
        imports: set,
        dependencies: set
    ):
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
        self.handle = name
        self.name = name
        self.source = source
        self.args = args
        self.imports = imports
        self.dependencies = dependencies

    @abstractmethod
    def __str__(self) -> str:
        """Return imports, dependencies and source code as string.

        :returns: Full source code of translated program
        :rtype: string
        """
        pass

    @abstractmethod
    def verify(self, examples: list) -> bool:
        """Verify code for a list of examples from task.

        :param examples: A list of (input, output) tuples
        :type examples: list
        :returns: Whether the translated program is correct.
        :rtype: bool
        """
        pass


class ParsedProgram(ParsedProgramBase, ParsedType):
    """Class parsing synthesized programs."""

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


class ParsedRProgram(ParsedProgramBase, ParsedRType):
    """Class parsing synthesized programs."""

    def __str__(self) -> str:
        """Return dependencies and source code as string.

        :returns: Full source code of translated program
        :rtype: string
        """
        imports = '\n'.join([f'library({module})' for module in self.imports])
        dependencies = '\n'.join(self.dependencies) + '\n'
        header = f'{self.name} <- function({", ".join(self.args)}) \u007b\n'
        indent_source = re.sub(r'^', '    ', self.source, flags=re.MULTILINE)
        return imports + '\n\n' + dependencies + header + indent_source + '\n}'

    def verify(self, examples: list) -> bool:
        """Verify code for a list of examples from task.

        :param examples: A list of (input, output) tuples
        :type examples: list
        :returns: Whether the translated program is correct.
        :rtype: bool
        """
        return True  # TODO


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

    def as_dict(self):
        """Return member attributes as dict for json dumping."""
        primitives = {p.handle: p.as_dict() for p in self.primitives.values()}
        invented = {i.handle: i.as_dict() for i in self.invented.values()}
        return {
            'primitives': primitives,
            'invented': invented
        }


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
    """Class containing (compact) extracted frontiers."""

    def __init__(self, hit: dict, miss: dict) -> None:
        """Store HIT and MISS CompactFrontiers in member variables.

        :param hit: A (name, HIT CompactFrontier) dictionary.
        :type hit: dict
        :param miss: A (name, MISS CompactFrontier) dictionary.
        :type miss: dict
        """
        self.hit_frontiers: dict = hit
        self.miss_frontiers: dict = miss

    def get_best(self) -> List[Dict]:
        """Return the HIT frontiers as dict with best posteriors.

        :returns: A list of minimal CompactFrontier dictionaries.
        :rtype: List[Dict]
        """
        hits_best = []

        for hit in self.hit_frontiers.values():
            best_valid = best_invalid = None

            if len(hit.translations) > 0:
                best_valid = str(hit.translations[0])
            if len(hit.failed) > 0:
                best_invalid = str(hit.failed[0])

            hit_best = {
                'annotation': hit.annotation,
                'best_program': str(hit.programs[0]),
                'best_valid_translation': best_valid,
                'best_invalid_translation': best_invalid
            }
            hits_best.append(hit_best)

        return hits_best

    def sample(self) -> dict:
        """Return a random HIT frontier with valid translation.

        :returns: A minimal CompactFrontier dictionary.
        :rtype: dict
        """
        best_valid = [best for best in self.get_best()
                      if best['best_valid_translation'] is not None]
        if len(best_valid) > 0:
            return random.choice(best_valid)
        else:
            return {}
