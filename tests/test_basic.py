import json
from empathetic_reviewer.reviewer import generate_report

def test_generate_report_basic():
    data = {
        "code_snippet": "def f(x):\n    if x == True:\n        return 1\n    return 0",
        "review_comments": [
            "Boolean comparison '== True' is redundant.",
            "Variable 'x' is a bad name."
        ]
    }
    md = generate_report(data)
    assert "Positive Rephrasing" in md
    assert "The 'Why'" in md
    assert "Suggested Improvement" in md
    assert "Holistic Summary" in md
