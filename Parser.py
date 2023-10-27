from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Lox import Lox
from Token import Token
from TokenType import TokenType
from tool.Expr import Expr, Binary, Grouping, Literal, Unary


class Parser:
    def __init__(self, interpreter: Lox, tokens: list[Token]) -> None:
        self.tokens = tokens
        self._current = 0
        self.interpreter = interpreter

    class ParseError(SyntaxError):
        pass

    def parse(self) -> Expr | None:
        try:
            return self._expression()
        except self.ParseError:
            return None

    def _expression(self) -> Expr:
        return self._equality()

    def _equality(self) -> Expr:
        expr: Expr = self._comparison()
        while self._match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator: Token = self._previous()
            right: Expr = self._comparison()
            expr = Binary(expr, operator, right)
        return expr

    def _comparison(self) -> Expr:
        expr: Expr = self._term()
        while self._match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator: Token = self._previous()
            right: Expr = self._term()
            expr = Binary(expr, operator, right)
        return expr

    def _term(self) -> Expr:
        expr: Expr = self._factor()
        while self._match(TokenType.MINUS, TokenType.PLUS):
            operator: Token = self._previous()
            right: Expr = self._factor()
            expr = Binary(expr, operator, right)
        return expr

    def _factor(self) -> Expr:
        expr: Expr = self._unary()
        while self._match(TokenType.SLASH, TokenType.STAR):
            operator: Token = self._previous()
            right: Expr = self._factor()
            expr = Binary(expr, operator, right)
        return expr

    def _unary(self) -> Expr:
        if self._match(TokenType.BANG, TokenType.MINUS):
            operator: Token = self._previous()
            right: Expr = self._unary()
            return Unary(operator, right)
        return self._primary()

    def _primary(self) -> Expr:
        if self._match(TokenType.FALSE): return Literal(False)
        if self._match(TokenType.TRUE): return Literal(True)
        if self._match(TokenType.NIL): return Literal(None)

        if self._match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self._previous().literal)

        if self._match(TokenType.LEFT_PAREN):
            expr: Expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        raise self._error(self._peek(), "Expect expression.")

    def _match(self, *types: TokenType) -> bool:
        for type in types:
            if self._check(type):
                self._advance()
                return True
        return False

    def _consume(self, type: TokenType, message: str) -> Token:
        if self._check(type): return self._advance()
        raise self._error(self._peek(), message)

    def _check(self, type: TokenType) -> bool:
        if self._is_at_end(): return False
        return self._peek().type == type

    def _advance(self) -> Token:
        if not self._is_at_end(): self._current += 1
        return self._previous()

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _peek(self) -> Token:
        return self.tokens[self._current]

    def _previous(self) -> Token:
        return self.tokens[self._current - 1]

    def _error(self, token: Token, message: str) -> ParseError:
        self.interpreter.error(token, message)
        return self.ParseError(SyntaxError)

    def _synchronize(self) -> None:
        self._advance()
        while not self._is_at_end():
            if self._previous().type == TokenType.SEMICOLON: return
            match self._peek().type:
                case TokenType.CLASS | TokenType.FOR | TokenType.FUN | TokenType.IF | TokenType.PRINT \
                     | TokenType.RETURN | TokenType.VAR | TokenType.WHILE:
                    return
            self._advance()
