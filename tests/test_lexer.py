import pytest
from src.lexer import Lexer

def test_number():
    lexer = Lexer("123 45")
    tokens = list(lexer.lexer())
    assert tokens[0].type == "NUMBER"
    assert tokens[0].value == "123"

def test_identifier():
    lexer = Lexer("x variable")
    tokens = list(lexer.lexer())
    assert tokens[0].type == "ID"
    assert tokens[0].value == "x"

def test_keywords():
    lexer = Lexer("int if while return")
    tokens = list(lexer.lexer())
    assert [t.type for t in tokens] == ["INT", "IF", "WHILE", "RETURN"]

def test_program():
    code = "int main(){return 0;}"
    lexer = Lexer(code)
    tokens = list(lexer.lexer())
    expected = ["INT", "ID", "LPAREN", "RPAREN", "LBRACE", "RETURN", "NUMBER", "SEMICOLON", "RBRACE"]
    assert [t.type for t in tokens] == expected

@pytest.mark.parametrize("code, expected", [
    ("x=5;", ["ID", "ASSIGN", "NUMBER", "SEMICOLON"]),
    ("if(x>0){}", ["IF", "LPAREN", "ID", "GT", "NUMBER", "RPAREN", "LBRACE", "RBRACE"]),
])
def test_complex(code, expected):
    lexer = Lexer(code)
    types = [t.type for t in lexer.lexer()]
    assert types == expected
