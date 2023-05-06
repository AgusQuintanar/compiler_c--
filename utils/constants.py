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
        "IF",
        "THEN",
        "ELSE",
        "END",
        "DO",
        "WHILE",
        "READ",
        "WRITE"
    ]
)


TOKEN_IDS = {
    "IF": 1,
    "THEN": 2,
    "ELSE": 3,
    "END": 4,
    "DO": 5,
    "WHILE": 6,
    "READ": 7,
    "WRITE": 8,
    "+": 9,
    "-": 10,
    "*": 11,
    "(": 12,
    ")": 13,
    "[": 14,
    "]": 15,
    "{": 16,
    "}": 17,
    ";": 18,
    ",": 19,
    "<": 20,
    "<=": 21,
    ">": 22,
    ">=": 23,
    "!=": 24,
    "=": 25,
    "==": 26,
    "/": 27,
    "IDENTIFIER": 28,
    "INT": 29,
    "FLOAT": 30,
    "COMMENT": 31,
    "STRING": 32
}