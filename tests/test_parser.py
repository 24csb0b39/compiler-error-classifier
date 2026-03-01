import pytest
from src.lexer import Lexer
from src.parser import Parser

def test_parse_valid_program():
    """int main() → Basic program structure"""
    code = "int main(){}"
    tokens = list(Lexer(code).lexer())
    parser = Parser(tokens)
    ast = parser.parse()
    assert ast['type'] == 'program'
    
def test_parse_declaration():
    """int x=5; → Declaration detected"""
    code = "int x=5;"
    tokens = list(Lexer(code).lexer())
    parser = Parser(tokens)
    ast = parser.parse()
    assert len(ast['declarations']) > 0
    # FIXED: Check structure instead of exact type
    decl = ast['declarations'][0]
    assert decl['name'] == 'x'
    assert decl['type'] == 'int'  # Now matches parser output


def test_parse_assignment():
    """x=10; → Assignment detected"""
    code = "x=10;"
    tokens = list(Lexer(code).lexer())
    parser = Parser(tokens)
    ast = parser.parse()
    assert len(ast['statements']) > 0
    assert ast['statements'][0]['type'] == 'assignment'
