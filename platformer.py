import pygame
import os
from time import sleep

pygame.init()
pygame.mixer.init()

#Note to self:
#All fonts are Century gothic and antialiased

#Constant stuff
pygame.mouse.set_visible(False)
dev_mode = False
FPS = 60
WIDTH = 800
HEIGHT = 600
CTL_MODE = 0
BASE_SAVE = """Pygame Platformer save file
level = 0"""
if dev_mode == False:
    gameDisp = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN, 32)
    full_screen = True
else:
    gameDisp = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    full_screen = False
    play = True
    exit = False
pygame.display.set_caption("Platformer game")
g_dir = os.path.dirname(__file__)
img_dir = os.path.join(g_dir, "images")
g_icon = pygame.image.load(os.path.join(img_dir, "icon.png"))
pygame.display.set_icon(g_icon)
pygame.mouse.set_cursor(*pygame.cursors.tri_left)
g_clock = pygame.time.Clock()
save_file = open(os.path.join(g_dir, "save.txt"), "r+")
file_info = save_file.read()
if len(file_info) > 0:
    #do not write to save file and take info to use when launching game
    pass
else:
    save_file.write(BASE_SAVE)
save_file.close()

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
        self.font_ui = pygame.font.SysFont(None, 36)
        self.time = 0

    def level(self, number):
        self.time = 0
        self.plats = pygame.sprite.Group()
        self.all_stuff = pygame.sprite.Group()
        self.goal = pygame.sprite.Group()
        self.cube = player(os.path.join(img_dir, "player.png"),
            ((spawns[my_level])[0],
            (spawns[my_level])[1]))
        #UI text

        self.text_surf2 = self.font_ui.render("Time: %s" % self.time, True, WHITE)

        if number == 0:
            self.text_surf1 = self.font_ui.render("Level: 1-1", True, WHITE)
            #Level tutorial
            #platform(width, height, color, (x, y))
            floor = platform(800, 25, BLACK, (0, 575))
            wall1 = platform(10, 600, BLACK, (-10, 0))
            wall2 = platform(10, 600, BLACK, (800, 0))
            ceiling = platform(800, 10, BLACK, (0, -10))
            plat1 = player(os.path.join(img_dir, "75x25_plat.png"), (200, 450))
            plat3 = player(os.path.join(img_dir, "75x25_plat.png"), (375, 400))
            plat4 = player(os.path.join(img_dir, "75x25_plat.png"), (525, 300))

            #Special objects
            level_goal = player(os.path.join(img_dir, "goal.png"),
                ((goals[my_level])[0],
                (goals[my_level])[1]))


            self.plats.add(floor, plat1, plat3, plat4, ceiling, wall1, wall2)

        if number == 1:
            self.text_surf1 = self.font_ui.render("Level: 1-2", True, WHITE)
            #Create platforms
            floor = platform(800, 25, BLACK, (0, 575))
            wall1 = platform(10, 600, BLACK, (-10, 0))
            wall2 = platform(10, 600, BLACK, (800, 0))
            ceiling = platform(800, 10, BLACK, (0, -10))
            plat1 = player(os.path.join(img_dir, "725x25_plat.png"), (0, 435))
            plat2 = player(os.path.join(img_dir, "725x25_plat.png"), (75, 300))
            plat3 = player(os.path.join(img_dir, "75x25_plat.png"), (325, 165))
            plat4 = player(os.path.join(img_dir, "75x25_plat.png"), (725, 150))

            #End goal
            level_goal = player(os.path.join(img_dir, "goal.png"),
                ((goals[my_level])[0],
                (goals[my_level])[1]))

            #Groups

            self.plats.add(floor, ceiling, wall1, wall2, plat1, plat2, plat3, plat4)

        self.goal.add(level_goal)
        self.all_stuff.add(self.plats, self.cube, self.goal)
        self.text_to_blit = [self.text_surf1, self.text_surf2]

    def render(self, display):
        self.text_surf2 = self.font_ui.render("Time: %s" % self.time, True, WHITE)
        self.text_to_blit[1] = self.text_surf2
        self.fill(SKYBLUE)
        self.all_stuff.draw(self)
        temp = 0
        for text in self.text_to_blit:
            self.blit(text, (10, 10+temp))
            temp += 30
        display.blit(self, (0,0))

    def return_plats(self):
        return self.plats

    def tick_timer(self):
        self.time += 1

#Images for intro animation
py_logo = pygame.image.load(os.path.join(img_dir, "pygame_powered_big.png")).convert()
my_logo = pygame.image.load(os.path.join(img_dir, "my_logo.png")).convert()

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
    menu = True
    inst = False
    menu_pic = pygame.image.load(os.path.join(img_dir, "game_logo.png")).convert()
    alpha = 0
    button1 = pygame.image.load(os.path.join(img_dir, "play_button.png")).convert()
    button2 = pygame.image.load(os.path.join(img_dir, "help_button.png")).convert()
    wasd_button_off_off = pygame.image.load(os.path.join(img_dir, "wasd_button.png")).convert()
    wasd_button_off_on = pygame.image.load(os.path.join(img_dir, "wasd_button2.png")).convert()
    arrow_button_off_off = pygame.image.load(os.path.join(img_dir, "arrow_button.png")).convert()
    arrow_button_off_on = pygame.image.load(os.path.join(img_dir, "arrow_button2.png")).convert()
    control_banner = pygame.image.load(os.path.join(img_dir, "control_banner.png")).convert()
    fullsc_banner = pygame.image.load(os.path.join(img_dir, "fullsc_banner.png")).convert()
    fulsc_on_off = pygame.image.load(os.path.join(img_dir, "fullsc_on.png")).convert()
    fulsc_on_on = pygame.image.load(os.path.join(img_dir, "fullsc_on2.png")).convert()
    fulsc_off_off = pygame.image.load(os.path.join(img_dir, "fullsc_off.png")).convert()
    fulsc_off_on = pygame.image.load(os.path.join(img_dir, "fullsc_off2.png")).convert()
    back_button = pygame.image.load(os.path.join(img_dir, "back_button.png")).convert()
    inst_text = pygame.image.load(os.path.join(img_dir, "instructions_text.png")).convert()
    sleep(1)
    #menu art fading in
    for x in range(52):
        gameDisp.fill(BLACK)
        gameDisp.blit(menu_pic, (0,0))
        gameDisp.blit(button1, (200, 200))
        gameDisp.blit(button2, (400, 200))
        menu_pic.set_alpha(alpha)
        button1.set_alpha(alpha)
        button2.set_alpha(alpha)
        pygame.display.flip()
        sleep(0.01)
        alpha += 5
    menu_pic.set_alpha(255)
    pygame.mouse.set_visible(True)
#Menu Loop
    while menu:
        gameDisp.fill(BLACK)
        #Mouse tuple contains: mouse x, mouse y, and if left click is down
        mouse = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], pygame.mouse.get_pressed()[0])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
                play = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit = True
                    menu = False
                    play = False
                    break
        #Button clicking check
        if inst == False:
            if mouse[2] == 1:
                if ((mouse[0] >= 200) and (mouse[0] <= 400)) and ((mouse[1] <= 300) and (mouse[1] >= 200)):
                    play = True
                    menu = False
                    exit = False
                    mouse = (0,0,0)
                if ((mouse[0] >= 400) and (mouse[0] <= 600)) and ((mouse[1] <= 300) and (mouse[1] >= 200)):
                    inst = True
        else:
            if mouse[2] == 1:
                if ((mouse[0] >= 200) and (mouse[0] <= 400)) and ((mouse[1] <= 250) and (mouse[1] >= 200)):
                    #if WASD control on is clicked
                    CTL_MODE = 0
                    mouse = (0,0,0)
                if ((mouse[0] >= 200) and (mouse[0] <= 400)) and ((mouse[1] <= 300) and (mouse[1] >= 250)):
                    #if arrow_key control on is clicked
                    CTL_MODE = 1
                    mouse = (0,0,0)
                if ((mouse[0] >= 400) and (mouse[0] <= 600)) and ((mouse[1] <= 300) and (mouse[1] >= 250)):
                    #if full screen on is clicked
                    if full_screen == False:
                        full_screen = True
                        gameDisp = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN, 32)
                        pygame.display.set_icon(g_icon)
                    mouse = (0,0,0)
                if ((mouse[0] >= 400) and (mouse[0] <= 600)) and ((mouse[1] <= 250) and (mouse[1] >= 200)):
                    #if full screen off on is clicked
                    if full_screen == True:
                        full_screen = False
                        gameDisp = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
                        pygame.display.set_icon(g_icon)
                    mouse = (0,0,0)
                if ((mouse[0] >= 384) and (mouse[0] <= 579)) and ((mouse[1] <= 381) and (mouse[1] >= 331)):
                    inst = False

        #Drawing
        gameDisp.blit(menu_pic, (0,0))
        if inst == False:
            gameDisp.blit(button1, (200, 200))
            gameDisp.blit(button2, (400, 200))
        if inst == True:
            if CTL_MODE == 0:
                gameDisp.blit(wasd_button_off_on, (200, 200))
                gameDisp.blit(arrow_button_off_off, (200, 250))
            else:
                gameDisp.blit(wasd_button_off_off, (200, 200))
                gameDisp.blit(arrow_button_off_on, (200, 250))
            gameDisp.blit(control_banner, (200, 150))
            if full_screen == True:
                gameDisp.blit(fulsc_off_off, (400, 200))
                gameDisp.blit(fulsc_on_on, (400,250))
            else:
                gameDisp.blit(fulsc_off_on, (400, 200))
                gameDisp.blit(fulsc_on_off, (400,250))
            gameDisp.blit(fullsc_banner, (400, 150))
            gameDisp.blit(back_button, (384, 331))
            gameDisp.blit(inst_text, (15, 480))

        pygame.display.flip()
        g_clock.tick(FPS)

pygame.mouse.set_visible(True)
#Variables
jump = False
key_right = False
key_left = False
my_level = 0
gravity = 1
y_pos = 0
x_pos = 0
ch_x = 0
ch_y = 0
jump_speed = 20
move_speed = 0.5
#add spawn x+25 and y-25 to make sure the square goes where it is supposed to and track bottom right corner instead of top left
spawns = {0:(20+25, 575-25),
 1:(20+25, 575-25)}

goals = {0:(562.5-25, 300-50),
 1:(750, 100)}

#objects
g_surf = game(WIDTH, HEIGHT)
g_surf.level(my_level)
#Event number 25 is id
one_second = 25
pygame.time.set_timer(one_second, 1000)

#game loop
while play and (not exit):
    gameDisp.fill(BLACK)
    #Game events/logic
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
            break

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                exit = True
                break
            if CTL_MODE == 0:
                if event.key == pygame.K_w:
                    jump = False
                if event.key == pygame.K_a:
                    key_left = False
                if event.key == pygame.K_d:
                    key_right = False
            if CTL_MODE == 1:
                if event.key == pygame.K_UP:
                    jump = False
                if event.key == pygame.K_LEFT:
                    key_left = False
                if event.key == pygame.K_RIGHT:
                    key_right = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit = True
                break
            if event.key == pygame.K_r:
                g_surf.level(my_level)
            if CTL_MODE == 0:
                if event.key == pygame.K_w:
                    jump = True
                if event.key == pygame.K_a:
                    key_left = True
                if event.key == pygame.K_d:
                    key_right = True
            if CTL_MODE == 1:
                if event.key == pygame.K_UP:
                    jump = True
                if event.key == pygame.K_LEFT:
                    key_left = True
                if event.key == pygame.K_RIGHT:
                    key_right = True
        if event.type == one_second:
            g_surf.tick_timer()

##    if exit == True:
##        play = False
##        break

    if jump == True:
        ch_y -= jump_speed
        jump = False
    if key_right == True:
        ch_x += move_speed
    elif key_left == True:
        ch_x -= move_speed
    else:
        if ch_x > 0:
            ch_x -= move_speed
        if ch_x < 0:
            ch_x += move_speed

    x_pos += ch_x
    y_pos += ch_y

    #Move x position and check for collision
    g_surf.cube.move(ch_x, 0)
    if len(g_surf.cube.if_collide(g_surf.plats, False)) > 0:
        g_surf.cube.move(ch_x*-1, 0)
        ch_x = 0

    #move y position and check for collision
    g_surf.cube.move(0, ch_y)
    if len(g_surf.cube.if_collide(g_surf.plats, False)) > 0:
        g_surf.cube.move(0, ch_y*-1)
        ch_y = 0

    #Double check collisions to prevent going in the side of platforms
    if len(g_surf.cube.if_collide(g_surf.plats, False)) > 0:
        g_surf.cube.move(ch_x*-1, ch_y*-1)
        ch_y = 0
        ch_x = 0

    #Check if collision with the goal
    if len(g_surf.cube.if_collide(g_surf.goal, False)) > 0:
        #Level change animation or whatever
        my_level += 1
        g_surf.level(my_level)

    #Always pulling the square down
    ch_y += gravity

    #Drawing and rendering
    g_surf.render(gameDisp)
    pygame.display.flip()
    g_clock.tick(60)

pygame.quit()
