from enum import Enum


# We need to set the token types
class TokenType(Enum):
    """Simple enum that holds the token types"""
    IDENTIFIER = "IDENTIFIER "
    NUMBER = "NUMBER"
    ASSIGN = "ASSIGN"
    PLUS = "PLUS"
    MULTIPLY = "MULTIPLY"
    NEWLINE = "NEWLINE"
    COMMENT = "COMMENT"


# We need to create the lexer class
class Lexer:
    """Helps to tokenize the characters in the source code."""
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0
        self.current_char = source_code[0]

    def advance(self):
        """Moves to the next character"""
        # Increas the position by 1
        self.position += 1
        # If the position is less than the length of the source code
        if self.position < len(self.source_code):
            # Set the current_char to the character at position self.position
            self.current_char = self.source_code[self.position]
        else:
            self.current_char = None

    def tokenize(self):
        """Checks if the current chart meets any of the predifined criteria"""
        tokens = []

        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()
            elif self.current_char.isalpha():
                tokens.append(self.tokenize_identifier())
            elif self.current_char.isdigit():
                tokens.append(self.tokenize_number())
            elif self.current_char == "=":
                tokens.append(Token(TokenType.ASSIGN, self.current_char))
                self.advance()
            elif self.current_char == "+":
                tokens.append(Token(TokenType.PLUS, self.current_char))
                self.advance()
            elif self.current_char == "*":
                tokens.append(Token(TokenType.MULTIPLY, self.current_char))
                self.advance()
            elif self.current_char == "\n":
                tokens.append(Token(TokenType.NEWLINE, self.current_char))
                self.advance()
            # Handle comments
            elif self.current_char == "/":
                # Check if it's a comment
                if self.peek() == "/":
                    # We call self.advance twice to skip the comments
                    self.advance()
                    self.advance()

                    # Advance until there is a new line
                    while self.current_char is not None and self.current_char != "\n":
                        self.advance()
                else:
                    raise SyntaxError(f"Invalid character: {self.current_char}")
            else:
                raise SyntaxError(f"Invalid character: {self.current_char}")

        return tokens

    def tokenize_number(self):
        """Tokenizes the numbers"""
        number = ""
        # Loop through the characters until the character is None or not a number
        while self.current_char is not None and self.current_char.isdigit():
            number += self.current_char
            self.advance()
        return Token(TokenType.NUMBER, number)

    # TODO: Revisit and comment
    def tokenize_identifier(self):
        identifier = ""
        # Loops until char is None or if the char is not _ or alphanumeric
        while self.current_char is not None and (
            self.current_char.isalnum() or self.current_char == "_"
        ):
            identifier += self.current_char
            self.advance()

        return Token(TokenType.IDENTIFIER, identifier)

    def peek(self):
        peek_position = self.position + 1
        if peek_position < len(self.source_code):
            return self.source_code[peek_position]
        else:
            return None


class Token:
    """Returns the token representation"""
    def __init__(self, token_type, value) -> None:
        self.token_type = token_type
        self.value = value

    def __repr__(self) -> str:
        return f"<Token({self.token_type}, '{self.value}')"


if __name__ == "__main__":
    CODE = """
            x = 5 + 3
            y = x * 2
            """

    lexer = Lexer(CODE)
    tokens = lexer.tokenize()

    for token in tokens:
        print(token)
