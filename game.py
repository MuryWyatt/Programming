import pygame
from settings import *
from maze import *
from pacman import *
from ghosts import *
from pellets import *

# Initialize pygame
pygame.init()

clock = pygame.time.Clock()


def handle_input(pacman):
    """Handle user input for movement"""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]: pacman.move("UP")
    if keys[pygame.K_DOWN]: pacman.move("DOWN")
    if keys[pygame.K_LEFT]: pacman.move("LEFT")
    if keys[pygame.K_RIGHT]: pacman.move("RIGHT")

def check_ghost_collision(pacman, ghost):
    """Check if Pac-Man collides with the ghost"""
    distance = ((pacman.x - ghost.x) ** 2 + (pacman.y - ghost.y) ** 2) ** 0.5
    return distance < 20  # Collision threshold

def check_pellet_collision(pacman, pellets):
    """Check if Pac-Man collides with the pellets"""
    distance = ((pacman.x - pellets.x) ** 2 + (pacman.y - pellets.y) ** 2) ** 0.5
    print(pellets.x, pellets.y)
    return distance < 20  # Collision threshold

# Initialize game objects
pacman = PacMan(300, 300)
ghost = Ghost(100, 100, RED)
pellets = Pellet(0,0)

running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle user input
    handle_input(pacman)

    # Move ghost
    ghost.move_towards(pacman)

    # Draw game elements
    draw_maze()
    draw_pellets()
    pacman.draw()
    ghost.draw()
    

    # Check for collision
    if check_ghost_collision(pacman, ghost):
        print("Game Over! Pac-Man was caught!")
        running = False

        # Check for collision
    if check_pellet_collision(pacman, pellets):
        for pellet in pellets:
            if pacman.x == pellet.x and pacman.y == pellet.y:
                print("PacMan ate the pellet")


    pygame.display.flip()
    clock.tick(30) 

pygame.quit()

