import argparse
import os
import sys

from parser import parse_file, format_analysis
from generator import generate_tests_for_file
from runner import run_tests_and_coverage

def main():
    parser = argparse.ArgumentParser(description="Automated Test Generation Agent")
    parser.add_argument("target", help="The Python specific file to generate tests for.")
    parser.add_argument("--out", help="Optional path to save the generated test file. Defaults to test_<target>.py in the same dir.")
    parser.add_argument("--run", action="store_true", help="Run the generated tests immediately and show coverage.")
    
    args = parser.parse_args()
    target_file = os.path.abspath(args.target)
    
    if not os.path.exists(target_file):
        print(f"Error: Target file {target_file} does not exist.")
        sys.exit(1)
        
    print(f"[*] Analyzing source code for {target_file}...")
    try:
        analysis = parse_file(target_file)
    except Exception as e:
        print(f"Error parsing file: {e}")
        sys.exit(1)
        
    # print(format_analysis(analysis))
    print("[*] Generating tests using LLM...")
    try:
        test_code = generate_tests_for_file(analysis)
    except Exception as e:
        print(f"Error generating tests: {e}")
        sys.exit(1)
        
    if args.out:
        out_path = os.path.abspath(args.out)
    else:
        directory = os.path.dirname(target_file)
        basename = os.path.basename(target_file)
        test_filename = f"test_{basename}"
        out_path = os.path.join(directory, test_filename)
        
    print(f"[*] Saving generated tests to {out_path}...")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(test_code)
        
    print("[*] Test generation successful!")
    
    if args.run:
        print(f"[*] Running tests and collecting coverage...")
        report = run_tests_and_coverage(out_path, target_file)
        print("\n--- Test Report ---")
        print(report)

if __name__ == "__main__":
    main()
