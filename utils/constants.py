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
        "INT",
        "FLOAT",
        "STRING",
        "FOR",
        "IF",
        "ELSE",
        "WHILE",
        "RETURN",
        "READ",
        "WRITE",
        "VOID",
    ]
)


TOKEN_IDS = {
    "INT": 1,
    "FLOAT": 2,
    "STRING": 3,
    "FOR": 4,
    "IF": 5,
    "ELSE": 6,
    "WHILE": 7,
    "RETURN": 8,
    "READ": 9,
    "WRITE": 10,
    "VOID": 11,
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