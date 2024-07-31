import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy(ish) Bird')

#Define game vars.
grnd_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_freq = 1500 #miliseconds
last_pipe = pygame.time.get_ticks() - pipe_freq


#Load images:
backgrnd_img = pygame.image.load('Flappyish_bird/img/bg.png')
grnd_img = pygame.image.load('Flappyish_bird/img/ground.png')

###############################################
#classes:
class Bird(pygame.sprite.Sprite): #Bird class for all bird images and methods.
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images= [] #List of bird pics.
        self.index = 0 #Refers back to list and tells which pic. should be shown at particular time.
        self.counter = 0 #Speed at which image changes.
        for num in range(1, 4): #Loop through images in image list.
            img = pygame.image.load(f'Flappyish_bird/img/bird{num}.png')
            self.images.append(img) #Add loaded image to list.

        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self): #Overwrite update function in Sprite.

        if flying: # If game is started
            #Handle movement:
            #Gravity:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8

            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        if game_over == False:
            #Jumping:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            
            #Handle animation:
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1

                if self.index >= len(self.images):
                    self.index = 0
                    
            self.image = self.images[self.index]

            #Rotate the bird:
            self.image = pygame.transform.rotate(self.images[self.index], (self.vel * -2))
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)   

class Pipe(pygame.sprite.Sprite): 
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Flappyish_bird/img/pipe.png')
        self.rect = self.image.get_rect()

        #Position 1 is from top, -1 is from bottom:
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap/2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap/2)]
    
    def update(self):
        self.rect.x -+ scroll_speed



###############################################


bird_group = pygame.sprite.Group() #Keeps track of all sprites given to it.
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy) #Add sprites to group.


run = True
while run:

    clock.tick(fps)

    #Draw background:
    screen.blit(backgrnd_img, (0, 0))

    bird_group.draw(screen) #Add bird sprites to screen.
    bird_group.update()

    pipe_group.draw(screen) #Add pipes to screen.
    pipe_group.update()

    #Draw the ground:
    screen.blit(grnd_img, (grnd_scroll, 768))

    #Check if bird has hit the ground:
    if flappy.rect.bottom > 768:
        game_over = True
        flying = False

    if game_over == False:
        #Generate new pipes:
        time_now = pygame.time.get_ticks()
        if(time_now - last_pipe) > pipe_freq:
            top_pipe = Pipe(screen_width, int(screen_height / 2), 1)
            btm_pipe = Pipe(screen_width, int(screen_height / 2), -1)
            pipe_group.add(btm_pipe) #Add pipes to group.
            pipe_group.add(top_pipe)
            last_pipe = time_now

        #Scroll ground:
        grnd_scroll -= scroll_speed

        if abs(grnd_scroll) > 35:
            grnd_scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if (event.type == pygame.MOUSEBUTTONDOWN) and (flying == False) and (game_over == False):
            flying = True

    pygame.display.update()

pygame.quit()

