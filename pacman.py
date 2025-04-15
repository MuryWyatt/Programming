import pygame
from settings import *
from maze import *

class PacMan:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 8
        self.history = []  # Store movement history

    def move(self, direction):
        """Move Pac-Man within screen boundaries and avoid maze walls"""
        new_x, new_y = self.x, self.y
        if direction == "UP":
            new_y -= self.speed
        elif direction == "DOWN":
            new_y += self.speed
        elif direction == "LEFT":
            new_x -= self.speed
        elif direction == "RIGHT":
            new_x += self.speed
        
        # Check for collisions with maze walls
        # This creates a rectangular boundary for the moving entity (e.g., Pac-Man or a ghost) at its new potential position (new_x, new_y).
        # The pygame.Rect() function defines a rectangle using four parameters:
        # new_x - 15: The top-left X coordinate (subtracting 15 centers it correctly).
        # new_y - 15: The top-left Y coordinate (subtracting 15 centers it correctly).
        # 30, 30: The width and height of the entity (assuming it's a circle with a 15-pixel radius).
        # This rectangle acts as a hitbox for collision detection.
        new_rect = pygame.Rect(new_x - 15, new_y - 15, 30, 30)
        if not any(new_rect.colliderect(wall) for wall in maze_walls):
            self.x, self.y = new_x, new_y
            self.history.append((self.x, self.y))

    def get_position(self):
        return self.x, self.y

    def draw(self):
        pygame.draw.circle(screen, YELLOW, self.get_position(), 15)
