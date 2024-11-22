def solve_puzzle(user_input=None):
    import random

    puzzles = [
        {"question": "What is 5 + 7?", "answer": "12"},
        {"question": "Spell 'Mall Mania' backward.", "answer": "ainam llam"}
    ]

    puzzle = random.choice(puzzles)
    print(f"Puzzle: {puzzle['question']}")

    # If input is provided, compare directly
    if user_input is not None:
        return user_input.strip().lower() == puzzle["answer"]

    # If no input provided, prompt for it (for debugging or manual testing)
    user_answer = input("> ").strip().lower()
    return user_answer == puzzle["answer"]
