# src/parser.py - Week 5 FIXED Parser
from typing import List, Dict, Any
from src.lexer import Token

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = [t for t in tokens if t.type != 'SKIP']  # Remove whitespace
        self.pos = 0
    
    def parse(self) -> Dict[str, Any]:
        """Lexer tokens → AST"""
        program = {
            'type': 'program',
            'functions': [],
            'declarations': [],
            'statements': []
        }
        
        while self.pos < len(self.tokens) and self.tokens[self.pos].type != 'EOF':
            if self.tokens[self.pos].type == 'INT' and self.pos + 1 < len(self.tokens):
                if self.tokens[self.pos + 1].type == 'ID':
                    # Function declaration: int main()
                    if self.pos + 4 < len(self.tokens) and self.tokens[self.pos + 2].type == 'LPAREN':
                        func = self.parse_function()
                        program['functions'].append(func)
                    else:
                        # Variable declaration: int x = 5;
                        decl = self.parse_declaration()
                        if decl:
                            program['declarations'].append(decl)
            elif self.tokens[self.pos].type == 'ID':
                stmt = self.parse_assignment()
                if stmt:
                    program['statements'].append(stmt)
            else:
                self.pos += 1
        
        return program
    
    def parse_function(self) -> Dict[str, Any]:
        """int main(){} → Function AST"""
        self.pos += 1  # Skip INT
        name = self.tokens[self.pos].value  # ID
        self.pos += 3  # Skip ID LPAREN RPAREN
        if self.pos < len(self.tokens) and self.tokens[self.pos].type == 'LBRACE':
            self.pos += 2  # Skip LBRACE RBRACE (simplified)
        return {'type': 'function', 'name': name, 'body': []}
    
    def parse_declaration(self) -> Dict[str, Any]:
        """int x=5; → Declaration AST"""
        if (self.pos < len(self.tokens) and self.tokens[self.pos].type == 'INT' and
            self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1].type == 'ID'):
            
            self.pos += 1  # Skip INT
            name = self.tokens[self.pos].value  # ID
            self.pos += 1
            
            # Skip = NUMBER ;
            while (self.pos < len(self.tokens) and 
                   self.tokens[self.pos].type not in ['LBRACE', 'EOF']):
                self.pos += 1
            
            return {'type': 'declaration', 'name': name, 'type': 'int'}
        return None
    
    def parse_assignment(self) -> Dict[str, Any]:
        """x=10; → Assignment AST"""
        if (self.pos < len(self.tokens) and self.tokens[self.pos].type == 'ID' and
            self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1].type == 'ASSIGN'):
            
            name = self.tokens[self.pos].value
            self.pos += 2  # Skip ID =
            
            # Skip NUMBER ;
            while (self.pos < len(self.tokens) and 
                   self.tokens[self.pos].type not in ['LBRACE', 'EOF']):
                self.pos += 1
            
            return {'type': 'assignment', 'left': name, 'right': 'int'}
        return None
