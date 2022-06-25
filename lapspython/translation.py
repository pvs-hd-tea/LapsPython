"""Implements functions for translation from lambda calculus to Python."""

import re

from dreamcoder.program import (Abstraction, Application, Index, Invented,
                                Primitive, Program)
from lapspython.types import ParsedGrammar, ParsedProgram


class Translator:
    """Translate lambda programs to Python code."""

    def __init__(self, grammar: ParsedGrammar) -> None:
        """Init grammar used for translation and empty containers.

        :param grammar: Grammar used for translation
        :type grammar: lapspython.types.ParsedGrammar
        """
        self.grammar = grammar
        self.call_counts = {p: 0 for p in self.grammar.primitives}
        self.call_counts.update({i: 0 for i in self.grammar.invented})
        self.code = ''
        self.args: list = []
        self.dependencies: set = set()

    def translate(self, program: Program, name: str) -> ParsedProgram:
        """Init variables and call recursive translation function.

        :param program: Abstraction/Invented at any depth of lambda expression
        :type program: subclass of dreamcoder.program.Program
        :param name: Task/Function name
        :type name: string
        :returns: Translated program
        :rtype: ParsedProgram
        """
        for call in self.call_counts:
            self.call_counts[call] = 0
        self.code = ''
        self.args = []
        self.dependencies = set()
        self.name = name

        self._translate_wrapper(program)
        source = self.code.strip()
        last_variable_assignments = re.findall(r'\w+ =', source)
        if len(last_variable_assignments) > 0:
            source = 'return'.join(source.split(last_variable_assignments[-1]))

        return ParsedProgram(name, source, self.args, self.dependencies)

    def _translate_wrapper(self, program: Program, node_type: str = 'body'):
        """Redirect node to corresponding translation procedure.

        :param program: Node of program tree.
        :type program: Subclass of dreamcoder.program.Program
        :returns:
        :rtype: tuple
        """
        if program.isAbstraction:
            return self._translate_abstraction(program)
        if program.isApplication:
            if node_type == 'f':
                return self._translate_application_f(program)
            if node_type == 'x':
                return self._translate_application_x(program)
            return self._translate_application_body(program)
        if program.isIndex:
            return self._translate_index(program)
        if program.isInvented:
            if node_type == 'f':
                return self._translate_invented(program)
            return self._translate_abstraction(program)
        if program.isPrimitive:
            if node_type == 'f':
                return self._translate_primitive_f(program)
            if node_type == 'x':
                return self._translate_primitive_x(program)
            return self._translate_primitive_body(program)
        raise ValueError(f'{node_type} node of type {type(program)}')

    def _translate_abstraction(self, abstraction: Abstraction) -> tuple:
        parsed, args = self._translate_wrapper(abstraction.body)
        args = [f'lambda x: {args[0]}']
        return parsed, args

    def _translate_application_f(self, application: Application) -> tuple:
        f = application.f
        x = application.x

        f_parsed, f_args = self._translate_wrapper(f, 'f')
        _, x_args = self._translate_wrapper(x, 'x')

        return f_parsed, f_args + x_args

    def _translate_application_x(self, application: Application) -> tuple:
        f = application.f
        x = application.x

        f_parsed, f_args = self._translate_wrapper(f, 'f')
        x_parsed, x_args = self._translate_wrapper(x, 'x')

        self.call_counts[f_parsed.handle] += 1
        name = f'{f_parsed.name}_{self.call_counts[f_parsed.handle]}'

        if not f.isInvented:
            x_args = f_args + x_args

        f_parsed_resolved = f_parsed.resolve_variables(x_args, name)
        self.code += f_parsed_resolved + '\n'

        return f_parsed, [name]

    def _translate_application_body(self, application: Application) -> tuple:
        f = application.f
        x = application.x

        f_parsed, f_args = self._translate_wrapper(f, 'f')
        x_parsed, x_args = self._translate_wrapper(x, 'x')

        x_args = f_args + x_args

        self.call_counts[f_parsed.handle] += 1
        name = f'{f_parsed.name}_{self.call_counts[f_parsed.handle]}'

        missing_args = len(f_parsed.args) - len(x_args)
        for i in range(missing_args):
            new_arg = f'{self.name}_{i + 1}'
            x_args.append(new_arg)
            self.args.append(new_arg)

        self.code += f_parsed.resolve_variables(x_args, name) + '\n'

        return None, [name]

    def _translate_index(self, index: Index) -> tuple:
        return None, [f'arg{index.i + 1}']

    def _translate_invented(self, invented: Invented) -> tuple:
        handle = str(invented)
        self.call_counts[handle] += 1
        f_parsed = self.grammar.invented[handle]
        if f_parsed.source == '':
            translator = Translator(self.grammar)
            f_trans = translator.translate(f_parsed.program, f_parsed.name)
            f_parsed.source = f_trans.source
            f_parsed.args = f_trans.args
            f_parsed.dependencies = f_trans.dependencies
        self.dependencies.update(f_parsed.dependencies)
        self.dependencies.add(f_parsed.source)
        name = f'{f_parsed.name}_{self.call_counts[handle]}'
        x_args = [name]
        self.code += f_parsed.resolve_variables(x_args, name) + '\n'

        return f_parsed, x_args

    def _translate_primitive_f(self, primitive: Primitive) -> tuple:
        parsed = self.grammar.primitives[primitive.name].resolve_lambdas()
        self.dependencies.update(parsed.dependencies)
        return parsed, []

    def _translate_primitive_x(self, primitive: Primitive) -> tuple:
        return None, [f"'{primitive.value}'"]

    def _translate_primitive_body(self, primitive: Primitive) -> tuple:
        return None, [f"lambda x: '{primitive.value}'"]
