import pygame
import sys
import os
import inventory
import mall_map
import npc
import puzzle
from puzzle import solve_puzzle


pygame.init()


# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_SPEED = 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mall Mania")
clock = pygame.time.Clock()

# Load assets
ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')
player_img = pygame.image.load(os.path.join(ASSETS_DIR, "player.png")).convert_alpha()
player_img = pygame.transform.scale(player_img, (50, 50))  # Resize player sprite to 50x50 pixels
npc_img = pygame.image.load(os.path.join(ASSETS_DIR, "npc.png")).convert_alpha()
font = pygame.font.Font(None, 36)

# Load background images
backgrounds = {
    "Entrance": pygame.image.load(os.path.join(ASSETS_DIR, "entrance_bg.png")),
    "Food Court": pygame.image.load(os.path.join(ASSETS_DIR, "foodcourt_bg.png")),
    "Clothing Store": pygame.image.load(os.path.join(ASSETS_DIR, "clothingstore_bg.png")),
    "Electronics Store": pygame.image.load(os.path.join(ASSETS_DIR, "electronicstore_bg.png")),
}

# Game state
player_x, player_y = WIDTH // 2, HEIGHT // 2
current_location = "Entrance"
inventory_items = []
running = True

# Game state
interaction_completed = {
    "Food Court": False,
    "Clothing Store": False,
    "Electronics Store": False,
    "Entrance": False,
}

class InputBox:
    def __init__(self, x, y, w, h, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.font = font
        self.text = ''
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                pass
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def draw(self, screen):
        # Draw the input box
        pygame.draw.rect(screen, self.color, self.rect, 2)
        txt_surface = self.font.render(self.text, True, BLACK)
        screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))



# Function to draw input box
def draw_input_box(screen, input_text, active, x=200, y=500, width=400, height=40, font=None):
    box_color = (0, 200, 0) if active else (200, 200, 200)
    pygame.draw.rect(screen, box_color, (x, y, width, height), border_radius=5)

    text_surface = font.render(input_text, True, BLACK)
    screen.blit(text_surface, (x + 10, y + (height - text_surface.get_height()) // 2))


# Main game loop
def main():
    global player_x, player_y, current_location, running
    input_box = InputBox(10, HEIGHT - 40, 200, 32, font)
    input_text = ""  # Store user input
    active = False  # Track if the input box is active

    while running:
        screen.fill(WHITE)  # Clear the screen
        draw_location(current_location)  # Draw location
        draw_inventory()  # Draw inventory
        draw_player(player_x, player_y)  # Draw player
        input_box.draw(screen)  # Draw input box

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            elif event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_RETURN:
                    process_command(input_text)  # Process the input command
                    input_text = ""  # Clear the input box
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]  # Remove last character
                else:
                    input_text += event.unicode  # Add typed character

            input_box.handle_event(event)  # Handle input box events

        # Draw input box
        draw_input_box(screen, input_text, active, font=font)

        # Handle movement
        keys = pygame.key.get_pressed()
        player_x, player_y = handle_movement(keys, player_x, player_y)

        handle_interactions()

        # Update the display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


# Function to process commands
def process_command(command):
    global current_location
    command = command.strip().lower()

    if command.startswith("go "):  # Check if the command starts with 'go'
        location = command[3:].strip().title()  # Extract the location and title-case it
        if location in backgrounds:  # Validate if the location exists
            current_location = location
            print(f"You moved to: {current_location}")
        else:
            print(f"Invalid location: {location}")
    else:
        print(f"Unknown command: {command}")

def handle_movement(keys, x, y):
    if keys[pygame.K_LEFT] and x > 0:
        x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] and x < WIDTH - player_img.get_width():
        x += PLAYER_SPEED
    if keys[pygame.K_UP] and y > 0:
        y -= PLAYER_SPEED
    if keys[pygame.K_DOWN] and y < HEIGHT - player_img.get_height():
        y += PLAYER_SPEED
    return x, y


def draw_location(location):
    if location in backgrounds:
        screen.blit(backgrounds[location], (0, 0))  # Draw the background image
    else:
        screen.fill(WHITE)  # Fallback in case no background is found
    
    # Display the current location as text overlay
    text = font.render(f"Location: {location}", True, BLACK)
    screen.blit(text, (10, 10))


def draw_inventory():
    inventory_list = ", ".join(inventory_items) if inventory_items else "Empty"
    text = font.render(f"Inventory: {inventory_list}", True, BLACK)
    screen.blit(text, (10, 50))


def draw_player(x, y):
    screen.blit(player_img, (x, y))


def handle_interactions():
    """
    Handles interactions with NPCs based on the current location.
    Displays riddles and invokes puzzle-solving logic.
    """
    global current_location
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:  # Interact key
        if current_location in interaction_completed:
            if interaction_completed[current_location]:
                print("You have already interacted here. Nothing more to do.")
            else:
                # Check if the NPC module has the `talk_to_npc` function
                if hasattr(npc, "talk_to_npc"):
                    npc_riddle = npc.talk_to_npc(current_location)  # Fetch riddle for the current location
                    if npc_riddle:
                        display_npc_riddle(npc_riddle)  # Display the riddle and manage user input
                        interaction_completed[current_location] = True  # Mark as completed
                    else:
                        print("There's no one to talk to here.")
                else:
                    print("NPC interaction functionality is not implemented.")
        else:
            print("No interaction available at this location.")


def display_npc_riddle(riddle):
    """
    Displays a riddle from the NPC, manages user input, and validates the answer.
    """
    overlay_width, overlay_height = 500, 300
    overlay_x = (WIDTH - overlay_width) // 2
    overlay_y = (HEIGHT - overlay_height) // 2

    # Create a semi-transparent overlay
    overlay = pygame.Surface((overlay_width, overlay_height), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, 220))  # White with transparency

    # Input box specific to the riddle
    riddle_input_box = InputBox(overlay_x + 50, overlay_y + 200, 400, 40, font)
    active = True  # Keeps the riddle loop active

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            riddle_input_box.handle_event(event)

            # Submit answer on Enter key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                user_answer = riddle_input_box.text.strip().lower()
                active = False  # Exit the riddle input loop

        # Redraw the main screen
        screen.blit(backgrounds[current_location], (0, 0))
        draw_inventory()
        draw_player(player_x, player_y)

        # Draw the riddle overlay
        screen.blit(overlay, (overlay_x, overlay_y))

        # Load and display NPC image
        npc_image = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_DIR, "npc.png")).convert_alpha(), (100, 100))
        screen.blit(npc_image, (WIDTH // 2 - 50, overlay_y - 120))

        # Draw the riddle text
        riddle_surface = font.render(riddle, True, BLACK)
        screen.blit(riddle_surface, (overlay_x + (overlay_width - riddle_surface.get_width()) // 2, overlay_y + 50))

        # Draw the riddle input box
        riddle_input_box.draw(screen)

        pygame.display.flip()

    # Validate the answer
    if validate_riddle_answer(current_location, riddle_input_box.text.strip().lower()):
        print("Correct! Here's your reward.")
        reward = npc.give_item(current_location)
        if reward and reward not in inventory_items:
            inventory_items.append(reward)
    else:
        print("Incorrect answer. Try again later!")



def get_user_input(prompt_text=None, npc_image_path=None):
    """
    Collects user input with a semi-transparent overlay and optional prompt text.

    Args:
        prompt_text (str): The text to display as a prompt (e.g., a riddle or question).
        npc_image_path (str): Path to the NPC image to display (optional).

    Returns:
        str: The user's input as a lowercase string.
    """
    # Overlay dimensions
    overlay_width, overlay_height = 400, 200
    overlay_x = (WIDTH - overlay_width) // 2
    overlay_y = (HEIGHT - overlay_height) // 2

    # Create a semi-transparent overlay surface
    overlay = pygame.Surface((overlay_width, overlay_height))
    overlay.set_alpha(200)  # Set transparency
    overlay.fill(WHITE)

    # Input box setup
    input_box = InputBox(overlay_x + 50, overlay_y + 120, 300, 32, font)
    user_input = ""
    active = True

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Exit input mode
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

            input_box.handle_event(event)  # Handle input box events

        # Draw the overlay on top of the game screen
        screen.blit(overlay, (overlay_x, overlay_y))

        # Render the prompt text on the overlay
        if prompt_text:
            prompt_surface = font.render(prompt_text, True, BLACK)
            prompt_x = overlay_x + (overlay_width - prompt_surface.get_width()) // 2
            prompt_y = overlay_y + 20
            screen.blit(prompt_surface, (prompt_x, prompt_y))

        # Draw the NPC image on the overlay (if provided)
        if npc_image_path:
            npc_image = pygame.image.load(npc_image_path).convert_alpha()
            npc_image = pygame.transform.scale(npc_image, (100, 100))
            screen.blit(npc_image, (overlay_x + 20, overlay_y + 50))

        # Draw the input box on the overlay (always on top)
        input_box.draw(screen)

        # Update display
        pygame.display.update()

    return user_input.strip().lower()

def give_item_wrapper(npc, location, inventory_items):
    """
    A wrapper function to adapt the call for the NPC's give_item method.
    """
    try:
        return npc.give_item(location)  # Pass only the location if that's all it accepts
    except Exception as e:
        print(f"Error in give_item call: {e}")
        return None
        
def validate_riddle_answer(location, answer):
    """
    Validates the user's answer to the riddle based on location.
    
    Args:
        location (str): The current location.
        answer (str): The user's answer to the riddle.
    
    Returns:
        bool: True if the answer is correct, False otherwise.
    """
    correct_answers = {
        "Food Court": "pizza",
        "Clothing Store": "jacket",
        "Electronics Store": "laptop"
    }
    return correct_answers.get(location) == answer

def process_npc_response(answer):
    """
    Processes the user's response to an NPC's riddle and awards the reward.
    
    Args:
        answer (str): The user's answer to the riddle.
    """
    global inventory_items

    if validate_riddle_answer(current_location, answer):
        print("Correct! Here's your reward.")
        rewards = {
            "Food Court": "pizza",
            "Clothing Store": "jacket",
            "Electronics Store": "laptop"
        }
        reward = rewards.get(current_location)
        if reward and reward not in inventory_items:
            inventory_items.append(reward)
            print(f"You received: {reward}")
        else:
            print("No items left to collect here!")
    else:
        print("Incorrect answer. Try again later!")

def display_npc_riddle(riddle):
    """
    Displays a riddle from the NPC and validates the answer.
    Awards a reward if the answer is correct.
    """
    # Overlay dimensions
    overlay_width, overlay_height = 500, 300
    overlay_x = (WIDTH - overlay_width) // 2
    overlay_y = (HEIGHT - overlay_height) // 2

    # Create a semi-transparent white overlay
    overlay = pygame.Surface((overlay_width, overlay_height), pygame.SRCALPHA)
    overlay.fill((200, 200, 200, 200))  # 200 is transparency level

    # Draw the semi-transparent overlay
    screen.blit(overlay, (overlay_x, overlay_y))
    
    # Render and draw the NPC image
    npc_image = pygame.image.load(os.path.join(ASSETS_DIR, "npc.png")).convert_alpha()
    npc_image = pygame.transform.scale(npc_image, (100, 100))
    screen.blit(npc_image, (WIDTH // 2 - 50, overlay_y - 120))  # Positioned above the overlay

    # Render and draw the riddle text on the overlay
    riddle_text = font.render(riddle, True, BLACK)
    text_x = overlay_x + (overlay_width - riddle_text.get_width()) // 2
    text_y = overlay_y + 50  # Adjust within the transparent box
    screen.blit(riddle_text, (text_x, text_y))

    # Update the display to show all elements
    pygame.display.flip()

    # Prompt user for input after drawing the riddle
    print("Solve the riddle to earn a reward!")
    user_answer = get_user_input()  # Wait for user input

    # Validate and handle the answer
    if validate_riddle_answer(current_location, user_answer):
        print("Correct! Here's your reward.")
        try:
            reward = npc.give_item(current_location)
            if reward and reward not in inventory_items:
                inventory_items.append(reward)
                print(f"You received: {reward}")
            else:
                print("No items left to collect here!")
        except Exception as e:
            print(f"Error in NPC reward logic: {e}")
    else:
        print("Incorrect answer. Try again later!")

    
# Start the game
if __name__ == "__main__":
    main()