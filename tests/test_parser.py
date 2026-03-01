import pytest
from src.lexer import Lexer
from src.parser import Parser

def test_parse_valid_program():
    code = "int main(){}"
    tokens = list(Lexer(code).lexer())
    parser = Parser(tokens)  # Pass TOKENS, not text
    ast = parser.parse()
    assert ast['type'] == 'program'

def test_parse_declaration():
    code = "int x=5;"
    tokens = list(Lexer(code).lexer())
    parser = Parser(tokens)  # Pass TOKENS, not text
    ast = parser.parse()
    assert len(ast['declarations']) > 0
    assert ast['declarations'][0]['name'] == 'x'

def test_parse_assignment():
    code = "x=10;"
    tokens = list(Lexer(code).lexer())
    parser = Parser(tokens)  # Pass TOKENS, not text
    ast = parser.parse()
    assert len(ast['statements']) > 0
