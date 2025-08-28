# Empathetic Code Reviewer

A tool that transforms direct, blunt code review comments into supportive, constructive, and educational guidance. Foster a positive code review culture with feedback that helps developers grow while maintaining code quality standards.

## Features

- **Positive Rephrasing**: Converts critical comments into encouraging feedback
- **Educational Explanations**: Provides the "why" behind suggestions with clear principles
- **Concrete Examples**: Offers specific code improvements with before/after examples
- **Severity-aware Tone**: Adjusts feedback tone (gentle ↔️ firm-but-kind) based on issue severity
- **Resource Links**: Includes references to relevant documentation (PEP 8, Python docs, etc.)
- **Offline Functionality**: Works with a rule-based generator without requiring internet
- **LLM Integration Point**: Optional plugin architecture for large language models
- **Web Interface**: Interactive tool accessible via local server
- **CLI Support**: Command-line interface for automation and integration

## Quick Start

### Installation

1. Clone or download the project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### CLI Mode

Process code review comments from a JSON file:

```bash
python -m empathetic_reviewer.cli --input sample_input.json --output report.md
```

### Web Mode

1. Start the web server:
   ```bash
   python -m empathetic_reviewer.web_server
   ```

2. Open your browser and navigate to `http://localhost:5000`

3. Paste your code snippet and review comments, then receive empathetic feedback

## Input Format

Provide your code and review comments in JSON format:

```json
{
  "code_snippet": "def get_active_users(users):\n results = []\n for u in users:\n  if u.is_active == True and u.profile_complete == True:\n   results.append(u)\n return results",
  "review_comments": [
    "This is inefficient. Don't loop twice conceptually.",
    "Variable 'u' is a bad name.",
    "Boolean comparison '== True' is redundant."
  ]
}
```

## Example Output

The tool generates Markdown-formatted feedback with:

1. **Positive Rephrasing**: Encouraging framing of the feedback
2. **The 'Why'**: Explanation of the underlying principle
3. **Suggested Improvement**: Concrete code example
4. **Resources**: Helpful links for further learning

## Advanced Usage

### Integrate Your Own LLM

For enhanced feedback generation, you can integrate your preferred language model:

1. Implement an `EmpatheticRewriter` compatible class
2. Plug it into `reviewer.py`
3. Use the `LLMRewriter` stub as a template for your API calls

Example implementation outline:

```python
class MyLLMRewriter(EmpatheticRewriter):
    def rewrite_comment(self, original_comment, code_snippet, context):
        # Your LLM integration logic here
        return empathetic_feedback
```

### Customize Severity Heuristics

Adjust how the tool determines comment severity by modifying the heuristics in `reviewer.py`:

```python
# Customize your severity detection rules
SEVERITY_INDICATORS = {
    "low": ["consider", "maybe", "optional"],
    "medium": ["should", "recommend", "better"],
    "high": ["error", "bug", "security", "never", "always"]
}
```

## Project Layout

```
empathetic_code_reviewer/
├── empathetic_reviewer/
│   ├── __init__.py
│   ├── reviewer.py          # Core review logic
│   ├── cli.py               # Command-line interface
│   └── web_server.py        # Web server implementation
├── web/
│   └── index.html           # Web interface
├── tests/
│   └── test_basic.py        # Test cases
├── sample_input.json        # Example input
├── sample_output.md         # Example output
├── README.md
└── requirements.txt         # Python dependencies
```

## Contributing

We welcome contributions! Please feel free to submit issues, suggestions, or pull requests to improve the Empathetic Code Reviewer.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions, issues, or suggestions:
1. Check the existing issues on GitHub
2. Create a new issue with detailed information
3. Include sample input and expected output when reporting bugs

---

**Remember**: Code reviews are about helping each other grow as developers while maintaining quality standards. This tool helps ensure that feedback is constructive, educational, and supportive.
