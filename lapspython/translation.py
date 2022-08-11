"""Implements functions for translation from lambda calculus to Python."""

import logging
import re
import traceback

from dreamcoder.program import (Abstraction, Application, Index, Invented,
                                Primitive, Program)
from lapspython.types import (ParsedGrammar, ParsedProgram, ParsedProgramBase,
                              ParsedRProgram, ParsedType)



class Translator:
    """Translate lambda programs to Python code."""

    def __init__(self, grammar: ParsedGrammar, mode='python') -> None:
        """Init grammar used for translation and empty containers.

        :param grammar: Grammar used for translation
        :type grammar: lapspython.types.ParsedGrammar
        """
        self.mode = mode.lower()
        if self.mode not in ('python', 'r'):
            raise ValueError('mode must be "Python" or "R".')

        if self.mode == 'python':
            self.sep = ' = '
        else:
            self.sep = ' <- '

        self.grammar = grammar
        self.call_counts = {p: 0 for p in self.grammar.primitives}
        self.call_counts.update({i: 0 for i in self.grammar.invented})
        self.code: list = []
        self.args: list = []
        self.imports: set = set()
        self.dependencies: set = set()
        self.debug_stack: list = []
        self.logger = self.setup_logger()

    def setup_logger(self) -> logging.Logger:
        """Write debug stack into translation.log in case of exception."""
        logger = logging.getLogger(__name__)
        handler = logging.FileHandler('translation.log', 'w')
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(handler)
        return logger

    def log_exception(self):
        """Write logging message into translation.log."""
        self.logger.debug(f'{self.name}\n')
        for entry in self.debug_stack:
            self.logger.debug(entry)
        if len(self.code) > 0:
            code = '\n'.join(self.code)
            self.logger.debug(f'\n{code}')
        self.logger.debug(f'\n{traceback.format_exc()}\n')

    def translate(self, program: Program, name: str) -> ParsedProgramBase:
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
        self.name = name
        arg_types = ParsedType.parse_argument_types(program.infer())
        n_args = len(arg_types) - 1
        self.args = [f'arg{i + 1}' for i in range(n_args)]
        self.imports = set()
        self.dependencies = set()
        self.name = name
        self.debug_stack = []

        self._translate_wrapper(program)

        source = '\n'.join(self.code)

        if self.mode == 'python':
            last_variable_assignments = re.findall(r'\w+ = ', source)
            if len(last_variable_assignments) > 0:
                split = source.split(last_variable_assignments[-1])
                source = 'return '.join(split)

            return ParsedProgram(
                name,
                source,
                self.args,
                self.imports,
                self.dependencies
            )

        return ParsedRProgram(
            name,
            source,
            self.args,
            self.imports,
            self.dependencies
        )

    def _translate_wrapper(self, program: Program, node_type: str = 'body'):
        """Redirect node to corresponding translation procedure.

        :param program: Node of program tree.
        :type program: Subclass of dreamcoder.program.Program
        :returns:
        :rtype: tuple
        """
        debug = (str(program), str(type(program)), node_type)
        self.debug_stack.append(', '.join(debug))

        if program.isAbstraction:
            return self._translate_abstraction(program)
        if program.isApplication:
            return self._translate_application(program)
        if program.isIndex:
            return self._translate_index(program)
        if program.isInvented:
            if node_type == 'f':
               return self._translate_invented(program)
            return self._translate_abstraction(program)  # unparsed invented
        if program.isPrimitive:
            if node_type == 'f':
                return self._translate_primitive_f(program)
            return self._translate_primitive_x(program)
        raise ValueError(f'{node_type} node of type {type(program)}')

    def _translate_abstraction(self, abstraction: Abstraction) -> tuple:
        return self._translate_wrapper(abstraction.body)

    def _translate_application(self, application: Application) -> tuple:
        f, xs = application.applicationParse()
        x_args = []

        for x in xs:
            x_parsed, x_parsed_resolved = self._translate_wrapper(x, 'x')

            if x.isAbstraction:
                try:
                    x_arg = self.convert_func_to_lambda(x_parsed_resolved)
                except TypeError:
                    print(type(x), x_parsed, x_parsed_resolved)
                    raise
            elif not isinstance(x_parsed, str):
                x_arg = x_parsed.name
            else:
                x_arg = x_parsed
                
            x_args.append(x_arg)

        f_parsed, _ = self._translate_wrapper(f, 'f')

        if f.isIndex:
            return f_parsed, None

        self.call_counts[f_parsed.handle] += 1
        name = f'{f_parsed.name}_{self.call_counts[f_parsed.handle]}'
        f_parsed_resolved = f_parsed.resolve_variables(x_args, name)
        self.code.append(f_parsed_resolved)

        return name, f_parsed_resolved

    def _translate_index(self, index: Index) -> tuple:
        arg = f'arg{index.i + 1}'
        return arg, arg

    def _translate_invented(self, invented: Invented) -> tuple:
        handle = str(invented)
        f_parsed = self.grammar.invented[handle]
        if f_parsed.source == '':
            translator = Translator(self.grammar, self.mode)
            f_trans = translator.translate(f_parsed.program, f_parsed.name)
            f_parsed.source = f_trans.source
            f_parsed.args = f_trans.args
            f_parsed.dependencies = f_trans.dependencies
        self.imports.update(f_parsed.imports)
        self.dependencies.update(f_parsed.dependencies)
        self.dependencies.add(str(f_parsed))
        name = f'{f_parsed.name}_{self.call_counts[handle]}'
        x_args = [name]

        return f_parsed, x_args

    def _translate_primitive_f(self, primitive: Primitive) -> tuple:
        parsed = self.grammar.primitives[primitive.name].resolve_lambdas()
        self.imports.update(parsed.imports)
        self.dependencies.update(parsed.dependencies)
        return parsed, ''

    def _translate_primitive_x(self, primitive: Primitive) -> tuple:
        return f"'{primitive.value}'", f"'{primitive.value}'"

    def convert_arg_to_lambda(self, arg: str) -> str:
        """Convert variable to anonymous function."""
        if self.mode == 'python':
            return f'lambda lx: {arg}'
        if self.mode == 'r':
            return f'function(lx) {arg}'

    def convert_func_to_lambda(self, func: str) -> str:
        """Convert variable assignment to anonymous function."""
        lambda_head = ''
        if self.mode == 'python':
            lambda_head = 'lambda lx: '
        elif self.mode == 'r':
            lambda_head = 'function(lx) '
        body = re.sub(r'\w+ = ', '', func)
        body = re.sub(r'arg\d', 'lx', body)
        return f'{lambda_head}{body}'

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
        if len(self.code) == 0:
            return ''
        return self.code[-1].split(self.sep)[0]
