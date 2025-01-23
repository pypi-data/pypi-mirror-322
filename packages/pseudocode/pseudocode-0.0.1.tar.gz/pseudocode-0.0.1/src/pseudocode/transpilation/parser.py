from sys import exit
from pseudocode.transpilation import Token

class Parser():
    """Parses the tokens to Python code"""
    def __init__(self, tokens: list[Token]) -> None:
        self.pos: int = 0
        self.tokens: list[Token] = tokens
        self.python_code: str = ''
        self.parse_print()

    def current_token(self) -> Token:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else exit()
    
    def eat(self, expected_token: str) -> None:
        token = self.current_token()
        if expected_token not in token:
            raise SyntaxError(f"Invalid token: {token}")
        self.pos += 1

    def eats(self, *tokens: str) -> None:
        for token in tokens:
            self.eat(token)

    def parse_expression(self) -> str:
        token = self.current_token()
        if "t_STRING" in token:
            self.pos += 1
            return token["t_STRING"]

    def parse_print(self):
        self.eats("t_SEND")
        expression = self.parse_expression()
        self.eats("t_TO", "t_OUTPUT")
        print(f"print({expression})")
        