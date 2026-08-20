import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from evaluator import evaluate_response, deterministic_scores, build_report
import pandas as pd

def test_correct_answer():
    r = evaluate_response("capital of France", "Paris is the capital of France.", "Paris is the capital of France.", False)
    assert r["overall_score"] >= 65

def test_empty_response():
    r = evaluate_response("2+2", "4", "", False)
    assert r["overall_score"] < 50

def test_safety_penalty():
    r = deterministic_scores("", "safe", "This is 100% safe and guaranteed.")
    assert r["safety"] < 100

def test_report():
    df = pd.DataFrame([
        {"overall_score": 80, "accuracy": 90, "grounding": 80, "consistency": 75, "safety": 85},
        {"overall_score": 60, "accuracy": 65, "grounding": 55, "consistency": 70, "safety": 50}
    ])
    x = build_report(df)
    assert x["total_cases"] == 2 and x["average_score"] == 70.0
