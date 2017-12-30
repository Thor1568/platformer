import pygame
import os

pygame.init()
pygame.mixer.init()

FPS = 60
width = 800
height = 600
gameDisp = pygame.display.set_mode((width, height), pygame.FULLSCREEN, 32)

#Basic colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#functions/classes
class player(pygame.sprite.Sprite):
    def __init__(self, img, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img).convert()
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]; self.rect.y = pos[1]

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

class platform(pygame.sprite.Sprite):
    def __init__(self, width, height, color, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img).convert()
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]; self.rect.y = pos[1]

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

class game(pygame.Surface):
    def __init__(self, width, height):
        pygame.Surface.__init__(self, size=(width, height))

    def level(self, number):
        if number == 0:
            #Make level 0 or the tutorial
            pass
        if number == 1:
            pass

    def render(self, display):
        display.blit(self, (0,0))


#Intro loop
intro = True
while intro:
    pass

#Menu loop
menu = True
inst = False
sett = False
while menu:
    pass

#game loop
play = True
while play:
    pass
