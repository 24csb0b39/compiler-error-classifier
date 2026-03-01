# src/semantics.py - Week 4 Semantic Analysis Engine
from typing import Dict, Optional, List
from src.lexer import Token
from src.parser import Parser

class SymbolTable:
    def __init__(self):
        self.symbols: Dict[str, Dict] = {}
        self.scope_stack: List[int] = [0]  # Global scope
    
    def enter_scope(self):
        self.scope_stack.append(len(self.scope_stack))
    
    def exit_scope(self):
        self.scope_stack.pop()
    
    def declare(self, name: str, typ: str, scope: int):
        """SEM003: Detect duplicate declaration"""
        if name in self.symbols and self.symbols[name]['scope'] == scope:
            raise SemanticError(f"SEM003: Duplicate declaration of {name}")
        self.symbols[name] = {'type': typ, 'scope': scope}
    
    def lookup(self, name: str) -> Optional[Dict]:
        """Scope resolution - find nearest declaration"""
        if name in self.symbols:
            return self.symbols[name]
        raise SemanticError(f"SEM001: Undeclared variable {name}")
    
    def type_check(self, op: str, left_type: str, right_type: str) -> str:
        """SEM002: Type compatibility checking"""
        if left_type != right_type:
            raise SemanticError(f"SEM002: Type mismatch {left_type} != {right_type}")
        return left_type

class SemanticError(Exception):
    def __init__(self, code: str, message: str = ""):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
    
    def analyze_program(self, ast: Dict) -> Dict:
        """Main entry point for semantic analysis"""
        try:
            self.symbol_table.enter_scope()
            for func in ast.get('functions', []):
                self.analyze_function(func)
            self.symbol_table.exit_scope()
            return {'status': 'OK', 'errors': []}
        except SemanticError as e:
            return {'status': 'ERROR', 'errors': [str(e)]}
    
    def analyze_function(self, func: Dict):
        """Analyze function declaration"""
        self.symbol_table.enter_scope()
        name = func['name']
        self.symbol_table.declare(name, 'function', self.symbol_table.scope_stack[-1])
        
        for stmt in func.get('body', []):
            self.analyze_statement(stmt)
        self.symbol_table.exit_scope()
    
    def analyze_statement(self, stmt: Dict):
        """Analyze single statement"""
        stmt_type = stmt['type']
        
        if stmt_type == 'declaration':
            self.analyze_declaration(stmt)
        elif stmt_type == 'assignment':
            self.analyze_assignment(stmt)
        elif stmt_type == 'return':
            self.analyze_return(stmt)
    
    def analyze_declaration(self, decl: Dict):
        """int x = 5; → SEM001, SEM002, SEM003"""
        name = decl['name']
        typ = decl['type']  # 'int', 'string'
        expr_type = self.analyze_expression(decl['init'])
        
        self.symbol_table.type_check('=', typ, expr_type)
        self.symbol_table.declare(name, typ, self.symbol_table.scope_stack[-1])
    
    def analyze_assignment(self, assign: Dict):
        """x = 10; → SEM001, SEM002"""
        name = assign['left']
        expr_type = self.analyze_expression(assign['right'])
        sym = self.symbol_table.lookup(name)
        self.symbol_table.type_check('=', sym['type'], expr_type)
    
    def analyze_expression(self, expr: Dict) -> str:
        """Recursive expression type checking"""
        if expr['type'] == 'literal':
            return self.literal_type(expr['value'])
        elif expr['type'] == 'variable':
            sym = self.symbol_table.lookup(expr['name'])
            return sym['type']
        elif expr['type'] == 'binary':
            left = self.analyze_expression(expr['left'])
            right = self.analyze_expression(expr['right'])
            return self.symbol_table.type_check(expr['op'], left, right)
        raise SemanticError("SEM999", "Invalid expression")
    
    def literal_type(self, value: str) -> str:
        if value.isdigit():
            return 'int'
        elif value.startswith('"'):
            return 'string'
        return 'unknown'
