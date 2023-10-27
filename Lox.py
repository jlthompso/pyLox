#!/usr/bin/env python3
import argparse
import sys
from Scanner import Scanner
from Token import Token
from TokenType import TokenType
from Parser import Parser
from AstPrinter import AstPrinter


class Lox:
    def __init__(self, path):
        self.had_error = False
        if path:
            self._run_file(path)
        else:
            self._run_prompt()

    def _run_file(self, path: str) -> None:
        with open(path, 'r') as f:
            self._run(f.read())
        if self.had_error: exit(65)

    def _run_prompt(self) -> None:
        while True:
            if not (line := input("> ")):
                break
            self._run(line)
            self.had_error = False

    def _run(self, source: str) -> None:
        scanner = Scanner(source, self.error)
        tokens = scanner.scan_tokens()
        parser = Parser(self, tokens)
        expression = parser.parse()
        if self.had_error: return
        print(AstPrinter().print(expression))

    def error(self, loc: Token | int, message: str) -> None:
        if isinstance(loc, Token):
            token = loc
            if token.type == TokenType.EOF:
                self._report(token.line, " at end", message)
            else:
                self._report(token.line, f" at '{token.lexeme}'", message)
        else:
            line = loc
            self._report(line, "", message)

    def _report(self, line: int, where: str, message: str):
        print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
        self.had_error = True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run Lox code.")
    parser.add_argument('script',
                        nargs='?',
                        type=str,
                        help="path to Lox source code file (enter REPL if not specified)",
                        )
    Lox(parser.parse_args().script)
