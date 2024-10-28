# Mall Mania

Welcome to **Mall Mania**, a text-based game built with Python! Explore the mall, interact with NPCs, solve puzzles, and collect items to complete various challenges.

## Game Features

- **Player Movement**: Navigate through different stores and areas in the mall.
- **Inventory System**: Collect items during your adventure.
- **Puzzle/Challenge Mechanism**: Solve trivia and word games to progress.
- **NPC Interactions**: Talk to store owners and other mall characters for hints and help.

## Gameplay

The player starts at the mall entrance and can move through different locations, interact with characters, and take on challenges. Here's a sneak peek at the gameplay mechanics:

- **Move**: Type `go <location>` to move to a different area.
- **Take Items**: Collect items by typing `take <item>` when available.
- **Solve Puzzles**: Solve randomly generated puzzles and win rewards.
- **Talk**: Engage with NPCs using the `talk <npc>` command.

## Project Structure

```plaintext
shopping_mall_game/
├── main.py           # Main game script
├── mall_map.py       # Defines the map of the mall and locations
├── inventory.py      # Manages the player's inventory system
├── puzzle.py         # Contains logic for puzzle challenges
└── npc.py            # Defines NPC interactions and dialogues
