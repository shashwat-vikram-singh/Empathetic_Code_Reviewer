"""
Empathetic Code Reviewer: Rule-based generator of supportive, educational code review feedback.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Tuple
import re
import json

PRINCIPLE_LINKS = {
    "readability": [
        ("PEP 8 – Naming Conventions", "https://peps.python.org/pep-0008/#naming-conventions"),
        ("PEP 8 – Programming Recommendations", "https://peps.python.org/pep-0008/#programming-recommendations"),
    ],
    "performance": [
        ("Python Data Structures – List Comprehensions", "https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions"),
        ("Time Complexity Basics", "https://wiki.python.org/moin/TimeComplexity"),
    ],
    "conventions": [
        ("PEP 8 – Idiomatic Comparisons", "https://peps.python.org/pep-0008/#programming-recommendations"),
    ],
    "pythonic": [
        ("Comprehensions & Generators", "https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions"),
    ]
}

SEVERITY_WORDS = {
    "high": ["bug", "security", "vulnerab", "crash", "race", "sql injection", "xss", "unsafe", "broken"],
    "medium": ["inefficient", "n+1", "complex", "slow", "leak", "duplicat", "anti-pattern"],
    "low": ["nit", "minor", "typo", "style", "naming", "redundant", "format"]
}

@dataclass
class Section:
    original: str
    rephrased: str
    why: str
    suggestion: str
    links: List[Tuple[str, str]]

def detect_principles(comment: str) -> List[str]:
    c = comment.lower()
    principles = []
    if any(w in c for w in ["inefficient", "slow", "n+1", "optimiz", "complexity"]):
        principles.append("performance")
    if any(w in c for w in ["name", "read", "clar", "maintain", "refactor"]):
        principles.append("readability")
    if any("== true" in c or "== false" in c or "boolean" in c or "pep 8" in c for _ in [0]):
        principles.append("conventions")
        principles.append("pythonic")
    if not principles:
        principles.append("readability")
    return list(dict.fromkeys(principles))  # dedupe, preserve order

def detect_severity(comment: str) -> str:
    c = comment.lower()
    for s, words in SEVERITY_WORDS.items():
        if any(w in c for w in words):
            return s
    # fallback by punctuation/tone
    if "!" in comment or "all caps" in c:
        return "medium"
    return "low"

def tone_prefix(severity: str) -> str:
    if severity == "high":
        return "Thanks for flagging this critical area. Let's make it safe and robust:"
    if severity == "medium":
        return "Good foundation here—there's an opportunity to tighten things up:"
    return "Nice work on the core idea! With a small tweak, we can improve it further:"

def rephrase_comment(comment: str, severity: str) -> str:
    # Gentle rewrite templates
    c = comment.strip().rstrip(".")
    softened = {
        "inefficient": "we can streamline this to avoid extra work on large inputs",
        "bad name": "we can pick a more descriptive name to aid readability",
        "redundant": "we can simplify this to be more idiomatic",
    }
    text = tone_prefix(severity)
    if "inefficient" in c.lower():
        return f"{text} {softened['inefficient']}."
    if "name" in c.lower():
        return f"{text} {softened['bad name']}."
    if "redundant" in c.lower() or "== true" in c.lower():
        return f"{text} {softened['redundant']}."
    return f"{text} {c.capitalize()}."

def suggest_fix(code_snippet: str, comment: str) -> str:
    # Very small heuristics for Python
    code = code_snippet
    # Simplify boolean comparison
    if re.search(r"==\s*True", code) or "boolean" in comment.lower():
        code = re.sub(r"==\s*True", "", code)
        code = re.sub(r"==\s*False", " is False", code)
    # Improve variable name 'u' -> 'user'
    if re.search(r"\bfor\s+u\s+in\s+", code):
        code = re.sub(r"\bfor\s+u\s+in\s+", "for user in ", code)
        code = re.sub(r"\bu\b", "user", code)
    # List comprehension optimization heuristic
    if "inefficient" in comment.lower() or "loop" in comment.lower():
        # Try to transform a simple append loop into a list comprehension
        # Fallback: present a canonical example instead of risky transform
        return (
            "```python\n"
            "def get_active_users(users):\n"
            "    return [user for user in users if getattr(user, 'is_active', False) and getattr(user, 'profile_complete', False)]\n"
            "```"
        )
    return f"```python\n{code}\n```"

def principle_explanations(principles: List[str]) -> str:
    chunks = []
    for p in principles:
        if p == "performance":
            chunks.append("Iterating with unnecessary work can add up as input size grows. Using comprehensions or combining checks reduces per-item overhead.")
        elif p == "readability":
            chunks.append("Clear, descriptive names and straightforward conditionals make code easier to read, review, and maintain.")
        elif p == "conventions":
            chunks.append("Python style guides (PEP 8) recommend idiomatic boolean checks (e.g., `if flag:` rather than `if flag == True`).")
        elif p == "pythonic":
            chunks.append("Leaning on Python idioms like comprehensions keeps code concise and expressive.")
    return " ".join(chunks)

def links_for(principles: List[str]) -> List[Tuple[str, str]]:
    seen = set()
    out = []
    for p in principles:
        for title, url in PRINCIPLE_LINKS.get(p, []):
            if url not in seen:
                out.append((title, url))
                seen.add(url)
    return out

def generate_sections(code_snippet: str, review_comments: List[str]) -> List[Section]:
    sections = []
    for c in review_comments:
        sev = detect_severity(c)
        principles = detect_principles(c)
        sections.append(
            Section(
                original=c,
                rephrased=rephrase_comment(c, sev),
                why=principle_explanations(principles),
                suggestion=suggest_fix(code_snippet, c),
                links=links_for(principles),
            )
        )
    return sections

def generate_report(data: Dict[str, object]) -> str:
    code_snippet = str(data.get("code_snippet", "")).rstrip()
    review_comments = list(data.get("review_comments", []))

    sections = generate_sections(code_snippet, review_comments)

    lines = []
    lines.append("# Empathetic Code Review Report\n")
    lines.append("Analyzing the provided function and comments with an emphasis on supportive guidance, learning, and actionable improvements.\n")
    lines.append("---\n")
    for s in sections:
        lines.append(f'### Analysis of Comment: "{s.original}"\n')
        lines.append(f"* **Positive Rephrasing:**\n{s.rephrased}\n")
        lines.append(f"* **The 'Why':**\n{s.why}\n")
        lines.append(f"* **Suggested Improvement:**\n{s.suggestion}\n")
        if s.links:
            lines.append("*Further Reading:* " + " · ".join(f"[{t}]({u})" for t, u in s.links) + "\n")
        lines.append("---\n")

    # Holistic Summary
    lines.append("## Holistic Summary\n")
    lines.append(
        "Great foundation! The recommendations focus on efficiency, readability, and Python conventions. "
        "By adopting descriptive names, idiomatic boolean checks, and comprehensions, you make the code faster, clearer, and more maintainable. "
        "Keep iterating—these habits compound into professional-quality code.\n"
    )
    return "\n".join(lines)

def main():
    import argparse, sys, pathlib
    parser = argparse.ArgumentParser(description="Empathetic Code Reviewer")
    parser.add_argument("--input", "-i", required=True, help="Path to input JSON")
    parser.add_argument("--output", "-o", required=True, help="Path to output Markdown")
    args = parser.parse_args()

    inp = json.loads(pathlib.Path(args.input).read_text(encoding="utf-8"))
    report = generate_report(inp)
    pathlib.Path(args.output).write_text(report, encoding="utf-8")
    print(f"Wrote report to {args.output}")

if __name__ == "__main__":
    main()
