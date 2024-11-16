# Mall Mania

Welcome to **Mall Mania**, an exciting 2D adventure game built with Python and Pygame! Explore the mall, interact with NPCs, solve puzzles, and collect items to complete your adventure.

---

## Game Features

- **Player Movement**: Navigate visually across different stores and areas in the mall.
- **Inventory System**: Collect and manage items during your journey, displayed on-screen.
- **Puzzle Challenges**: Solve math, trivia, or word puzzles to earn rewards and progress.
- **NPC Interactions**: Chat with NPCs for hints and assistance.
- **Dynamic Gameplay**: Explore a mix of exploration, problem-solving, and interactive challenges with a visual interface.

---

## Gameplay

Start your journey at the **mall entrance**, explore different areas, and interact with NPCs, puzzles, and items.  

### Controls
- **Arrow Keys**: Move the player around.
- **Space**: Interact with NPCs or collect items.
- **ESC**: Exit the game.

---

## Project Structure

```plaintext
mall_mania/
├── main.py           # Main game script (entry point)
├── assets/           # Game assets (images for player, NPCs, and items)
│   ├── player.png    # Player sprite
│   ├── npc.png       # NPC sprite
│   ├── items/        # Item sprites (e.g., burger.png, tshirt.png)
├── mall_map.py       # Defines the mall map layout and item locations
├── inventory.py      # Handles inventory logic
├── puzzle.py         # Puzzle and challenge mechanics
└── npc.py            # NPC interactions and dialogues
