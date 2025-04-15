import pygame

class Fruits:

import os
import random # Can be useful for random fruit spawns if needed

# --- Configuration ---
# Store data for different fruit types
# Format: 'type_name': {'points': value, 'image': 'filename.png', 'duration': milliseconds}
FRUIT_DATA = {
    'cherry':     {'points': 100,  'image': 'cherry.png',     'duration': 10000}, # 10 seconds to grab
    'banana':     {'points': 200,  'image': 'banana.png',     'duration': 9000}, # 9 seconds to grab
    'strawberry': {'points': 300,  'image': 'strawberry.png', 'duration': 9000}, # 9 seconds to grab
    'orange':     {'points': 500,  'image': 'orange.png',     'duration': 9000}, # 9 seconds to grab
    'apple':      {'points': 700,  'image': 'apple.png',      'duration': 8000}, # 8 seconds to grab
    'melon':      {'points': 1000, 'image': 'melon.png',      'duration': 8000}, # 8 seconds to grab
    'galaxian':   {'points': 2000, 'image': 'galaxian.png',   'duration': 7000}, # 7 seconds to grab
    'bell':       {'points': 3000, 'image': 'bell.png',       'duration': 7000}, # 7 seocnds to grab
    'key':        {'points': 5000, 'image': 'key.png',        'duration': 6000}, # 6 seconds to grab
    
}

# Define the base path for fruit images (adjust as necessary)
# Assumes your images are in a subdirectory like 'assets/images/fruits'
IMAGE_FOLDER = os.path.join('assets', 'images', 'fruits')

# --- Fruit Class ---
class Fruit(pygame.sprite.Sprite):
    """
    Represents a fruit item in the Pac-Man game.

    Attributes:
        type (str): The type of fruit (e.g., 'cherry', 'strawberry').
        points (int): Score value awarded when eaten.
        lifespan (int): How long the fruit stays on screen (in milliseconds).
        image (pygame.Surface): The visual representation of the fruit.
        rect (pygame.Rect): The rectangular area of the fruit for positioning and collision.
        is_active (bool): True if the fruit is currently visible and collectible.
        creation_time (int): The time (in milliseconds) when the fruit was created/activated.
    """
    def __init__(self, fruit_type, position, groups=None):
        """
        Initializes a Fruit instance.

        Args:
            fruit_type (str): The key corresponding to the desired fruit in FRUIT_DATA.
            position (tuple): The (x, y) coordinates for the center of the fruit.
            groups (pygame.sprite.Group or list): Optional sprite group(s) to add this fruit to.
        """
        # Initialize the parent Sprite class
        if groups:
            super().__init__(groups)
        else:
            super().__init__()


        if fruit_type not in FRUIT_DATA:
            raise ValueError(f"Unknown fruit type: {fruit_type}")

        self.type = fruit_type
        data = FRUIT_DATA[self.type]
        self.points = data['points']
        self.lifespan = data['duration'] # Time to stay active (ms)

        # Load image
        image_path = os.path.join(IMAGE_FOLDER, data['image'])
        try:
            # Load image with transparency support
            self.image = pygame.image.load(image_path).convert_alpha()
        except pygame.error as e:
            print(f"Error loading fruit image: {image_path}")
            print(e)
            # Create a fallback surface if image loading fails
            # Make it visible so you know there's an error
            self.image = pygame.Surface([25, 25]) # Adjust size as needed
            self.image.fill((255, 0, 255)) # Magenta often indicates missing textures
            pygame.draw.circle(self.image, (255, 255, 0), (12, 12), 10) # Yellow circle


        # Set position and collision rectangle
        # self.rect will store the fruit's position and size
        self.rect = self.image.get_rect(center=position)

        # Activation state and timer
        self.is_active = True
        self.creation_time = pygame.time.get_ticks() # Record spawn time using Pygame's timer

    def update(self):
        """
        Updates the fruit's state each frame.
        Checks if the fruit's lifespan has expired.
        """
        if not self.is_active:
            return # Do nothing if already eaten or disappeared

        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.creation_time

        # Check if the fruit should disappear
        if elapsed_time >= self.lifespan:
            self.disappear()

    def eaten(self):
        """
        Handles the fruit being eaten by Pac-Man.
        Deactivates the fruit and returns its point value.
        """
        if self.is_active:
            self.is_active = False
            # print(f"{self.type.capitalize()} eaten! +{self.points} points.") # Optional: for debugging
            self.kill() # Remove the sprite from all groups it belongs to
            return self.points
        return 0 # Return 0 if already inactive

    def disappear(self):
        """
        Handles the fruit disappearing after its time runs out.
        Deactivates the fruit.
        """
        if self.is_active:
            self.is_active = False
            # print(f"{self.type.capitalize()} disappeared.") # Optional: for debugging
            self.kill() # Remove the sprite from all groups

    def draw(self, screen):
        """
        Draws the fruit onto the specified surface (screen) if active.
        Note: If using sprite groups, group.draw(screen) is often preferred.
              This method is here for completeness or if not using groups for drawing.
        """
        if self.is_active:
            screen.blit(self.image, self.rect)

# --- How to Use in your Game ---

# 1. Initialization (usually done once at the start)
# pygame.init()
# screen = pygame.display.set_mode((800, 600)) # Your screen dimensions
# clock = pygame.time.Clock()

# # Create sprite groups
# all_sprites = pygame.sprite.Group() # Optional: For managing all sprites
# fruit_group = pygame.sprite.Group() # Specific group for fruit(s)

# # Variable to hold the currently active fruit (if any)
# current_fruit = None

# # Game state variables (examples)
# score = 0
# level = 1 # Or however you track levels
# pellets_eaten = 0
# TOTAL_PELLETS_LEVEL_1 = 240 # Example

# # 2. Spawning a Fruit (inside your game loop or based on game events)
# # Example: Spawn a cherry when 70 pellets are eaten, and then an orange at 170
# def check_fruit_spawn(pellets_eaten_count, current_level, active_fruit):
#     if active_fruit is None: # Only spawn if no fruit is currently active
#         spawn_pos = (400, 300) # Determine spawn location (e.g., center)
#         fruit_to_spawn = None

#         if current_level == 1:
#             if pellets_eaten_count == 70:
#                 fruit_to_spawn = 'cherry'
#             elif pellets_eaten_count == 170:
#                  fruit_to_spawn = 'strawberry' # Second fruit for level 1
#         elif current_level == 2:
#              if pellets_eaten_count == 70:
#                  fruit_to_spawn = 'orange'
#              # Add more conditions for other levels/pellets

#         if fruit_to_spawn:
#             print(f"Spawning {fruit_to_spawn}!")
#             # Add the new fruit to relevant groups
#             new_fruit = Fruit(fruit_to_spawn, spawn_pos, (all_sprites, fruit_group))
#             return new_fruit # Return the newly created fruit instance
#     return active_fruit # Return the existing fruit or None


# # 3. Game Loop
# running = True
# while running:
#     # --- Event Handling ---
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         # Handle other input (Pac-Man movement etc.)

#     # --- Game Logic ---
#     # Move Pac-Man, ghosts, etc.
#     # Check pellet eating
#     # if pacman_ate_pellet:
#     #    pellets_eaten += 1
#     #    score += 10
#     #    current_fruit = check_fruit_spawn(pellets_eaten, level, current_fruit)


#     # Update all sprites (this will call current_fruit.update() if it's in all_sprites)
#     all_sprites.update()

#     # Check for Pac-Man / Fruit collision
#     # Assuming pacman_sprite is your Pac-Man sprite object
#     # collided_fruit = pygame.sprite.spritecollideany(pacman_sprite, fruit_group)
#     # if collided_fruit:
#     #    points_earned = collided_fruit.eaten() # Handles removal and returns points
#     #    score += points_earned
#     #    current_fruit = None # Mark that the fruit is gone

#     # Check if the current fruit has disappeared on its own
#     if current_fruit and not current_fruit.is_active:
#         current_fruit = None # Fruit timed out


#     # --- Drawing ---
#     # screen.fill((0, 0, 0)) # Black background
#     # Draw maze, pellets, Pac-Man, ghosts...

#     # Draw all sprites in the group (includes the fruit if it exists)
#     # all_sprites.draw(screen)

#     # Or draw fruit specifically if not using all_sprites for drawing
#     # if current_fruit:
#     #    current_fruit.draw(screen)

#     # Display score, lives etc.
#     # pygame.display.flip()
#     # clock.tick(60) # Limit frame rate

# pygame.quit()