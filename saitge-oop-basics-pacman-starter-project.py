import pygame
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Python Game")

clock = pygame.time.Clock()

# Tuples for Colors
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128,)

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

def handle_input(pacman):
    """Handle user input for movement"""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]: pacman.move("UP")
    if keys[pygame.K_DOWN]: pacman.move("DOWN")
    if keys[pygame.K_LEFT]: pacman.move("LEFT")
    if keys[pygame.K_RIGHT]: pacman.move("RIGHT")

def check_collision(pacman, ghost):
    """Check if Pac-Man collides with the ghost"""
    distance = ((pacman.x - ghost.x) ** 2 + (pacman.y - ghost.y) ** 2) ** 0.5
    return distance < 20  # Collision threshold

# Initialize game objects
pacman = PacMan(300, 300)
ghost = Ghost(100, 100, RED)

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
    pacman.draw()
    ghost.draw()

    # Check for collision
    if check_collision(pacman, ghost):
        print("Game Over! Pac-Man was caught!")
        running = False

    pygame.display.flip()
    clock.tick(30) 



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

    def draw(self):
        """
        Draw the pellet on the screen as a yellow circle.
        """
        pygame.draw.circle(screen, ORANGE, (self.x, self.y), 10)

    def is_colliding(self, pacman):
        """
        Check if Pac-Man has collided with this pellet.
        Parameters:
            pacman (PacMan): The PacMan object to check for collision.
        Returns:
            bool: True if Pac-Man's position is close enough to the pellet, else False.
        """
        pacman_x, pacman_y = pacman.get_position()
        distance = ((self.x - pacman_x) ** 2 + (self.y - pacman_y) ** 2) ** 0.5
        return distance < 15  # Collision threshold (distance between Pac-Man and pellet)





# Pellet list (you can customize the positions)
pellets = [
    Pellet(100, 100), Pellet(200, 100), Pellet(300, 100), Pellet(400, 100), Pellet(500, 100),
    Pellet(100, 200), Pellet(500, 200),
    Pellet(100, 300), Pellet(500, 300),
    Pellet(100, 400), Pellet(500, 400),
    Pellet(100, 500), Pellet(500, 500),
    Pellet(200, 400), Pellet(300, 400), Pellet(400, 400)
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



pygame.quit()