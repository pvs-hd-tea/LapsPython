"""Implements functions for translation from lambda calculus to Python."""

import re
from collections import Counter

from dreamcoder.domains.list.listPrimitives import primitives
from dreamcoder.program import Abstraction, Application, Index, Invented, Primitive, Program
from lapspython.types import ParsedGrammar, ParsedInvented, ParsedPrimitive


class Translator:
    """Translate lambda programs to Python code."""

    def __init__(self, grammar: ParsedGrammar = ParsedGrammar()) -> None:
        self.grammar = grammar
        self.call_counts = {p: 0 for p in self.grammar.primitives}
        self.call_counts.update({i: 0 for i in self.grammar.invented})
        self.args = []
        self.dependencies = set()

    def translate(self, program: Program, name: str = '') -> str:
        """Init variables and call recursive translation function.
        
        :param program: Abstraction/Invented at any depth of lambda expression
        :type program: subclass of dreamcoder.program.Program
        :param name: Task/Function name
        :type name: string, optional
        :returns: Python source code
        :rtype: string
        """
        for call in self.call_counts:
            self.call_counts[call] = 0
        self.args = []
        source = self._translate_program(program)

        dependencies = '\n'.join(self.dependencies) + '\n'

        if name == '':
            return dependencies + source

        header = f'def {name}({", ".join(self.args)}):\n'
        last_variable_assignment = re.findall(r'\w+ =', source)[-1]
        source = 'return'.join(source.split(last_variable_assignment))
        indented_source = re.sub(r'^', '    ', source, flags=re.MULTILINE)
        return dependencies + header + indented_source

    def _translate_program(self, program: Program) -> str:
        """Recursively parse nested lambda expressions under a given grammar.
        
        :param program: Abstraction/Invented at any depth of lambda expression
        :type program: subclass of dreamcoder.program.Program
        """
        if not isinstance(program, (Abstraction, Invented)):
            raise TypeError(f'Encountered unexpected type {type(program)}.')
        if not program.body.isApplication:
            raise TypeError(f'Encountered unexpected type {type(program)}.')

        code, f, x = self._translate_application(program.body)
        self.call_counts[f.name] += 1
        name = f'{f.name}_{self.call_counts[f.name]}'
        print("\ncode:")
        print(code)
        print("\nf:")
        print(f)
        print("\nx:")
        print(x)
        code += f.resolve_variables(x, name) + '\n'
        return code

    def _translate_application(self, application: Application) -> tuple:
        """Parse function and argument of application object.

        :param program: Application object f(x)
        :type program: dreamcoder.type.Application
        :returns: (code, ParsedPrimitive, args) tuple
        :rtype: tuple
        """
        code = ''

        x = application.x
        if x.isIndex:
            x_args = [f'arg{x.i}']
            self.args.append(x_args[0])
        elif x.isPrimitive:
            if isinstance(x.value, str):
                x_args = [f"'{x.value}'"]
            else:
                raise TypeError(f'Encountered unexpected type {type(x)}.')
        elif x.isApplication:
            x_code, x_parsed, x_args = self._translate_application(x)
            self.call_counts[x_parsed.name] += 1
            name = f'{x_parsed.name}_{self.call_counts[x_parsed.name]}'
            code += x_code + x_parsed.resolve_variables(x_args, name) + '\n'
            x_args = [name]
        else:
            raise TypeError(f'Encountered unexpected type {type(x)}.')

        f = application.f
        if f.isPrimitive:
            f_parsed = ParsedPrimitive(f).resolve_lambdas()
            self.dependencies.update(f_parsed.dependencies)
        elif f.isApplication:
            f_code, f_parsed, f_args = self._translate_application(f)
            x_args = f_args + x_args
        else:
            raise TypeError(f'Encountered unexpected type {type(f)}.')
        
        return code, f_parsed, x_args

    def _translate_invented(self, invented: Invented) -> str:
        """Parse invented and argument of invented object.
    
        :param program: Invented object
        :type program: dreamcoder.type.Invented
        """
        parsed_invented = ParsedInvented(invented)
        call_count = self.call_counts.get(str(invented), 0) + 1
        self.call_counts[str(invented)] = call_count
        return parsed_invented.translation
