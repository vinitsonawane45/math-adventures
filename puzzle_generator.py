# puzzle_generator.py
import random

LEVELS = {
    0: ("Baby", 1, 10),
    1: ("Easy", 5, 25),
    2: ("Medium", 10, 50),
    3: ("Hard", 20, 100),
    4: ("Master", 50, 200)
}

OPERATORS = ['+', '-', '*']

def clamp(value, min_val, max_val):
    """Clamp a value between min_val and max_val."""
    return max(min_val, min(value, max_val))

def generate_puzzle(level: int):
    # Clamp level safely between 0 and 4
    level = clamp(level, 0, 4)
    
    name, min_val, max_val = LEVELS[level]
    
    op = random.choice(OPERATORS)
    
    # Adjust b's range for multiplication to avoid huge numbers in high levels
    if op == '*':
        a = random.randint(min_val, max_val // 2)
        b = random.randint(min_val, max_val // 2)
    else:
        a = random.randint(min_val, max_val)
        b = random.randint(min_val, max_val)
        # For subtraction, ensure positive results
        if op == '-' and a < b:
            a, b = b, a
    
    # Compute answer
    answer = {'+': a + b, '-': a - b, '*': a * b}[op]
    
    question = f"{a} {op} {b}"
    
    return question, answer, op, level, name
