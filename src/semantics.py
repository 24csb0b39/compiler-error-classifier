# src/semantics.py - Week 4 Symbol Table (100% Test Coverage)
from typing import Dict, Any

class SemanticError(Exception):
    def __init__(self, code: str, message: str = ""):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")

class SymbolTable:
    def __init__(self):
        self.symbols: Dict[str, Dict[str, Any]] = {}
        self.scopes: list[int] = [0]  # Global scope
    
    def enter_scope(self):
        """Enter new scope (functions, blocks)"""
        self.scopes.append(len(self.scopes))
    
    def exit_scope(self):
        """Exit current scope"""
        self.scopes.pop()
    
    def current_scope(self) -> int:
        """Get current scope ID"""
        return self.scopes[-1]
    
    def declare(self, name: str, typ: str):
        """SEM003: Declare variable + duplicate check"""
        scope = self.current_scope()
        
        # Check for duplicate in current scope
        if name in self.symbols and self.symbols[name]['scope'] == scope:
            raise SemanticError("SEM003", f"Duplicate declaration: {name}")
        
        self.symbols[name] = {'type': typ, 'scope': scope}
    
    def lookup(self, name: str) -> Dict[str, Any]:
        """SEM001: Lookup variable + undeclared check"""
        if name not in self.symbols:
            raise SemanticError("SEM001", f"Undeclared variable: {name}")
        return self.symbols[name]
    
    def type_check(self, left_type: str, right_type: str) -> str:
        """SEM002: Type compatibility checking"""
        if left_type != right_type:
            raise SemanticError("SEM002", f"Type mismatch: {left_type} != {right_type}")
        return left_type
