"""Implements classes to extract primitives and lambda expressions."""
import inspect
import re
import sys

from lapspython.types import ParsedPrimitive


class PrimitiveExtractor:
    """Extract, parse, and store all imported primitives."""

    parsed_primitives: dict = {}

    def extract(self):
        """Collect and parse all primitives in workspace."""
        primitive_modules = self.__extract_imported_primitive_modules()
        primitives = self.__extract_imported_primitives(primitive_modules)
        self.parsed_primitives = self.__parse_primitives(primitives)
        return self.parsed_primitives

    def __extract_imported_primitive_modules(self) -> list:
        """Return all imported modules implementing primitives.

        :returns: A list of matching module objects
        :rtype: list
        """
        keys = sys.modules.keys()
        pattern = r'^\w+\.domains\.\w+\.\w+Primitives$'
        return [sys.modules[key] for key in keys if re.match(pattern, key)]

    def __extract_imported_primitives(self, modules: list) -> list:
        """Identify all primitives in given modules.

        :param modules: A list of module objects
        :type modules: list
        :returns: A list of function objects
        :rtype: list
        """
        primitives = []
        for module in modules:
            function_pairs = inspect.getmembers(module, inspect.isfunction)
            functions = [f_pair[1] for f_pair in function_pairs]
            module_primitives = [f for f in functions if f.__name__[0] == '_']
            primitives.extend(module_primitives)
        return primitives

    def __parse_primitives(self, primitives: list) -> dict:
        """Convert function object to ParsedPrimitive object.

        :param primitives: A list of function objects
        :type primitives: list
        :returns: A dictionary of ParsedPrimitive objects
        :rtype: dict
        """
        parsed_primitives = {}
        for primitive in primitives:
            name = primitive.__name__
            args = inspect.getfullargspec(primitive).args

            source = inspect.getsource(primitive)
            source = source[source.find(':') + 1:]
            indent = re.search(r'\w', source).start()
            if indent == 1:
                source = source[indent:]
            else:
                source = re.sub(r'^\n', '', source)
                source = re.sub(r'^ {4}', '', source, flags=re.MULTILINE)
            source = re.sub(r'\n$', '', source)

            parsed_primitives[name] = ParsedPrimitive(name, source, args)
        return parsed_primitives

