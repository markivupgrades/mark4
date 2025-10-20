import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display window in full-screen mode
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("360º Rotating Image with Background")

# Get the screen dimensions
screen_width, screen_height = screen.get_size()

# Load the background image
background = pygame.image.load("PatekFACE.png").convert()

# Scale the background to match the screen size (optional, if needed)
background = pygame.transform.scale(background, (screen_width, screen_height))

# Load the rotating image
rotating_image = pygame.image.load("PatekSECOND.png").convert_alpha()

# Get the rect for the rotating image and center it
image_rect = rotating_image.get_rect(center=(screen_width // 2, screen_height // 2))

# Start the angle at 0
angle = 0

# Game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

    # Draw the background image
    screen.blit(background, (0, 0))

    # Rotate the image
    rotated_image = pygame.transform.rotate(rotating_image, angle)

    # Get the new rect and keep it centered
    rotated_rect = rotated_image.get_rect(center=image_rect.center)

    # Draw the rotated image on top of the background
    screen.blit(rotated_image, rotated_rect.topleft)

    # Update the display
    pygame.display.flip()

    # Increment the angle for rotation (clockwise)
    angle = (angle - 1) % 360

    # Control frame rate
    clock.tick(60)
