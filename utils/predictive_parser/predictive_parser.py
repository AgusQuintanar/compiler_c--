from .grammar import Grammar

from ..scanner import Token, TokenType


class PredictiveParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = 0

    def get_next_token(self):
        self.current_token += 1
        print(f"Next token: {self.tokens[self.current_token]}")
        return self.tokens[self.current_token]

    def get_current_token(self):
        # print(f"Current token: {self.tokens[self.current_token]}")
        return self.tokens[self.current_token]

    def add_token(self, token):
        self.tokens.append(token)

    def parse(self):
        # current_token = self.tokens[self.current_token]
        self.add_token(Token(value="$", type=TokenType.TERMINAL))

        for token in self.tokens:
            print(token)
        grammar = Grammar(
            get_current_token=self.get_current_token,
            get_next_token=self.get_next_token,
        )
        grammar.program()

        if self.get_current_token().value == "$":
            print("Success")
        else:
            print("Error")
            remaining_tokens = self.tokens[self.current_token :]
            print("Remaining tokens")
            for token in remaining_tokens:
                print(token)
