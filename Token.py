#!/usr/bin/env python3

from TokenType import TokenType


class Token:
    def __init__(self, type: TokenType, lexeme: str, literal: object, line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def to_string(self) -> str:
        return f"{self.type} {self.lexeme} {self.literal}"
