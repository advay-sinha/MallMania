def solve_puzzle(user_input=None):
    import random

    puzzles = [
    {"question": "What is 5 + 7?", "answer": "12"},
    {"question": "Spell 'Mall Mania' backward.", "answer": "ainam llam"},
    {"question": "What is 2 + 2?", "answer": "4"},
    {"question": "What is the color of the sky on a clear day?", "answer": "Blue"},
    {"question": "How many legs does a spider have?", "answer": "8"},
    {"question": "What is the first letter of the alphabet?", "answer": "A"},
    {"question": "What sound does a cow make?", "answer": "Moo"},
    {"question": "What is the opposite of 'up'?", "answer": "Down"},
    {"question": "What comes after Tuesday?", "answer": "Wednesday"},
    {"question": "How many sides does a triangle have?", "answer": "3"},
    {"question": "What is 10 - 5?", "answer": "5"}
]
    
    puzzle = random.choice(puzzles)
    print(f"Puzzle: {puzzle['question']}")

    # If input is provided, compare directly
    if user_input is not None:
        return user_input.strip().lower() == puzzle["answer"]

    # If no input provided, prompt for it (for debugging or manual testing)
    user_answer = input("> ").strip().lower()
    return user_answer == puzzle["answer"]