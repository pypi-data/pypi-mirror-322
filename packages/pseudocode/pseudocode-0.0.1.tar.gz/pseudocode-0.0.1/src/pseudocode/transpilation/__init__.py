from typing import TypeAlias
from collections import OrderedDict
from re import Pattern

Token: TypeAlias = dict[str, str]

TokenPatterns: TypeAlias = OrderedDict[str, Pattern]

__all__ = ["Token", "TokenPatterns", "bnf", "lexer", "parser"]