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
        self.code: list = []
        self.args: list = []
        self.dependencies: set = set()
        self.debug_stack: list = []

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
        self.code = []
        n_args = len(program.infer().arguments) - 1
        self.args = [f'arg{i + 1}' for i in range(n_args)]
        self.dependencies = set()
        self.name = name
        self.debug_stack = []

        self._translate_wrapper(program)
        source = '\n'.join(self.code)
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
        self.debug_stack.append((program, type(program), node_type))
        if program.isAbstraction:
            if node_type == 'x':
                return self._translate_abstraction_x(program)
            return self._translate_abstraction_body(program)
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
            return self._translate_abstraction_body(program)
        if program.isPrimitive:
            if node_type == 'f':
                return self._translate_primitive_f(program)
            if node_type == 'x':
                return self._translate_primitive_x(program)
            return self._translate_primitive_body(program)
        raise ValueError(f'{node_type} node of type {type(program)}')

    def _translate_abstraction_body(self, abstraction: Abstraction) -> tuple:
        parsed, args = self._translate_wrapper(abstraction.body)
        args = [f'lambda x: {args[0]}']
        return parsed, args

    def _translate_abstraction_x(self, abstraction: Abstraction) -> tuple:
        parsed, args = self._translate_wrapper(abstraction.body)

        if self.contains_index(abstraction):
            last_row = self.code.pop()
            body = last_row.split(' = ')[-1]
            body = re.sub(r'arg\d', 'x', body)
            args = [f'lambda x: {body}']
        else:
            args = [f'lambda x: {args[0]}']

        return parsed, args

    def _translate_application_f(self, application: Application) -> tuple:
        f = application.f
        x = application.x

        _, x_args = self._translate_wrapper(x, 'x')
        f_parsed, f_args = self._translate_wrapper(f, 'f')

        return f_parsed, f_args + x_args

    def _translate_application_x(self, application: Application) -> tuple:
        f = application.f
        x = application.x

        x_parsed, x_args = self._translate_wrapper(x, 'x')
        f_parsed, f_args = self._translate_wrapper(f, 'f')

        if x_args[-1][:3] == 'arg' and x_args[-1] not in self.args:
            x_args[-1] = self.get_last_variable()

        self.call_counts[f_parsed.handle] += 1
        name = f'{f_parsed.name}_{self.call_counts[f_parsed.handle]}'

        if not f.isInvented:
            x_args = f_args + x_args

        f_parsed_resolved = f_parsed.resolve_variables(x_args, name)
        self.code.append(f_parsed_resolved)

        return f_parsed, [name]

    def _translate_application_body(self, application: Application) -> tuple:
        f = application.f
        x = application.x

        x_parsed, x_args = self._translate_wrapper(x, 'x')
        f_parsed, f_args = self._translate_wrapper(f, 'f')

        x_args = f_args + x_args

        self.call_counts[f_parsed.handle] += 1
        name = f'{f_parsed.name}_{self.call_counts[f_parsed.handle]}'

        missing_args = len(f_parsed.args) - len(x_args)
        for i in range(missing_args):
            new_arg = f'arg{i + 1}'
            if new_arg in self.args:
                x_args.append(new_arg)

        f_parsed_resolved = f_parsed.resolve_variables(x_args, name)
        self.code.append(f_parsed_resolved)

        return None, [name]

    def _translate_index(self, index: Index) -> tuple:
        arg = f'arg{index.i + 1}'
        return None, [arg]

    def _translate_invented(self, invented: Invented) -> tuple:
        handle = str(invented)
        f_parsed = self.grammar.invented[handle]
        if f_parsed.source == '':
            translator = Translator(self.grammar)
            f_trans = translator.translate(f_parsed.program, f_parsed.name)
            f_parsed.source = f_trans.source
            f_parsed.args = f_trans.args
            f_parsed.dependencies = f_trans.dependencies
        self.dependencies.update(f_parsed.dependencies)
        self.dependencies.add(str(f_parsed))
        name = f'{f_parsed.name}_{self.call_counts[handle]}'
        x_args = [name]

        return f_parsed, x_args

    def _translate_primitive_f(self, primitive: Primitive) -> tuple:
        parsed = self.grammar.primitives[primitive.name].resolve_lambdas()
        self.dependencies.update(parsed.dependencies)
        return parsed, []

    def _translate_primitive_x(self, primitive: Primitive) -> tuple:
        return None, [f"'{primitive.value}'"]

    def _translate_primitive_body(self, primitive: Primitive) -> tuple:
        return None, [f"'{primitive.value}'"]

    def contains_index(self, program: Program) -> bool:
        """Test whether the subprogram contains a de Bruijin index."""
        if program.isIndex:
            return True
        if program.isPrimitive:
            return False
        if 'body' in dir(program):
            return self.contains_index(program.body)
        else:
            f = self.contains_index(program.f)
            x = self.contains_index(program.x)
            return (f or x)

    def get_last_variable(self) -> str:
        """Return the declared variable in the last line of code."""
        return self.code[-1].split(' = ')[0]
