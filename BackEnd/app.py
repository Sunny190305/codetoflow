from flask import Flask, request, jsonify
import os
try:
    from flask_cors import CORS
except ImportError:
    # Define a dummy CORS that does nothing
    def CORS(app, **kwargs):
        pass
from parser.python_parser import parse_python_code
from parser.c_cpp_parser import parse_c_cpp_code
from parser.java_parser import parse_java_code
from parser.html_parser import parse_html_code

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

@app.route('/parse', methods=['POST'])
def parse_code():
    data = request.json
    source_code = data.get('code', '')
    language = data.get('language', 'python').lower()

    if language == 'python':
        result = parse_python_code(source_code)
    elif language in ['c', 'cpp', 'c++']:
        result = parse_c_cpp_code(source_code)
    elif language == 'java':
        result = parse_java_code(source_code)
    elif language == 'html':
        result = parse_html_code(source_code)
    else:
        return jsonify({"error": f"Unsupported language: {language}"}), 400

    if "error" in result:
        return jsonify(result), 400
        
    return jsonify(result)

# Keep the old endpoint for backward compatibility if needed, or redirect
@app.route('/parse-python', methods=['POST'])
def parse_python_legacy():
    data = request.json
    source_code = data.get('code', '')
    result = parse_python_code(source_code)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
