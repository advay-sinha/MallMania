import pygame
import sys
import os
import inventory
import mall_map
import npc
import puzzle



# Initialize Pygame
pygame.init()


# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_SPEED = 5

# Setup screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mall Mania")
clock = pygame.time.Clock()

# Load assets
ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')
# Load and scale player image
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

class InputBox:
    def __init__(self, x, y, w, h, font, color_inactive=BLACK, color_active=(0, 255, 0)):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = color_inactive
        self.color_active = color_active
        self.color = color_inactive
        self.text = ''
        self.font = font
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state if clicked inside the input box
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                print(f"Input submitted: {self.text}")  # Handle the input
                self.text = ''  # Clear input after submission
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def draw(self, screen):
        # Render the text
        txt_surface = self.font.render(self.text, True, self.color)
        # Resize the box if the text is too long
        width = max(200, txt_surface.get_width() + 10)
        self.rect.w = width
        # Blit the text and rect
        screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)



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
    input_text = " " #store user input


    # Input box state
    active = False
    input_text = ""

    while running:
        screen.fill(WHITE)  # Clear the screen
        draw_location(current_location)  # Draw location
        draw_inventory()  # Draw inventory
        draw_player(player_x, player_y)  # Draw player
        input_box.draw(screen)  # Draw input box

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if mouse click is within the input box
                if 200 <= event.pos[0] <= 600 and 500 <= event.pos[1] <= 540:
                    active = True
                else:
                    active = False
            elif event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_RETURN:
                    print(f"User Input: {input_text}")  # Process the input
                    # Example: Use input for a puzzle
                    if puzzle.solve_puzzle(input_text):
                        print("Puzzle solved!")
                    else:
                        print("Incorrect input!")
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
    global current_location
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        npc_dialogue = npc.talk_to_npc(current_location)
        if npc_dialogue:
            print(f"NPC says: {npc_dialogue}")
        else:
            item = mall_map.get_item(current_location)
            if item:
                inventory.add_item(inventory_items, item)
                print(f"You picked up: {item}")
            else:
                print("Nothing to interact with here.")


# Start the game
if __name__ == "__main__":
    main()
