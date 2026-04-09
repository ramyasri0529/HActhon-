import os
from google import genai
from typing import Dict, Any

def generate_tests_for_file(analysis: Dict[str, Any]) -> str:
    """
    Given the analysis of a Python file, calls the Gemini model to generate pytest code.
    """
    # Initialize the client. Under the hood, it picks up GEMINI_API_KEY from environment variables.
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set.")
    
    client = genai.Client()
    
    prompt = f"""
You are an expert Python testing engineer building an automated test suite.
Your goal is to write high-quality, comprehensive unit and integration tests using `pytest` for the provided Python file.
The test code should ensure high code coverage and contain meaningful assertions. 
Include edge case scenarios and properly mock any external dependencies or side effects.

### File Information
- **Filepath:** {analysis['filepath']}

### Source Code
```python
{analysis['source_code']}
```

### Instructions
1. Write tests using the `pytest` framework.
2. Ensure you import the components from the source file accurately (assume the file is importable based on its filepath, or just use absolute imports if necessary, but typically standard relative/absolute imports are fine).
3. Generate tests that cover happy paths, error paths, and edge cases.
4. Output the raw Python code for the tests. DO NOT INCLUDE ANY MARKDOWN CODE BLOCKS OR BACKTICKS IN THE FINAL OUTPUT - JUST THE PURE PYTHON CODE. (Wait, to be safe, I'll extract it if you do).
5. Add insightful comments explaining what each test is validating.
"""

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    
    output = response.text
    # Clean up markdown if present
    if output.startswith("```python"):
        output = output[9:]
    elif output.startswith("```"):
        output = output[3:]
        
    if output.endswith("```"):
        output = output[:-3]
        
    return output.strip()
