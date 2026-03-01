# src/api/main.py - Week 7 FastAPI (FIXED)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.ml.error_classifier import ErrorClassifier

app = FastAPI(title="ML Compiler API v1.0")

clf = ErrorClassifier()

class CodeInput(BaseModel):
    code: str

@app.get("/")
async def root():
    return {"message": "🚀 ML Compiler API v1.0", "ml_accuracy": "71%"}

@app.post("/analyze")
async def analyze_code(input: CodeInput):
    """C code → ML predictions (uses classify method)"""
    try:
        # Use existing classify method
        result = clf.classify(input.code)
        error_type, confidence = result.split(" (")
        confidence = confidence.rstrip(")%")
        
        predictions = [{
            "error_type": error_type,
            "confidence": float(confidence)/100,
            "probability": f"{confidence}%"
        }]
        
        return {
            "status": "success",
            "code_length": len(input.code),
            "predictions": predictions,
            "error_count": 1 if error_type != "OK" else 0,
            "summary": f"{error_type} detected ({confidence} confidence)"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy", "ml_ready": True}
