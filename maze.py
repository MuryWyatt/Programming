import pygame
from settings import *

# Screen settings
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Python Game")

# Maze List with gaps
# pygame.Rect(x, y, width, height): This function creates a rectangle with the specified position (x, y) and dimensions (width, height).
maze_walls = [
    pygame.Rect(50, 50, 200, 10),
    pygame.Rect(50, 50, 10, 200),
    pygame.Rect(50, 350, 10, 200),
    pygame.Rect(50, 540, 200, 10),
    pygame.Rect(150, 150, 200, 10),
    pygame.Rect(150, 150, 10, 200),
    pygame.Rect(150, 440, 200, 10),
    pygame.Rect(350, 50, 200, 10),
    pygame.Rect(350, 540, 200, 10),
    pygame.Rect(440, 150, 10, 200),
    pygame.Rect(540, 50, 10, 200),
    pygame.Rect(540, 350, 10, 200)
]

def draw_maze():
    for wall in maze_walls:
        pygame.draw.rect(screen, WHITE, wall)