"""Implements types for parsed primitivies and lambda expressions."""

import re


class ParsedPrimitive:
    """Data class containing name, source and list of args of a function."""

    def __init__(self, name: str, source: str, args: list):
        """Construct primitive object with parsed function specs.

        :param name: function name
        :param source: source code (body) of the function
        :param args: argument names of the function
        """
        if type(name) != str:
            raise TypeError('name must be a non-empty string.')
        if name == '':
            raise ValueError('name must be a non-empty string.')
        if type(source) != str:
            raise TypeError('source must be a non-empty string.')
        if source == '':
            raise ValueError('source must be a non-empty string.')
        if type(args) not in (list, tuple):
            raise TypeError('args must be a list or tuple of strings.')
        if not all(type(arg) == str for arg in args):
            raise TypeError('args must be a list or tuple of strings.')

        self.name = name
        self.source = source
        self.args = args

    # Will later be moved to translation module
    def resolve(self, args: list) -> str:
        """Substitute default arguments in source.

        :param args: list of argument names (number must be equal)
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
