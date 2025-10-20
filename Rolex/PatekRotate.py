import pygame
import sys
import os
from datetime import datetime

# 🔧 Set absolute path to image directory
base_path = "/home/pi/Rolex/png"

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Real-Time Clock with Date")

screen_width, screen_height = screen.get_size()
center = (screen_width // 2, screen_height // 2)

# 🖼️ Load and scale background
background = pygame.image.load(os.path.join(base_path, "PatekFACE.png")).convert()
background = pygame.transform.scale(background, (screen_width, screen_height))

# 🕰️ Load clock hands
hour_hand = pygame.image.load(os.path.join(base_path, "PatekHOUR.png")).convert_alpha()
minute_hand = pygame.image.load(os.path.join(base_path, "PatekMINUTE.png")).convert_alpha()
second_hand = pygame.image.load(os.path.join(base_path, "PatekSECOND.png")).convert_alpha()

# 🗓️ Font and date setup
font = pygame.font.SysFont("Copperplate", 60, bold=True)
date_color = (0, 0, 0)
clock = pygame.time.Clock()

last_day = None
date_surface = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

    now = datetime.now()
    seconds = now.second + now.microsecond / 1_000_000
    minutes = now.minute + seconds / 60
    hours = now.hour % 12 + minutes / 60

    second_angle = -6 * seconds
    minute_angle = -6 * minutes
    hour_angle = -30 * hours

    if now.day != last_day:
        date_text = str(now.day)
        date_surface = font.render(date_text, True, date_color)
        last_day = now.day

    rotated_hour = pygame.transform.rotate(hour_hand, hour_angle)
    rotated_hour_rect = rotated_hour.get_rect(center=center)

    rotated_minute = pygame.transform.rotate(minute_hand, minute_angle)
    rotated_minute_rect = rotated_minute.get_rect(center=center)

    rotated_second = pygame.transform.rotate(second_hand, second_angle)
    rotated_second_rect = rotated_second.get_rect(center=center)

    screen.blit(background, (0, 0))
    screen.blit(date_surface, (1317 - date_surface.get_width() // 2, 613))
    screen.blit(rotated_hour, rotated_hour_rect)
    screen.blit(rotated_minute, rotated_minute_rect)
    screen.blit(rotated_second, rotated_second_rect)

    pygame.display.flip()
    clock.tick(30)
