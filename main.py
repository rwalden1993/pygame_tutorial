# Import the pygame module
from typing import List, Tuple, Union, Any

import pygame

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Initialize pygame
pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

GRID_WIDTH = 25  # px


def make_shape(shape: List[Tuple[int, int]]) -> List[List[Union[int, Any]]]:
    def _scalar_multiply(tup):
        return [x * GRID_WIDTH for x in tup]

    return list(map(_scalar_multiply, shape))


SQUARE = make_shape([(0, 0), (0, 2), (2, 2), (2, 0)])
I_SHAPE = make_shape([(0, 0), (1, 0), (1, 3), (0, 3)])
L_SHAPE = make_shape([(0, 0), (1, 0), (1, 2), (2, 2), (2, 3), (0, 3)])
J_SHAPE = make_shape([(1, 0), (1, 2), (0, 2), (0, 3), (2, 3), (2, 0)])
T_SHAPE = make_shape([(1, 0), (2, 0), (2, 1), (3, 1), (3, 2), (0, 2), (0, 1), (1, 1)])
S_SHAPE = make_shape([(0, 1), (1, 1), (1, 0), (3, 0), (3, 1), (2, 1), (2, 2), (0, 2)])
Z_SHAPE = make_shape([(0, 0), (2, 0), (2, 1), (3, 1), (3, 2), (1, 2), (1, 1), (0, 1)])


# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite, ):
    def __init__(self, shape):
        super(Player, self).__init__()
        self.shape = shape
        max_x = max([x for x, y in shape])
        max_y = max([y for x, y in shape])
        self.surf = pygame.Surface((max_x, max_y))
        self.color = (255, 255, 255)
        self.rect = pygame.draw.polygon(self.surf, self.color, self.shape)

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rotate_center(-90)
        if pressed_keys[K_DOWN]:
            self.rotate_center(90)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-GRID_WIDTH, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(GRID_WIDTH, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def rotate_center(self, angle):
        old_center = self.rect.center
        self.surf = pygame.transform.rotate(self.surf, angle)
        self.rect.center = old_center




# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Instantiate player. Right now, this is just a rectangle.
player = Player(SQUARE)

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Variable to keep the main loop running
running = True

# Main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    # Update the player sprite based on user keypresses
    player.update(pressed_keys)

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Draw the player on the screen
    screen.blit(player.surf, player.rect)

    # Update the display
    pygame.display.flip()

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(15)
