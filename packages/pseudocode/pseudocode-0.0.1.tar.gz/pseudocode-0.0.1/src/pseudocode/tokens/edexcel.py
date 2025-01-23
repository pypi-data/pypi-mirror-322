# value: str = r"[^'\"\[\]]+(?:\[[^'\"]+\])*"
# # If anyone could clarify if a ' can be in a string in pseudocode, thatd be great
# string: str = r"'[^']*'|\"[^\"]*\""
# array: str = r"\[.*\]"
# # regex for variable / array index initialisation
# variable: str = r"[^ '\"\[\]]+"
# var_index: str = rf"{variable}(?:\[[^'\"]+\])*"
# # Also whether or not its fine for the ' ?' to be a ' *' instead
# condition: str = rf"(?:NOT )?{value}(?: ?(?:=|<>|>|>=|<|<=) ?{value})?(?: (?:AND|OR) (?:NOT )?{value}(?: ?(?:=|<>|>|>=|<|<=) ?{value})?)*"
# newline:str = rf"(?:\n)"
# comment: str = r"#.*"


# # data types
# tokens = {
#     "t_WHITESPACE": r" ",
#     "t_INTEGER": r"[\+\-]?\d+",
#     "t_REAL": r"[\+\-]?\d*\.\d+",
#     "t_BOOLEAN": r"TRUE|FALSE",
#     "t_STRING": r"'[^']*'|\"[^\"]*\"",
#     "t_CONST": r"CONST",

#     "t_TO": r"TO",

#     # built in functions
#     "t_SEND": r"SEND",
#     "t_OUTPUT": r"DISPLAY",

#     # arithmetic operators
#     "t_ADD": r"\+",
#     "t_SUBTRACT": r"\-",
#     "t_DIVIDE": r"\/",

#     # variable, this is last to not match other keywords
#     "t_VAR": "[a-zA-Z_][a-zA-Z0-9_]*"
# }

t_INTEGER = r"[\+\-]?\d+"
t_REAL = r"[\+\-]?\d*\.\d+"
t_BOOLEAN = r"TRUE|FALSE"
t_STRING = r"'[^']*'|\"[^\"]*\""
t_CONST = r"CONST"

t_TO = r"TO\b"

# selection


# built in functions
t_SEND = r"SEND(?=\ )"
t_OUTPUT = r"DISPLAY\b"

# arithmetic operators
t_ADD = r"\+"
t_SUBTRACT = r"\-"
t_DIVIDE = r"\/"

# variable this is last to not match other keywords
t_VAR = r"[a-zA-Z_][a-zA-Z0-9_]*"