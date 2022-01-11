import sys

import pygame
from settings import Settings
from ship import Ship


class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Space Invaders Clone")

        self.ship = Ship(self)

        self.bg_colour = self.settings.bg_colour
    def run_game(self):
        while True:
            self.check_events()
            self.update_screen()
            self.ship.update()

    def check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.ship.moving_right = True
                    elif event.key == pygame.K_a:
                        self.ship.moving_left = True
                    elif event.key == pygame.K_ESCAPE:
                        sys.exit()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        self.ship.moving_right = False
                    elif event.key == pygame.K_a:
                        self.ship.moving_left = False
    def update_screen(self):
            self.screen.fill(self.bg_colour)
            self.ship.blitme()
            pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()