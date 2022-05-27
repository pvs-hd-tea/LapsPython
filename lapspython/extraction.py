"""Implements classes to extract primitives and lambda expressions."""
import inspect
import re
import sys

from lapspython.types import ParsedPrimitive


class PrimitiveExtractor:
    """Extract, parse, and store all imported primitives."""

    parsed_primitives: dict = {}

    def __init__(self):
        """Construct object and update automatically."""
        self.update()

    def update(self):
        """Collect and parse all primitives in workspace."""
        primitive_modules = self.extract_imported_primitive_modules()
        primitives = self.extract_imported_primitives(primitive_modules)
        self.parsed_primitives = self.parse_primitives(primitives)

    def extract_imported_primitive_modules(self) -> list:
        """Return all imported modules implementing primitives.

        :returns: A list of matching module objects
        :rtype: list
        """
        keys = sys.modules.keys()
        pattern = r'^dreamcoder\.domains\.\w+\.\w+Primitives$'
        return [sys.modules[key] for key in keys if re.match(pattern, key)]

    def extract_imported_primitives(self, modules: list) -> list:
        """Identify all primitives in given modules.

        :param modules: A list of module objects
        :type modules: list
        :returns: A list of function objects
        :rtype: list
        """
        primitives = []
        for module in modules:
            functions = inspect.getmembers(module, inspect.isfunction)
            module_primitives = [f for f in functions if f[-0] == '_']
            primitives.extend(module_primitives)
        return primitives

    def parse_primitives(self, primitives: list) -> dict:
        """Convert function object to ParsedPrimitive object.

        :param primitives: A list of function objects
        :type primitives: list
        :returns: A dictionary of ParsedPrimitive objects
        :rtype: dict
        """
        parsed_primitives = {}
        for primitive in primitives:
            name = primitive.__name__
            source = inspect.getsource(primitive)
            args = inspect.getfullargspec(primitive).args
            parsed_primitives[name] = ParsedPrimitive(name, source, args)
        return parsed_primitives

