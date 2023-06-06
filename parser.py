"""
Parser based on the following grammar:

<program>   ::= <statement>+
<statement> ::= <assignment> | <expression>
<assignment>::= <identifier> '=' <expression>
<expression>::= <term> (('+' | '-') <term>)*
<term>      ::= <factor> (('*' | '/') <factor>)*
<factor>    ::= <identifier> | <number> | '(' <expression> ')'

"""
from .lexer import TokenType


class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.current_token = tokens[0]
        self.index = 0

    def parse(self):
        ast = self.parse_program()
        return ast

    def advance(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
        else:
            self.current_token = None

    def parse_program(self):
        statements = []
        while self.current_token is not None:
            statement = self.parse_statement()
            statements.append(statement)
        return statements

    def parse_statement(self):
        if (
            self.current_token is not None
            and self.current_token.token_type == TokenType.IDENTIFIER
        ):
            return self.parse_assignemnt()
        else:
            return self.parse_expression()

    def parse_assignemnt(self):
        if self.current_token:
            identifier = Identifier(self.current_token.value)
            self.advance()  # Consume the expression
            self.advance()  # Consume the "="
            expression = self.parse_expression()

            return Assigment(identifier, expression)

    def parse_expression(self):
        pass


class Assigment:
    def __init__(self, identifier, expression) -> None:
        self.identifier = identifier
        self.expression = expression


class Identifier:
    def __init__(self, name) -> None:
        self.name = name
