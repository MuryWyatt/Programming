import pygame
from settings import *
from maze import *
from pacman import *

class Pellet:
    def __init__(self, x, y):
        """
        Initialize a new Pellet at the given (x, y) position.
        Parameters:
            x (int): X-coordinate of the pellet.
            y (int): Y-coordinate of the pellet.
        """
        self.x = x
        self.y = y
        self.radius = 5 

    def draw(self, surface): # <--- Add 'surface' as an argument
        """
        Draw the pellet onto the specified surface.
        Parameters:
            surface (pygame.Surface): The surface to draw the pellet on.
        """
        # Use the passed 'surface' argument instead of the global 'screen'
        pygame.draw.circle(surface, ORANGE, (self.x, self.y), self.radius) # Use self.radius

    def is_colliding(self, pacman):
        pacman_x, pacman_y = pacman.get_position()
        distance = ((self.x - pacman_x) ** 2 + (self.y - pacman_y) ** 2) ** 0.5
        # Use a defined collision distance, maybe based on radii
        return distance < 15 # Adjust threshold as needed




# Pellet list (you can customize the positions)
pellets = [
    Pellet(100, 100), 
    Pellet(100, 200),
    Pellet(100, 300),
    Pellet(100, 400),
    Pellet(100, 500), 
    Pellet(200, 100),
    Pellet(200, 200),
    Pellet(200, 300),
    Pellet(200, 400),
    Pellet(200, 500), 
    Pellet(300, 100),
    Pellet(300, 200),
    Pellet(300, 400),
    Pellet(300, 500), 
    Pellet(400, 100),
    Pellet(400, 200),
    Pellet(400, 300),
    Pellet(400, 400),
    Pellet(400, 500), 
    Pellet(500, 100), 
    Pellet(500, 200),
    Pellet(500, 300),
    Pellet(500, 400),
    Pellet(500, 500),
    
]

def draw_pellets():
    """
    Draw all pellets on the screen.
    Loops through the list of pellet objects and calls their draw method.
    """
    for pellet in pellets:
        pellet.draw(screen)

def check_pellet_collection(pacman):
    """
    Check if Pac-Man collects any pellets. 
    If Pac-Man collides with a pellet, remove it from the list.
    Parameters:
        pacman (PacMan): The PacMan object to check for collisions with pellets.
    """
    global pellets  # Modify the global pellets list
    # Create a new list excluding the pellets that Pac-Man ate
    pellets = [pellet for pellet in pellets if not pellet.is_colliding(pacman)]