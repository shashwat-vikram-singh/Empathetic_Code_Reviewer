from flask import Flask, request, jsonify
from empathetic_reviewer.reviewer import generate_report
import json

app = Flask(__name__)

@app.route('/')
def serve_index():
    with open('web/index.html', 'r') as f:
        return f.read()

@app.route('/api/review', methods=['POST'])
def review_code():
    data = request.json
    if not data or 'code_snippet' not in data or 'review_comments' not in data:
        return jsonify({"error": "Invalid input"}), 400
    report = generate_report(data)
    return jsonify({"report": report})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)