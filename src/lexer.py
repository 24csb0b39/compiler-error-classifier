import re

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

TOKEN_SPECS = [
    ('SKIP', r'\s+'),           # WHITESPACE FIRST!
    ('NUMBER', r'\d+'),
    ('INT', r'int'),
    ('IF', r'if'),
    ('WHILE', r'while'),
    ('RETURN', r'return'),
    ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('ASSIGN', r'='),
    ('GT', r'>'),
    ('SEMICOLON', r';'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('MISMATCH', r'.'),
]

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
    
    def lexer(self):
        while self.pos < len(self.text):
            for type_, regex in TOKEN_SPECS:
                pattern = re.compile(regex)
                match = pattern.match(self.text, self.pos)
                if match:
                    value = match.group()
                    self.pos = match.end()
                    if type_ == 'SKIP':
                        continue            # Skip whitespace!
                    yield Token(type_, value)
                    break
            else:
                yield Token('MISMATCH', self.text[self.pos])
                self.pos += 1
