import pygame.font
import pygame
from pygame.sprite import Group
from modules.ship import Ship

class Scoreboard:
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.gameStats

        self.bg_colour = (0,0,0)
        self.font = pygame.font.Font('fonts/PressStart2P.ttf', 24)
        self.text_colour = (255,255,255)
        self.read_high_score()
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
    def prep_score(self):
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_colour)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
    def prep_high_score(self):
        high_score = round(self.stats.high_score, -1)
        high_score_str = 'HI:'+ '{:,}'.format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_colour)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
    def save_high_score(self):
        with open('score.dat', 'w') as f:
            f.write(str(self.stats.high_score))
    def read_high_score(self):
        with open('score.dat', 'r') as f:
            self.stats.high_score = int(f.read())
    def check_for_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
    def prep_level(self):
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_colour)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        self.ships = Group()
        for shipNum in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.image = pygame.image.load('images/ship-icon.png')
            ship.rect.x = 10 + shipNum * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)