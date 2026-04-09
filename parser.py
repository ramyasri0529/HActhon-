import ast
import os
from typing import Dict, Any, List

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self, filename: str):
        self.filename = filename
        self.functions = []
        self.classes = []
        self.imports = []

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            self.imports.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module:
            self.imports.append(node.module)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        methods = []
        for body_item in node.body:
            if isinstance(body_item, ast.FunctionDef):
                methods.append({
                    'name': body_item.name,
                    'is_async': False
                })
            elif isinstance(body_item, ast.AsyncFunctionDef):
                methods.append({
                    'name': body_item.name,
                    'is_async': True
                })
        
        self.classes.append({
            'name': node.name,
            'methods': methods,
            'docstring': ast.get_docstring(node)
        })
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        # Only capture functions at the module level
        # To avoid capturing methods again, we can check node's context,
        # but a simpler way is to just grab all and the generator can filter
        # Better: we only add it to functions if it's not starting with an indent?
        # Actually NodeVisitor traverses deeply. Let's just collect all top-level functions.
        pass

def parse_file(filepath: str) -> Dict[str, Any]:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File {filepath} not found.")
        
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()

    tree = ast.parse(source)
    
    # Simple top-level extraction to avoid mixing methods and functions
    functions = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            functions.append({
                'name': node.name,
                'is_async': isinstance(node, ast.AsyncFunctionDef),
                'docstring': ast.get_docstring(node),
                'source': ast.get_source_segment(source, node)
            })
            
    analyzer = CodeAnalyzer(filepath)
    analyzer.visit(tree)
    
    return {
        'filepath': filepath,
        'imports': analyzer.imports,
        'classes': analyzer.classes,
        'functions': functions,
        'source_code': source
    }

def format_analysis(analysis: Dict[str, Any]) -> str:
    summary = f"File: {analysis['filepath']}\n\n"
    summary += "Imports:\n" + "\n".join([f"- {i}" for i in analysis['imports']]) + "\n\n"
    
    summary += "Classes & Methods:\n"
    for c in analysis['classes']:
        summary += f"- class {c['name']}:\n"
        for m in c['methods']:
            summary += f"    - def {m['name']}(...)\n"
    
    summary += "\nFunctions:\n"
    for f in analysis['functions']:
        summary += f"- def {f['name']}(...)\n"
    
    return summary
