import pygame
from pygame.locals import *
import sys
import os


window_width, window_height = 640, 480
ball_width, ball_height = 20, 20
brick_width, brick_height = 64, 16
player_width, player_height = 64, 16
player_speed = 20
ball_speed = 2

class Initial_Sprite(pygame.sprite.Sprite):

    def __init__(self, image_file):
        pygame.sprite.Sprite.__init__(self)

    
        self.image = pygame.image.load('/Users/samaragould/Desktop/206/Project4/images/ball.bmp')
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()

class Player(Initial_Sprite):

    def __init__(self, image_file):
        Initial_Sprite.__init__(self, image_file)
        self.image = pygame.image.load('/Users/samaragould/Desktop/206/Project4/images/player.bmp')
        self.rect.bottom = window_height
        self.rect.left = (window_width - self.image.get_width()) / 2

    def move_left(self):
        if self.rect.left > 0:
            self.rect.move_ip(-player_speed, 0)

    def move_right(self):
        if self.rect.right < window_width:
            self.rect.move_ip(player_speed, 0)

class Brick(Initial_Sprite):
  
    def __init__(self, image_file, x, y):
        Initial_Sprite.__init__(self, image_file)
        self.image = pygame.image.load('/Users/samaragould/Desktop/206/Project4/images/brick.bmp')
        self.rect.x, self.rect.y = x, y

class Ball(Initial_Sprite):

    def __init__(self, image_file, speed_x, speed_y):
        Initial_Sprite.__init__(self, image_file)
        self.rect.bottom = window_height - player_height
        self.image = pygame.image.load('/Users/samaragould/Desktop/206/Project4/images/ball.bmp')
        self.rect.left = window_width / 2
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self):
        self.rect = self.rect.move(self.speed_x, self.speed_y)

        if self.rect.x > window_width - self.image.get_width() or self.rect.x < 0:
            self.speed_x *= -1
        if self.rect.y < 0:
            self.speed_y *= -1


pygame.init()
window = pygame.display.set_mode((window_width, window_height))
pygame.key.set_repeat(400, 30)
clock = pygame.time.Clock()
score = 0




all_sprites_group = pygame.sprite.Group()

player_bricks_group = pygame.sprite.Group()
bricks_group = pygame.sprite.Group()

player_ball_group = pygame.sprite.Group()


ball = Ball('ball.png', ball_speed, -ball_speed)
all_sprites_group.add(ball)

player_ball_group.add(ball)

player = Player('player.bmp')
all_sprites_group.add(player)
player_bricks_group.add(player)

player_ball_group.add(player)




for i in range(8):
    for j in range(8):
        brick = Brick('brick.bmp', (i+1)*brick_width + 5, (j+3)*brick_height + 5)
        all_sprites_group.add(brick)
        bricks_group.add(brick)
        player_bricks_group.add(brick)


while True:

    if ball.rect.y > window_height:
        print ('Game Over')
        pygame.quit()
        sys.exit()

 
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                player.move_left()
            elif event.key == K_RIGHT:
                player.move_right()

    
    hits = pygame.sprite.spritecollide(ball, player_bricks_group, False)
    

    
    if hits:
        hit_rect = hits[0].rect

        if hit_rect.left > ball.rect.left or ball.rect.right < hit_rect.right:
            ball.speed_y *= -1
        else:
            ball.speed_x *= -1

        if pygame.sprite.spritecollide(ball, bricks_group, True):
            score += len(hits)
            sound = pygame.mixer.Sound('alert.wav')
            sound.play()
            print ("Score: %s" % score)


    window.fill((0, 0, 0))
    all_sprites_group.draw(window)

    
    all_sprites_group.update()
    player_hits = pygame.sprite.spritecollide(ball, all_sprites_group, True)
    if player_hits:
        player_hit_rect = player_hits[0].rect
        if player_hit_rect.left > ball.rect.left or ball.rect.right < player_hit_rect.right:
            ball.speed_y *= 1
        else:
            ball.speed_x *= 1

    clock.tick(60)
    pygame.display.flip()
