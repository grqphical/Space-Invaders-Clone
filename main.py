import sys

import pygame
from time import sleep
from modules.settings import Settings
from modules.ship import Ship
from modules.alien import Alien
from modules.bullet import Bullet
from modules.gamestats import GameStats
from modules.button import Button


class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.bg_image = pygame.image.load('images/background.png')
        self.bg_image = pygame.transform.scale(self.bg_image, (1200,800)).convert()
        pygame.display.set_caption("PyInvaders")
        pygame.display.set_icon(pygame.image.load('images/ship.png'))

        self.gameStats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.play_button = Button(self, "Play")

        self.create_fleet()

        self.bg_colour = self.settings.bg_colour
    def run_game(self):
        while True:
            self.screen.blit(self.bg_image,(0,0))
            self.check_events()
            if self.gameStats.game_active:
                self.update_aliens()
                self.bullets.update()
                self.ship.update()
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
            self.update_screen()

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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_presses = pygame.mouse.get_pressed()
                    if mouse_presses[0]:
                        mouse_pos = pygame.mouse.get_pos()
                        fire_check = self.check_play_button(mouse_pos)
                        if not fire_check:
                            self._fire_bullet()
    def update_screen(self):
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        self.aliens.draw(self.screen)
        if not self.gameStats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()
    
    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet) 
    def create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        avalible_space_x = self.settings.screen_width - (2 * alien_width)
        number_of_aliens_x = avalible_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        avalible_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)

        number_rows = avalible_space_y // (2 * alien_height)
        for row in range(number_rows):
            for alien_number in range(number_of_aliens_x):
                self.create_alien(alien_number, row)
    def create_alien(self, alien_number, row):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row
        self.aliens.add(alien)
    def update_aliens(self):
        self.check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.ship_hit()
        self.check_aliens_bottom()
        
    def check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def ship_hit(self):
        if self.gameStats.ships_left > 0:
            self.gameStats.ships_left -= 1
        else:
            self.gameStats.game_active = False
            pygame.mouse.set_visible(True)

        self.aliens.empty()
        self.bullets.empty()

        self.create_fleet()
        self.ship.center_ship()

        sleep(0.5)

    def check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom > screen_rect.bottom:
                self.ship_hit()
                break
    def check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.gameStats.game_active:
            self.gameStats.reset_stats()
            self.gameStats.game_active = True
            self.aliens.empty()
            self.bullets.empty()
            self.create_fleet()
            self.ship.center_ship()
            return True
        pygame.mouse.set_visible(False)
        return False
        
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()