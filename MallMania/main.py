import pygame
import sys
import mall_map
import inventory
import puzzle
import npc

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
player_img = pygame.image.load("assets/player.png").convert_alpha()
npc_img = pygame.image.load("assets/npc.png").convert_alpha()
font = pygame.font.Font(None, 36)

# Game state
player_x, player_y = WIDTH // 2, HEIGHT // 2
current_location = "Entrance"
inventory_items = []
running = True

# Main game loop
def main():
    global player_x, player_y, current_location, running

    while running:
        screen.fill(WHITE)
        draw_location(current_location)
        draw_inventory()
        draw_player(player_x, player_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        player_x, player_y = handle_movement(keys, player_x, player_y)

        handle_interactions()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

def handle_movement(keys, x, y):
    if keys[pygame.K_LEFT] and x > 0:
        x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] and x < WIDTH - 50:  # Adjust for player sprite size
        x += PLAYER_SPEED
    if keys[pygame.K_UP] and y > 0:
        y -= PLAYER_SPEED
    if keys[pygame.K_DOWN] and y < HEIGHT - 50:
        y += PLAYER_SPEED
    return x, y

def draw_location(location):
    # Display the current location
    text = font.render(f"Location: {location}", True, BLACK)
    screen.blit(text, (10, 10))

def draw_inventory():
    # Display inventory
    text = font.render("Inventory: " + ", ".join(inventory_items), True, BLACK)
    screen.blit(text, (10, 50))

def draw_player(x, y):
    # Draw player sprite
    screen.blit(player_img, (x, y))

def handle_interactions():
    global current_location

    # Detect key interactions (e.g., SPACE to interact)
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
