#!/usr/bin/env python3


import argparse
import os
import typing


class GenerateAst:
    def __init__(self, output_dir) -> None:
        self.define_ast(output_dir, "Expr", [
            "Binary     : left: Expr, operator: Token, right: Expr",
            "Grouping   : expression: Expr",
            "Literal    : value: object",
            "Unary      : operator: Token, right: Expr",
        ])

    def define_ast(self, output_dir: str, base_name: str, types: list[str]) -> None:
        fname = base_name + '.py'
        fpath = os.path.join(output_dir, fname) if output_dir else './' + fname
        with open(fpath, 'w') as f:
            f.writelines(line + '\n' for line in [
                "#!/usr/bin/env python3",
                "",
                "from __future__ import annotations",
                "import Token",
                "from abc import ABC, abstractmethod",
                "",
                "",
                f"class {base_name}(ABC):",
                "    def __init__(self):",
                "        super().__init__()",
                "",
                "    @abstractmethod",
                f"    def accept(self, visitor: Visitor):",
                "        pass",
                "",
                "",
                "class Visitor(ABC):",
                "    def __init__(self):",
                "        super().__init__()",
            ])

            self.define_visitor(f, base_name, types)

            # the AST classes
            for type in types:
                class_name = type.split(':')[0].strip()
                fields = type.split(':', maxsplit=1)[1].strip()
                self.define_type(f, base_name, class_name, fields)

    def define_visitor(self, f: typing.TextIO, base_name: str, types: list[str]) -> None:
        base_name = base_name.lower()
        for type in types:
            type_name = type.split(':')[0].strip()
            f.writelines(line + '\n' for line in [
                "",
                "    @abstractmethod",
                f"    def visit_{type_name.lower()}_{base_name}(self, {base_name}: {type_name}):",
                "        pass",
            ])

    def define_type(self, f: typing.TextIO, base_name: str, class_name: str, fields: str) -> None:
        field_names = [field_name.split(':')[0] for field_name in fields.split(', ')]

        f.writelines(line + '\n' for line in [
            "",
            "",
            f"class {class_name}({base_name}):",
            f"    def __init__(self, {fields}):",
            "        super().__init__()",
        ])

        for name in field_names:
            f.write(f"        self.{name} = {name}\n")

        f.writelines(line + '\n' for line in [
            "",
            "    def accept(self, visitor: Visitor):",
            f"        return visitor.visit_{class_name.lower()}_{base_name.lower()}(self)",
        ])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate Lox expression types.")
    parser.add_argument('-o', '--output',
                        metavar='',
                        required=False,
                        type=str,
                        help="path to write generated source code (current directory if not specified)",
                        )
    GenerateAst(parser.parse_args().output)
