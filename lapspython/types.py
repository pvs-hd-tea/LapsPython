"""Implements types for parsed primitives and lambda expressions."""

import copy
import inspect
import re

from dreamcoder.program import Primitive
from dreamcoder.type import TypeConstructor, TypeVariable


class ParsedPrimitive:
    """Class parsing primitives for translation to clean Python code."""

    def __init__(self, primitive: Primitive):
        """Construct primitive object with parsed function specs.

        :param primitive: A Primitive object
        :type primitive: Primitive
        """
        implementation = primitive.value

        if inspect.isfunction(implementation):
            args = inspect.getfullargspec(implementation).args
            source = inspect.getsource(implementation)

            source = source[source.find(':') + 1:]
            indent = re.search(r'\w', source).start()
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
        self.arg_types = self.parse_argument_types(primitive.infer())
        self.return_type = self.arg_types.pop()

    def __str__(self):
        """Construct Python function from object.

        :returns: function source code
        :rtype: string
        """
        header = f'def {self.name}({", ".join(self.args)}):\n'
        indented_body = re.sub(r'^', '    ', self.source, flags=re.MULTILINE)
        return header + indented_body

    def parse_argument_types(self, arg_types: TypeConstructor) -> list:
        """Flatten inferred nested type structure of primitive.

        :param arg_types: arg_types: Inferred types.
        :type arg_types: TypeConstructor
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

