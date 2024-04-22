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

#Load images:
backgrnd_img = pygame.image.load('img/bg.png')
grnd_img = pygame.image.load('img/ground.png')

###############################################
#classes:
class Bird(pygame.sprite.Sprite): #Bird class for all bird images and methods.
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images= [] #List of bird pics.
        self.index = 0 #Refers back to list and tells which pic. should be shown at particular time.
        self.counter = 0 #Speed at which image changes.
        for num in range(1, 4): #Loop through images in image list.
            img = pygame.image.load(f'img/bird{num}.png')
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
###############################################

bird_group = pygame.sprite.Group() #Keeps track of all sprites given to it.

flappy = Bird(100, int(screen_height / 2))

bird_group.add(flappy) #Adding sprites to group.

run = True
while run:

    clock.tick(fps)

    #Draw background:
    screen.blit(backgrnd_img, (0, 0))

    bird_group.draw(screen) #Add bird sprites to screen.
    bird_group.update()

    #Draw the ground:
    screen.blit(grnd_img, (grnd_scroll, 768))

    #Check if bird has hit the ground:
    if flappy.rect.bottom > 768:
        game_over = True
        flying = False

    if game_over == False:
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

