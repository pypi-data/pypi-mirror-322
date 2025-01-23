from types import ModuleType
from re import match, compile
from importlib import import_module
from collections import OrderedDict
from sys import exit
from pseudocode.transpilation import Token, TokenPatterns

class Lexer():
    """Tokenizes the pseudocode"""
    def __init__(self, language: str="edexcel") -> None:
        """
        Initialises the Lexer class for tokenizing the pseudocode

        Args:
            language (str, optional): The language for lexing. Four languages are available: 
                - cie 
                - edexcel 
                - aqa  
                - ocr
        """
        self.__pos: int = 0
        self.__tokens: list[Token] = []
        self.__token_patterns: TokenPatterns = self.import_tokens(language)

    @staticmethod
    def import_tokens(language: str) -> TokenPatterns:
        """
        Try and import tokens from a specific appendix.
        If fail, git blame

        Args:
            language (str): Import one of the four appendixes

        Returns:
            Token Patterns to match to from specified appendix
        """
        try:
            tokens: ModuleType = import_module(f"pseudocode.tokens.{language}")
        except:
            exit("a .tokens file for the provided language doesn't exist")
        else:
            return OrderedDict((token, compile(r'^' + getattr(tokens, token))) for token in dir(tokens) if token.startswith('t_'))

    def tokenize(self, pseudocode: str) -> list[Token]:
        """
        Goes through the pseudocode and tokenizes it.

        Args:
            pseudocode (str): The pseudocode
        """
        t_whitespace = compile(r'\s+')
        while self.__pos < len(pseudocode):
            if whitespace := t_whitespace.match(pseudocode[self.__pos:]):
                self.__pos += len(whitespace.group(0))
                continue
            
            matched: bool = False
            for token, pattern in self.__token_patterns.items():
                if value := match(pattern, pseudocode[self.__pos:]):  
                    self.__tokens.append({token: value.group(0)})
                    self.__pos += len(value.group(0))
                    matched = True
                    break

            if not matched:
                exit(pseudocode[self.__pos:])
        
        return self.__tokens