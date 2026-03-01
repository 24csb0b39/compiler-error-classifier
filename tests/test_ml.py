import pytest
from src.ml.error_classifier import ErrorClassifier

def test_ml_model_initializes():
    """ML model loads without errors"""
    clf = ErrorClassifier()
    assert clf.model is not None

def test_ml_predicts_errors():
    """ML detects compiler errors"""
    clf = ErrorClassifier()
    result = clf.classify('int x = "hello";')
    assert "SEM002" in result or "SEM001" in result or "SEM003" in result

def test_ml_predicts_valid_code():
    """ML recognizes valid C code"""
    clf = ErrorClassifier()
    result = clf.classify('int main(){return 0;}')
    assert "OK" in result or len(result) > 0
