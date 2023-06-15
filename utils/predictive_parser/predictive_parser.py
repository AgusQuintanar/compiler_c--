class PredictiveParser:
    def match(self, token, grammar):
        if token.type == grammar:
            return True
        return False
    
    def parse(self, tokens):
        ...