# CUSTOM TYPES
IDENTIFIER = type('IDENTIFIER', (), {})
COMMENT = type('COMMENT', (), {})

azAZ = frozenset(
    [chr(i) for i in range(ord("a"), ord("z") + 1)]
    + [chr(i) for i in range(ord("A"), ord("Z") + 1)]
)

DIGITS = frozenset([str(_) for _ in range(10)])

EOF = "\0"

BLANK_DELIMITERS = frozenset([" ", "\t", "\n"])

RESERVED_KEYWORDS = frozenset(
    [
        "int",
        "float",
        "string",
        "for",
        "if",
        "else",
        "while",
        "return",
        "read",
        "write",
        "void",
    ]
)


TOKEN_IDS = {
    "int": 1,
    "float": 2,
    "string": 3,
    "for": 4,
    "if": 5,
    "else": 6,
    "while": 7,
    "return": 8,
    "read": 9,
    "write": 10,
    "void": 11,
    "+": 12,
    "-": 13,
    "*": 14,
    "(": 15,
    ")": 16,
    "[": 17,
    "]": 18,
    "{": 19,
    "}": 20,
    ";": 21,
    ",": 22,
    "<": 23,
    "<=": 24,
    ">": 25,
    ">=": 26,
    "!=": 27,
    "=": 28,
    "==": 29,
    "/": 30,
    "IDENTIFIER": 31,
    "INT_CONSTANT": 32,
    "FLOAT_CONSTANT": 33,
    "COMMENT": 34,
    "STRING_CONSTANT": 35
}