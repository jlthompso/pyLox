#!/usr/bin/env python3

import tool.Expr as Expr
from Token import Token
from TokenType import TokenType


class AstPrinter(Expr.Visitor):
    def __init__(self) -> None:
        super().__init__()

    def print(self, expr: Expr.Expr) -> str:
        return expr.accept(self)

    def visit_binary_expr(self, expr: Expr.Binary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: Expr.Grouping) -> str:
        return self.parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: Expr.Literal) -> str:
        if expr.value is None: return "nil"
        return str(expr.value)

    def visit_unary_expr(self, expr: Expr.Unary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name: str, *args: Expr.Expr) -> str:
        output = f"({name}"
        for expr in args:
            output += " " + expr.accept(self)
        output += ')'
        return output


if __name__ == '__main__':
    expression = Expr.Binary(
        Expr.Unary(
            Token(TokenType.MINUS, "-", None, 1),
            Expr.Literal(123),
        ),
        Token(TokenType.STAR, "*", None, 1),
        Expr.Grouping(
            Expr.Literal(45.67)
        ),
    )

    print(AstPrinter().print(expression))
