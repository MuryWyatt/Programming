import pygame
from settings import *
from maze import *
import random

class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.speed = 4
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])

    def move_towards(self, pacman):
        """Chase Pac-Man and avoid maze walls"""
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        best_direction = None
        min_distance = float('inf')

        for direction in directions:
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
            new_rect = pygame.Rect(new_x - 15, new_y - 15, 30, 30)
            if not any(new_rect.colliderect(wall) for wall in maze_walls):
                distance = ((new_x - pacman.x) ** 2 + (new_y - pacman.y) ** 2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
                    best_direction = direction
# Move the ghost in the best direction so they get closer to Pac-Man
# If the best direction is found, update the ghost's position based on that direction
        if best_direction:
            if best_direction == "UP":
                self.y -= self.speed
            elif best_direction == "DOWN":
                self.y += self.speed
            elif best_direction == "LEFT":
                self.x -= self.speed
            elif best_direction == "RIGHT":
                self.x += self.speed
        else:
            # If no direction is found, follow the wall
            self.follow_wall()

    def follow_wall(self):
        """Follow the wall to avoid getting stuck"""
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        random.shuffle(directions)  # Randomize direction order to avoid getting stuck

        for direction in directions:
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
            new_rect = pygame.Rect(new_x - 15, new_y - 15, 30, 30)
            if not any(new_rect.colliderect(wall) for wall in maze_walls):
                self.x, self.y = new_x, new_y
                break

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 15)
