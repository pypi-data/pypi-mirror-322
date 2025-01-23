from pseudocode.transpilation import *

class Pseudocode():
    """Object for initialising the pseudocode"""
    def __init__(self, source: str | list[str], file: bool=False) -> None:
        self.pseudocode: list[str] = self.read_file(source) if file else source

    @property
    def pseudocode(self) -> list[str]:
        return self._obj_data
    
    @pseudocode.setter
    def obj_data(self, source: str | list[str]) -> None:
        if type(source) == str:
            self._obj_data: list[str] = source.splitlines(True)
        elif type(source) == list:
            self._obj_data: list[str] = source
        else:
            raise ValueError("VertexParser accepts str or list[str] as source")

    @staticmethod
    def read_file(source) -> list[str] | None:
        try:
            with open(source, 'r') as file:
                return file.readlines()
        except FileNotFoundError:
            print("Given obj file doesn't exist")
            exit()


class Transpile():
    def __init__(self):
        self.lexer = lexer.Lexer("edexcel")
        tokenized: list[Token] = self.lexer.tokenize("SEND 'hello' TO DISPLAY")
        self.parser = parser.Parser(tokenized)

Transpile()