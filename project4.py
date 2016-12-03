import pygame
import random 

WIDTH = 480
HEIGHT = 680
game_speed = 40


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
    
    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0: 
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullet_group.add(bullet)


class Objects(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = object_img
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(2, 15)
        self.speedx = random.randrange(-3, 3)
    
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


player_img = pygame.image.load('/Users/samaragould/Desktop/206/Project4/images/player.bmp')
bullet_img = pygame.image.load('/Users/samaragould/Desktop/206/Project4/images/ball.bmp')
object_img = pygame.image.load('/Users/samaragould/Desktop/206/Project4/images/object.bmp')
background_img = pygame.image.load('/Users/samaragould/Desktop/206/Project4/images/background.bmp')
background_rect = background_img.get_rect()

all_sprites = pygame.sprite.Group()
object_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
player  = Player()
all_sprites.add(player)

for i in range(8):
    n = Objects()
    all_sprites.add(n)
    object_group.add(n)



score = 0

play = True 

while play: 
    clock.tick(game_speed)
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            play = False   
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
            
	



    all_sprites.update()

    hits = pygame.sprite.groupcollide(object_group, bullet_group, True, True)
    for hit in hits:
        score += len(hits)
        sound = pygame.mixer.Sound('alert.wav')
        sound.play()
        print ("Score: %s" % score)
        n = Objects()
        all_sprites.add(n)
        object_group.add(n)



    hits = pygame.sprite.spritecollide(player, object_group, False)
    if hits:
        print ('Final Score: ', score)
        print ('Game Over :(')
        play = False



    screen.fill((0, 0, 0))
    screen.blit(background_img, background_rect)

    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
