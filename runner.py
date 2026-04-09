import subprocess
import os

def run_tests_and_coverage(test_filepath: str, src_filepath: str) -> str:
    """
    Runs pytest with coverage on the given test file, targeting the source file for coverage tracking.
    """
    # Assuming testing context is the same directory as the source file.
    directory = os.path.dirname(src_filepath)
    src_filename = os.path.basename(src_filepath)
    test_filename = os.path.basename(test_filepath)
    
    # We want to run pytest with pytest-cov
    # Command: pytest test_filename --cov=src_filename --cov-report=term
    
    cmd = [
        "pytest",
        test_filename,
        f"--cov={src_filename.replace('.py', '')}",
        "--cov-report=term-missing"
    ]
    
    # Needs to run in the target directory
    result = subprocess.run(cmd, cwd=directory, capture_output=True, text=True)
    
    print("Test execution finished.")
    print("Exit code:", result.returncode)
    
    # Combine stdout and stderr
    output = result.stdout
    if result.stderr:
        output += "\n--- STDERR ---\n" + result.stderr
        
    return output
