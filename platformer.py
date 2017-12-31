import pygame
import os
from time import sleep

pygame.init()
pygame.mixer.init()

#Constant stuff
dev_mode = True
FPS = 60
width = 800
height = 600
gameDisp = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption("Platformer game")
g_dir = os.path.dirname(__file__)
g_icon = pygame.image.load(os.path.join(g_dir, "icon.png"))
pygame.display.set_icon(g_icon)
g_clock = pygame.time.Clock()

#Basic colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
SKYBLUE = (153, 191, 252)

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

    def if_collide(self, group, kill):
        return pygame.sprite.spritecollide(self, group, kill)

class platform(pygame.sprite.Sprite):
    def __init__(self, width, height, color, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.color = color
        self.pos = pos
        self.width = width
        self.height = height
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, self.color, (self.pos[0], self.pos[1], self.width, self.height))
        self.rect.x = pos[0]; self.rect.y = pos[1]

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def if_collide(self, group, kill):
        return pygame.sprite.spritecollide(self, group, kill)

    def update(self):
        pygame.draw.rect(self.image, self.color, (self.pos[0], self.pos[1], self.width, self.height))

class game(pygame.Surface):
    def __init__(self, width, height):
        pygame.Surface.__init__(self, size=(width, height))

    def level(self, number):
        self.cube = player(os.path.join(g_dir, "player.png"),
            ((spawns[my_level])[0],
            (spawns[my_level])[1]))
        if number == 0:
            #Level tutorial
            #platform(width, height, color, (x, y))
            floor = platform(800, 25, BLACK, (0, 575))
            plat1 = platform(75, 25, BLACK, (200, 450))
            plat2 = platform(25, 100, BLACK, (300, 475))
            plat3 = platform(75, 25, BLACK, (375, 400))
            plat4 = platform(75, 25, BLACK, (525, 300))
            plat5 = platform(75, 100, BLACK, (200, 475))
            self.plats = pygame.sprite.Group()
            self.all_stuff = pygame.sprite.Group()
            self.plats.add(floor, plat1, plat2, plat3, plat4, plat5)
            self.all_stuff.add(floor, plat1, self.cube, plat2, plat3, plat4, plat5)
        if number == 1:
            pass

    def render(self, display):
        self.fill(SKYBLUE)
        self.all_stuff.update()
        self.all_stuff.draw(self)
        display.blit(self, (0,0))

    def return_plats(self):
        return self.plats

#Images for intro animation
py_logo = pygame.image.load(os.path.join(g_dir, "pygame_powered_big.png")).convert()
my_logo = pygame.image.load(os.path.join(g_dir, "my_logo.png")).convert()

#Intro animation
if dev_mode == False:
    intro = True
    alpha = 0
    gameDisp.fill(BLACK)
    gameDisp.blit(py_logo, (50,150))
    py_logo.set_alpha(alpha)
    pygame.display.flip()
    for x in range(51):
        gameDisp.fill(BLACK)
        gameDisp.blit(py_logo, (50, 150))
        py_logo.set_alpha(alpha)
        pygame.display.flip()
        sleep(0.01)
        alpha += 5

    sleep(2)

    for x in range(52):
        gameDisp.fill(BLACK)
        gameDisp.blit(py_logo, (50,150))
        py_logo.set_alpha(alpha)
        pygame.display.flip()
        sleep(0.01)
        alpha -= 5

    sleep(2)
    alpha = 0
    gameDisp.fill(BLACK)
    gameDisp.blit(my_logo, (180, 100))
    my_logo.set_alpha(alpha)
    pygame.display.flip()

    for x in range(51):
        gameDisp.fill(BLACK)
        gameDisp.blit(my_logo, (180,100))
        my_logo.set_alpha(alpha)
        pygame.display.flip()
        sleep(0.01)
        alpha += 5

    sleep(2)

    for x in range(52):
        gameDisp.fill(BLACK)
        gameDisp.blit(my_logo, (180,100))
        my_logo.set_alpha(alpha)
        pygame.display.flip()
        sleep(0.01)
        alpha -= 5


#Menu loop
menu = False
inst = False
sett = False

while menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
            exit = True


#Variables
play = True
jump = False
key_right = False
key_left = False
my_level = 0
gravity = 2
y_speed = 0
x_speed = 0
spawns = {0:(20+50, 575-50),
 1:(50, 10)}

#objects
g_surf = game(width, height)
g_surf.level(my_level)

#game loop
while play:
    #Game events/logic
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
            break

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                exit = True
                break
            if event.key == pygame.K_w:
                jump = False
            if event.key == pygame.K_a:
                key_left = False
            if event.key == pygame.K_d:
                key_right = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit = True
                break
            if event.key == pygame.K_w:
                jump = True
            if event.key == pygame.K_a:
                key_left = True
            if event.key == pygame.K_d:
                key_right = True
            if event.key == pygame.K_f:
                pygame.display.toggle_fullscreen()


    if exit == True:
        play = False
        break

    #Sprite/group updates
    g_surf.level(my_level)


    if key_right == True:
        x_speed += 5
    if key_left == True:
        x_speed -= 5
    if jump == True:
        y_speed -= 10


    g_surf.cube.move(x_speed, y_speed)
    if len(g_surf.cube.if_collide(g_surf.plats, False)) > 0:
        if key_right == True:
            x_speed -= 5
            g_surf.cube.move(x_speed, y_speed)
        elif key_left == True:
            x_speed += 5
            g_surf.cube.move(x_speed, y_speed)
#    print(("x_pos: "+ str(x_speed)) + (" y_pos: "+ str(y_speed)))


    if y_speed < 0:
        y_speed += gravity
    #Drawing and rendering
    gameDisp.fill(BLACK)
    g_surf.render(gameDisp)
    pygame.display.flip()
    g_clock.tick(60)

pygame.quit()
