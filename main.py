import pygame 
from random import randint

HEIGHT = 700
WIDTH = 1200
FPS = 60


SIZE = (WIDTH,HEIGHT)

lost = 0
score = 0
monsters_num = 5
healths = 3




window = pygame.display.set_mode(SIZE)

clock = pygame.time.Clock()

background = pygame.transform.scale(
    pygame.image.load("galaxy.jpg"),
    SIZE)
pygame.mixer.init()
pygame.mixer.music.load("space.ogg")
pygame.mixer.music.play()

fire_sfx = pygame.mixer.Sound("fire.ogg")

pygame.font.init()
font_big = pygame.font.Font(None,70)
font_medium = pygame.font.Font(None,35)
font_small = pygame.font.Font(None,15)

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image ,coords: tuple, speed, size):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image),
        size)
        self.rect = self.image.get_rect()
        self.rect.center = coords
        self.speed = speed

    def reset(self):
        window.blit(self.image, self.rect.topleft)


class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            if self.rect.x < WIDTH:
                self.rect.x += self.speed
            else:
                self.rect.x = 0
        if keys[pygame.K_a]:
            if self.rect.x > 0:
                self.rect.x -= self.speed
            else:
                self.rect.x = WIDTH
    
    def fire(self):
            new_bullet = Bullet("bullet.png",(self.rect.centerx, self.rect.top),5 , (5,10))

            bullets.add(new_bullet)
            fire_sfx.play()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom >= HEIGHT:
            self.rect.y = 0
            global lost
            lost += 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom <= 0:
            self.kill()





player = Player("rocket.png", (WIDTH/2,HEIGHT-50),7,(75,100))

monsters = pygame.sprite.Group()



for i in range(monsters_num):
    new_enemy = Enemy("ufo.png",(randint(50,WIDTH-50),0),4,(75,50))
    monsters.add(new_enemy)

bullets = pygame.sprite.Group()





game = True
finish = False
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.fire()
    if not finish:
        window.blit(background,(0,0))
        player.reset()
        player.update()
        
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)


        text_lost = font_medium.render("Пропущено:" + str(lost),True, (255,255,255))
        text_score = font_medium.render("Рахунок: " + str(score),True, (255,255,255))
        text_healths = font_medium.render("ХП: " + str(healths),True, (255,255,255))


        window.blit(text_score,(0,0))
        window.blit(text_lost,(0,40))
        window.blit(text_healths,(0,80))

        shot_monsters = pygame.sprite.groupcollide(monsters,bullets,True,True)
        for i in shot_monsters:
            new_enemy = Enemy("ufo.png",(randint(50,WIDTH-50),0),randint(2,8),(75,50))
            monsters.add(new_enemy)
            score += 1

        
        collisions = pygame.sprite.spritecollide(player,monsters, True)
        for c in collisions:
            healths -= 1
            new_enemy = Enemy("ufo.png",(randint(50,WIDTH-50),0),randint(2,8),(75,50))
            monsters.add(new_enemy)
            









        if score >= 10:
            finish = True
            monsters.empty()

            text_win = font_big.render("Ти переміг", True,(200,0,100))
            window.blit(text_win, (WIDTH/2-50,HEIGHT/2))

        if lost >= 10 or healths <= 0:
            finish = True
            monsters.empty()
            
            text_lose = font_big.render("Ти програв", True,(200,0,100))
            window.blit(text_lose, (WIDTH/2-50,HEIGHT/2))







        
    pygame.display.update()
    clock.tick(FPS)
