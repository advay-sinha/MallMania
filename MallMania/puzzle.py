import random

def solve_puzzle():
    puzzles = [
        {"question": "What is 5 + 7?", "answer": "12"},
        {"question": "Spell 'Mall Mania' backward.", "answer": "ainam llam"}
    ]
    puzzle = random.choice(puzzles)
    print(f"Puzzle: {puzzle['question']}")
    user_answer = input("> ").strip().lower()
    return user_answer == puzzle["answer"]
