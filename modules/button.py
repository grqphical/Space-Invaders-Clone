import pygame.font
import pygame

class Button:
    def __init__(self, ai_game, message):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.width, self.height = 200, 50
        self.button_colour = (0,255,0)
        self.text_colour = (255,255,255)
        self.font = pygame.font.SysFont('Helvetica', 48)

        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = self.screen_rect.center

        self.prep(message)
    def prep(self,message):
        self.msg_image = self.font.render(message, True, self.text_colour, self.button_colour)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    def draw_button(self):
        #self.screen.fill(self.button_colour, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)