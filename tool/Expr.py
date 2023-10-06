#!/usr/bin/env python3

from __future__ import annotations
import Token
from abc import ABC, abstractmethod


class Expr(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def accept(self, visitor: Visitor):
        pass


class Visitor(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def visit_binary_expr(self, expr: Binary):
        pass

    @abstractmethod
    def visit_grouping_expr(self, expr: Grouping):
        pass

    @abstractmethod
    def visit_literal_expr(self, expr: Literal):
        pass

    @abstractmethod
    def visit_unary_expr(self, expr: Unary):
        pass


class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr) -> None:
        super().__init__()
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor):
        return visitor.visit_binary_expr(self)


class Grouping(Expr):
    def __init__(self, expression: Expr) -> None:
        super().__init__()
        self.expression = expression

    def accept(self, visitor: Visitor):
        return visitor.visit_grouping_expr(self)


class Literal(Expr):
    def __init__(self, value: object) -> None:
        super().__init__()
        self.value = value

    def accept(self, visitor: Visitor):
        return visitor.visit_literal_expr(self)


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr) -> None:
        super().__init__()
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor):
        return visitor.visit_unary_expr(self)
