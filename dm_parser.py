"""
Parser based on the following grammar:

<program>   ::= <statement>+
<statement> ::= <assignment> | <expression>
<assignment>::= <identifier> '=' <expression>
<expression>::= <term> (('+' | '-') <term>)*
<term>      ::= <factor> (('*' | '/') <factor>)*
<factor>    ::= <identifier> | <number> | '(' <expression> ')'

"""

from dm_lexer import TokenType


class Parser:
    """
    The main parser class that performs the parsing based on the grammar rules.
    """

    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.current_token = tokens[0]
        self.index = 0

    def parse(self):
        ast = self.parse_program()
        return ast

    def advance(self):
        """
        Moves the parser to the next token
        """
        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
        self.current_token = None

    def parse_program(self):
        # Collects the statements
        statements = []
        while self.current_token is not None:
            statement = self.parse_statement()
            statements.append(statement)
        return statements

    def parse_statement(self):
        """
        Determines whether the current token represents an assignment or an expression,
        and calls the respective method.
        """
        if (
            self.current_token is not None
            and self.current_token.token_type == TokenType.IDENTIFIER
        ):
            return self.parse_assignemnt()
        else:
            return self.parse_expression()

    def parse_assignemnt(self):
        """
        Parses an assignment statement by extracting the identifier,
        consuming the "=" operator and parsing the expression.
        """
        if self.current_token:
            identifier = Identifier(self.current_token.value)
            self.advance()  # Consume the expression
            self.advance()  # Consume the "="
            expression = self.parse_expression()

            return Assigment(identifier, expression)

    def parse_expression(self):
        """
        Parses an expression by parsing the first term then parsing
        any additional terms with appropiate operators.
        """
        # Parse te first term
        term = self.parse_term()

        # Parse additional terms if there are any
        while self.current_token is not None and self.current_token.token_type in (
            TokenType.PLUS,
            TokenType.MULTIPLY,
        ):
            operator = self.current_token.token_type
            self.advance()  # Consume the operator
            next_term = self.parse_term()
            term = BinaryOperation(term, operator, next_term)

    def parse_term(self):
        """
        Parses a term by parsing the first factor and then parsing any additional
        factors with appropiate operators.
        """
        # Parse the first factor
        factor = self.parse_factor()

        # Parse additional factors if there are any
        while self.current_token is not None and self.current_token.token_type in (
            TokenType.MULTIPLY,
            TokenType.DIVIDE,
        ):
            operator = self.current_token.token_type
            self.advance()  # Consume the operator
            next_factor = self.parse_factor()
            factor = BinaryOperation(factor, operator, next_factor)

        return factor

    def parse_factor(self):
        """
        Parses a factor by checking the type of the current token and handling the
        respective cases (identifier, number or expression with parentheses.)
        """
        if (
            self.current_token is not None
            and self.current_token.token_type == TokenType.IDENTIFIER
        ):
            # Parse an identifier factor
            identifier = Identifier(self.current_token.value)
            self.advance()  # Consume the identifier token
            return identifier

        elif (
            self.current_token is not None
            and self.current_token.token_type == TokenType.NUMBER
        ):
            # Parse a number factor
            number = Number(self.current_token.value)
            self.advance()  # Consume the number token
            return number

        elif (
            self.current_token is not None
            and self.current_token.token_type == TokenType.LEFT_PAREN
        ):
            # Parse an expression within parentheses
            self.advance()  # Consume the left parenthesis token
            expression = self.parse_expression()

            if (
                self.current_token is not None
                and self.current_token.token_type == TokenType.RIGHT_PAREN
            ):
                self.advance()  # Consume the right parenthesis token
                return expression
            else:
                # Handle mismatched parentheses
                raise SyntaxError("Mismatched parentheses")

        else:
            # Handle unexpected token
            raise SyntaxError("Unexpected token")


class BinaryOperation:
    """
    Represents a binary operation with a left operand, an operator and an expression.
    """

    def __init__(self, left, operator, rigth) -> None:
        self.left = left
        self.operator = operator
        self.rigth = rigth


class Assigment:
    """
    Represents an assignment statement with an identifier and an expression.
    """

    def __init__(self, identifier, expression) -> None:
        self.identifier = identifier
        self.expression = expression


class Identifier:
    """
    Reprensents an identifier (variable name)
    """

    def __init__(self, name) -> None:
        self.name = name


class Number:
    """
    Represents a numeric value
    """

    def __init__(self, value) -> None:
        self.value = value
