#!/usr/bin/env python
import pygame
from pygame.locals import *
import sys
import os


WINDOW_WIDTH, WINDOW_HEIGHT = 640, 480
BALL_WIDTH, BALL_HEIGHT = 20, 20
BRICK_WIDTH, BRICK_HEIGHT = 64, 16
PLAYER_WIDTH, PLAYER_HEIGHT = 64, 16
PLAYER_SPEED = 20
BALL_SPEED = 2

class Initial_Sprite(pygame.sprite.Sprite):

    def __init__(self, image_file):
        pygame.sprite.Sprite.__init__(self)

        # load image & rect#
        self.image = pygame.image.load('/Users/samaragould/Desktop/206/Project4/images/ball.bmp')
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()

class Player(Initial_Sprite):

    def __init__(self, image_file):
        Initial_Sprite.__init__(self, image_file)
        self.image = pygame.image.load('/Users/samaragould/Desktop/206/Project4/images/player.bmp')
        self.rect.bottom = WINDOW_HEIGHT
        self.rect.left = (WINDOW_WIDTH - self.image.get_width()) / 2

    def move_left(self):
        if self.rect.left > 0:
            self.rect.move_ip(-PLAYER_SPEED, 0)

    def move_right(self):
        if self.rect.right < WINDOW_WIDTH:
            self.rect.move_ip(PLAYER_SPEED, 0)

class Brick(Initial_Sprite):
  
    def __init__(self, image_file, x, y):
        Initial_Sprite.__init__(self, image_file)
        self.image = pygame.image.load('/Users/samaragould/Desktop/206/Project4/images/brick.bmp')
        self.rect.x, self.rect.y = x, y

class Ball(Initial_Sprite):

    def __init__(self, image_file, speed_x, speed_y):
        Initial_Sprite.__init__(self, image_file)
        self.rect.bottom = WINDOW_HEIGHT - PLAYER_HEIGHT
        self.image = pygame.image.load('/Users/samaragould/Desktop/206/Project4/images/ball.bmp')
        self.rect.left = WINDOW_WIDTH / 2
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self):
        self.rect = self.rect.move(self.speed_x, self.speed_y)
        #pygame.mixer.Sound.play(crash_sound)

        if self.rect.x > WINDOW_WIDTH - self.image.get_width() or self.rect.x < 0:
            self.speed_x *= -1
        if self.rect.y < 0:
            self.speed_y *= -1

# game init
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.key.set_repeat(400, 30)
clock = pygame.time.Clock()
score = 0


#pygame.mixer.music.load(os.path.join('sounds', 'scoreSound.mp3'))
#music.play()


# groups
all_sprites_group = pygame.sprite.Group()
player_bricks_group = pygame.sprite.Group()
bricks_group = pygame.sprite.Group()

# add sprites to their group
ball = Ball('ball.png', BALL_SPEED, -BALL_SPEED)
all_sprites_group.add(ball)

player = Player('player.bmp')
all_sprites_group.add(player)
player_bricks_group.add(player)

for i in range(8):
    for j in range(8):
        brick = Brick('brick.bmp', (i+1)*BRICK_WIDTH + 5, (j+3)*BRICK_HEIGHT + 5)
        all_sprites_group.add(brick)
        bricks_group.add(brick)
        player_bricks_group.add(brick)

# game loop
while True:
    # game over
    if ball.rect.y > WINDOW_HEIGHT:
        print ('Game Over')
        pygame.quit()
        sys.exit()

    # move player horizontally
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                player.move_left()
            elif event.key == K_RIGHT:
                player.move_right()

    # collision detection (ball bounce against brick & player)
    hits = pygame.sprite.spritecollide(ball, player_bricks_group, False)
    if hits:
        hit_rect = hits[0].rect

        # bounce the ball (according to side collided)
        if hit_rect.left > ball.rect.left or ball.rect.right < hit_rect.right:
            ball.speed_y *= -1
        else:
            ball.speed_x *= -1

        # collision with blocks
        if pygame.sprite.spritecollide(ball, bricks_group, True):
            score += len(hits)
            print ("Score: %s" % score)

    # render groups
    window.fill((0, 0, 0))
    all_sprites_group.draw(window)

    # refresh screen
    all_sprites_group.update()
    clock.tick(60)
    pygame.display.flip()
