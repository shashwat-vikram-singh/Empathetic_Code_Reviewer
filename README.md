Empathetic Code Reviewer
Transform direct, blunt code review comments into supportive, constructive, and educational guidance.
Features

Converts raw review comments into empathetic feedback with:
Positive Rephrasing
The 'Why' (principle explained)
Suggested Improvement (concrete code example)


Severity-aware tone (gentle ↔ firm-but-kind) using simple heuristics.
Resource links (PEP 8, Python docs) based on detected principles.
Works offline with a rule-based generator. Optional plug-in point for LLMs.
Web Interface: Interactive tool accessible via a local server.

Quick Start
CLI Mode
python -m empathetic_reviewer.cli --input sample_input.json --output report.md

Web Mode

Install dependencies:pip install -r requirements.txt


Run the web server:python -m empathetic_reviewer.web_server


Open a browser and navigate to http://localhost:5000.

Input JSON Format
{
  "code_snippet": "def get_active_users(users):\n results = []\n for u in users:\n  if u.is_active == True and u.profile_complete == True:\n   results.append(u)\n return results",
  "review_comments": [
    "This is inefficient. Don't loop twice conceptually.",
    "Variable 'u' is a bad name.",
    "Boolean comparison '== True' is redundant."
  ]
}

Optional: Integrate Your Own LLM
Implement EmpatheticRewriter compatible class and plug it into reviewer.py.You can also adapt LLMRewriter stub to call your preferred API.
Project Layout
empathetic_code_reviewer/
├── empathetic_reviewer/
│   ├── __init__.py
│   ├── reviewer.py
│   ├── cli.py
│   └── web_server.py
├── web/
│   └── index.html
├── tests/
│   └── test_basic.py
├── sample_input.json
├── sample_output.md
├── README.md
└── requirements.txt

License
MIT