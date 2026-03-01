import pytest
from src.semantics import SymbolTable, SemanticError

def test_symbol_table_declare():
    """Week 4: Basic symbol table works"""
    table = SymbolTable()
    table.declare("x", "int")
    result = table.lookup("x")
    assert result['type'] == 'int'
    assert result['scope'] == 0

def test_sem001_undeclared_variable():
    """SEM001: Undeclared identifier error"""
    table = SymbolTable()
    with pytest.raises(SemanticError, match="SEM001"):
        table.lookup("y")

def test_sem003_duplicate_declaration():
    """SEM003: Duplicate declaration error"""
    table = SymbolTable()
    table.declare("x", "int")
    with pytest.raises(SemanticError, match="SEM003"):
        table.declare("x", "int")

def test_sem002_type_mismatch():
    """SEM002: Type checking fails"""
    table = SymbolTable()
    with pytest.raises(SemanticError, match="SEM002"):
        table.type_check("int", "string")

def test_type_check_success():
    """Valid type checking passes"""
    table = SymbolTable()
    result = table.type_check("int", "int")
    assert result == "int"

def test_scope_management():
    """Scope enter/exit works"""
    table = SymbolTable()
    table.enter_scope()
    assert table.current_scope() == 1
    table.exit_scope()
    assert table.current_scope() == 0
