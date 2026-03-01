# src/parser.py - Week 4 Parser + AST Builder
from typing import Dict, List  # ADD THIS LINE
from src.lexer import Lexer, Token

class ParseError(Exception):
    pass

class Parser:
    def __init__(self, text: str):
        self.tokens = list(Lexer(text).lexer())
        self.pos = 0
    
    def parse(self) -> Dict:
        """Parse → AST for semantic analysis"""
        program = {'type': 'program', 'functions': []}
        
        while not self.eof():
            func = self.parse_function()
            if func:
                program['functions'].append(func)
        
        return program
    
    def parse_function(self) -> Dict:   
        """int main() { ... }"""
        try:
            self.expect('INT')
            name = self.expect('ID').value
            self.expect('LPAREN')
            self.expect('RPAREN')
            self.expect('LBRACE')
            body = self.parse_statements()
            self.expect('RBRACE')
            return {'type': 'function', 'name': name, 'body': body}
        except ParseError:
            return None
    
    def parse_statements(self) -> List[Dict]:
        """Statement list in function body"""
        stmts = []
        while not self.eof() and self.current.type != 'RBRACE':
            stmt = self.parse_statement()
            if stmt:
                stmts.append(stmt)
        return stmts
    
    def parse_statement(self) -> Dict:
        """Declaration, assignment, return"""
        if self.current.type == 'INT':
            return self.parse_declaration()
        elif self.current.type == 'RETURN':
            return self.parse_return()
        elif self.is_id(self.current):
            return self.parse_assignment()
        return None
    
    def parse_declaration(self) -> Dict:
        """int x = 5;"""
        self.consume('INT')
        name = self.consume('ID').value
        self.consume('ASSIGN')
        expr = self.parse_expression()
        self.consume('SEMICOLON')
        return {'type': 'declaration', 'name': name, 'type': 'int', 'init': expr}
    
    def parse_return(self) -> Dict:
        """return 0;"""
        self.consume('RETURN')
        expr = self.parse_expression()
        self.consume('SEMICOLON')
        return {'type': 'return', 'value': expr}
    
    def parse_assignment(self) -> Dict:
        """x = 10;"""
        name = self.consume('ID').value
        self.consume('ASSIGN')
        expr = self.parse_expression()
        self.consume('SEMICOLON')
        return {'type': 'assignment', 'left': name, 'right': expr}
    
    def parse_expression(self) -> Dict:
        """Simple expressions for Week 4"""
        if self.current.type == 'NUMBER':
            return {'type': 'literal', 'value': self.consume('NUMBER').value}
        elif self.is_id(self.current):
            return {'type': 'variable', 'name': self.consume('ID').value}
        raise ParseError("Invalid expression")
    
    def expect(self, token_type: str) -> Token:
        if self.current.type == token_type:
            return self.consume(token_type)
        raise ParseError(f"Expected {token_type}")
    
    def consume(self, token_type: str) -> Token:
        token = self.current
        if token.type == token_type:
            self.advance()
            return token
        raise ParseError(f"Expected {token_type}")
    
    @property
    def current(self) -> Token:
        return self.tokens[self.pos] if not self.eof() else Token('EOF', '')
    
    def advance(self):
        self.pos += 1
    
    def eof(self) -> bool:
        return self.pos >= len(self.tokens)
    
    def is_id(self, token: Token) -> bool:
        return token.type == 'ID'
