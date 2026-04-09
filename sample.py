import math

class Calculator:
    """A simple calculator class"""
    
    def add(self, a: int, b: int) -> int:
        return a + b
        
    def sqrt(self, a: float) -> float:
        if a < 0:
            raise ValueError("Cannot calculate square root of negative number")
        return math.sqrt(a)

def fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
