IDENTIFIER = type('IDENTIFIER', (), {})

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

DELIMITERS = frozenset(
    [
        " ",
        ";",
        ":",
        "=",
        "*",
        "+",
        "-",
        "/",
        "(",
        ")",
        "<",
        ">"
    ]
)
