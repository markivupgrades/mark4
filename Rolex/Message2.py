#!/usr/bin/env python3

import pygame
import sys

# Screen dimensions
WIDTH, HEIGHT = 1920, 1280

class MessageDisplay:
    def __init__(self, message, font_name, size, color, background):
        pygame.init()
        pygame.mouse.set_visible(False)

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Message Display")

        self.background_image = pygame.image.load(f"/home/pi/Rolex/png/{background}.png")
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))

        font_path = pygame.font.match_font(font_name)
        self.font = pygame.font.Font(font_path, size) if font_path else pygame.font.Font(None, size)

        self.text_color = pygame.Color(color)
        self.messages = message.split('\n')
        self.rendered_messages = [self.font.render(m, True, self.text_color) for m in self.messages]

        self.run()

    def draw_screen(self):
        self.screen.blit(self.background_image, (0, 0))

        text_height = len(self.rendered_messages) * (self.rendered_messages[0].get_rect().height + 10)
        y = HEIGHT // 2 - text_height // 2 - 20
        for msg in self.rendered_messages:
            text_rect = msg.get_rect()
            text_rect.centerx = WIDTH // 2
            text_rect.y = y
            self.screen.blit(msg, text_rect)
            y += text_rect.height + 10

        pygame.display.flip()

    def run(self):
        self.draw_screen()
        pygame.time.set_timer(pygame.USEREVENT, 1200000)  # 20 minutes in milliseconds
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.USEREVENT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    if len(sys.argv) < 6:
        sys.exit(1)

    message = sys.argv[1]
    font_name = sys.argv[2]
    size = int(sys.argv[3])
    color = sys.argv[4]
    background = sys.argv[5]

    MessageDisplay(message, font_name, size, color, background)