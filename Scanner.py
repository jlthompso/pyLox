from Token import Token
from TokenType import TokenType


class Scanner:
    _keywords = {
        'and': TokenType.AND,
        'class': TokenType.CLASS,
        'else': TokenType.ELSE,
        'false': TokenType.FALSE,
        'for': TokenType.FOR,
        'fun': TokenType.FUN,
        'if': TokenType.IF,
        'nil': TokenType.NIL,
        'or': TokenType.OR,
        'print': TokenType.PRINT,
        'return': TokenType.RETURN,
        'super': TokenType.SUPER,
        'this': TokenType.THIS,
        'true': TokenType.TRUE,
        'var': TokenType.VAR,
        'while': TokenType.WHILE,
    }

    def __init__(self, source: str, error):
        self.error = error
        self._source = source
        self._tokens = []
        self._start = 0
        self._current = 0
        self._line = 1

    def scan_tokens(self) -> list[Token]:
        while not self._is_at_end():
            self._start = self._current
            self._scan_token()

        self._tokens.append(Token(TokenType.EOF, "", None, self._line))
        return self._tokens

    def _scan_token(self) -> None:
        match c := self._advance():
            case '(': self._add_token(TokenType.LEFT_PAREN)
            case ')': self._add_token(TokenType.RIGHT_PAREN)
            case '{': self._add_token(TokenType.LEFT_BRACE)
            case '}': self._add_token(TokenType.RIGHT_BRACE)
            case ',': self._add_token(TokenType.COMMA)
            case '.': self._add_token(TokenType.DOT)
            case '-': self._add_token(TokenType.MINUS)
            case '+': self._add_token(TokenType.PLUS)
            case ';': self._add_token(TokenType.SEMICOLON)
            case '*': self._add_token(TokenType.STAR)
            case '!': self._add_token(TokenType.BANG_EQUAL if self._match('=') else TokenType.BANG)
            case '=': self._add_token(TokenType.EQUAL_EQUAL if self._match('=') else TokenType.EQUAL)
            case '<': self._add_token(TokenType.LESS_EQUAL if self._match('=') else TokenType.LESS)
            case '>': self._add_token(TokenType.GREATER_EQUAL if self._match('=') else TokenType.GREATER)
            case '/':
                if self._match('/'):
                    # comment continues to end of line
                    while self._peek() != '\n' and not self._is_at_end(): self._advance()
                else:
                    self._add_token(TokenType.SLASH)
            case ' ': pass  # ignore whitespace
            case '\r': pass  # ignore whitespace
            case '\t': pass  # ignore whitespace
            case '\n': self._line += 1
            case '"': self._string()
            case _:
                if self._is_digit(c):
                    self._number()
                elif self._is_alpha(c):
                    self._identifier()
                else:
                    self.error(self._line, "Unexpected character.")

    def _identifier(self) -> None:
        while self._is_alphanumeric(self._peek()): self._advance()
        text = self._source[self._start:self._current]
        self._add_token(self._keywords[text] if text in self._keywords else TokenType.IDENTIFIER)

    def _number(self) -> None:
        while self._is_digit(self._peek()): self._advance()
        if self._peek() == '.' and self._peek_next().isdigit():
            self._advance()  # add decimal point
            while self._is_digit(self._peek()): self._advance()
        self._add_token(TokenType.NUMBER, float(self._source[self._start:self._current]))

    def _string(self) -> None:
        while (c := self._peek()) != '"' and not self._is_at_end():
            if c == '\n': self._line += 1
            self._advance()

        if self._is_at_end():
            self.error(self._line, "Unterminated string.")
            return

        self._advance()  # advance to closing "
        # trim surrounding quotes
        self._add_token(TokenType.STRING, self._source[self._start + 1:self._current - 1])

    def _match(self, expected: str) -> bool:
        if self._is_at_end(): return False
        if self._source[self._current] != expected: return False
        self._current += 1
        return True

    def _peek(self) -> str:
        return '' if self._is_at_end() else self._source[self._current]

    def _peek_next(self) -> str:
        return '' if self._current + 1 >= len(self._source) else self._source[self._current + 1]

    def _is_alpha(self, c: str) -> bool:
        return 'a' <= c <= 'z' or 'A' <= c <= 'Z' or c == '_'

    def _is_alphanumeric(self, c: str) -> bool:
        return self._is_alpha(c) or self._is_digit(c)

    def _is_digit(self, c: str) -> bool:
        return '0' <= c <= '9'

    def _is_at_end(self) -> bool:
        return self._current >= len(self._source)

    def _advance(self) -> str:
        self._current += 1
        return self._source[self._current - 1]

    def _add_token(self, type: TokenType, literal: object = None) -> None:
        self._tokens.append(Token(type, self._source[self._start:self._current], literal, self._line))
