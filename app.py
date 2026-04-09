from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import traceback

from parser import parse_file, format_analysis
from generator import generate_tests_for_file
from runner import run_tests_and_coverage

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    code = data.get('code', '')
    
    if not code.strip():
        return jsonify({'error': 'Source code cannot be empty.'}), 400
        
    target_file = os.path.abspath('temp_source.py')
    test_file = os.path.abspath('test_temp_source.py')
    
    try:
        # Write user's code to a temporary file
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(code)
            
        # Parse the code
        analysis = parse_file(target_file)
        analysis_summary = format_analysis(analysis)
        
        # Check API key first
        if not os.environ.get("GEMINI_API_KEY"):
            # Mock behavior if no API Key to show the UI works
            test_code = 'import pytest\nfrom temp_source import *\n\n# NOTE: GEMINI_API_KEY was not set.\n# This is a generated mock test.\n\ndef test_mock():\n    assert True\n'
            coverage_report = "Mock Coverage Report. Please set GEMINI_API_KEY in the environment running this server to use real AI generation."
        else:
            # Generate the tests
            test_code = generate_tests_for_file(analysis)
            
        # Write tests to file
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_code)
            
        if os.environ.get("GEMINI_API_KEY"):
            # Run coverage
            coverage_report = run_tests_and_coverage(test_file, target_file)
            
        return jsonify({
            'success': True,
            'analysis': analysis_summary,
            'test_code': test_code,
            'coverage': coverage_report
        })
        
    except Exception as e:
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500
    finally:
        # Cleanup
        if os.path.exists(target_file):
            os.remove(target_file)
        if os.path.exists(test_file):
            os.remove(test_file)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
