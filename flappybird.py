#Dean Church
#FLappybird

import pygame 
from pygame.locals import *  
import sys
import random
from os import path
vec = pygame.math.Vector2

WHITE = (255, 255, 255)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE
PLAYER_GRAV = 0.8
BLACK = (0, 0, 0)
WIDTH = 400
HEIGHT = 700
FONT_NAME = 'arial'
HS_FILE = "highscore.txt"
TITLE = "Flappybird"
FPS = 60

class FlappyBird:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.bird = pygame.Rect(65, 50, 50, 50)
        self.font_name = pygame.font.match_font(FONT_NAME)
        self.highscore = HS_FILE
        self.load_data()
        self.pos = vec(40, HEIGHT - 100)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.gap = 130
        self.wallx = 400
        self.birdY = 350
        self.jump = 0
        self.jumpSpeed = 10
        self.gravity = 5
        self.dead = False
        self.sprite = 0
        self.counter = 0
        self.offset = random.randint(-110, 110)
        self.load_data()
        self.running = True
        self.clock = pygame.time.Clock()


    def load_data(self):
        self.background = pygame.image.load("images/background.png").convert()
        self.birdSprites = [pygame.image.load("images/1.png").convert_alpha(),
                            pygame.image.load("images/2.png").convert_alpha(),
                            pygame.image.load("images/dead.png")]
        self.wallUp = pygame.image.load("images/bottom.png").convert_alpha()
        self.wallDown = pygame.image.load("images/top.png").convert_alpha()
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        self.snd_dir = path.join(self.dir, 'snd')
        self.jump_sound = pygame.mixer.Sound(path.join(self.snd_dir, 'Jump33.wav'))
        self.boost_sound = pygame.mixer.Sound(path.join(self.snd_dir, 'Powerup15.wav'))


    def updateWalls(self):
        self.wallx -= 2
        if self.wallx < -80:
            self.wallx = 400
            self.counter += 1
            self.offset = random.randint(-110, 110)     

    def birdUpdate(self):
        if self.jump:
            self.jumpSpeed -= 1
            self.birdY -= self.jumpSpeed
            self.jump -= 1
            #self.jump_sound.play()
        else:
            self.birdY += self.gravity
            self.gravity += 0.2
        self.bird[1] = self.birdY
        upRect = pygame.Rect(self.wallx,
                             360 + self.gap - self.offset + 10,
                             self.wallUp.get_width() - 10,
                             self.wallUp.get_height())
        downRect = pygame.Rect(self.wallx,
                               0 - self.gap - self.offset - 10,
                               self.wallDown.get_width() - 10,
                               self.wallDown.get_height())
        if upRect.colliderect(self.bird):
            self.dead = True
        if downRect.colliderect(self.bird):
            self.dead = True
        if not 0 < self.bird[1] < 720:            
            self.bird[1] = 50
            self.birdY = 50
            self.dead = False
            self.counter = 0
            self.wallx = 400
            self.offset = random.randint(-110, 110)
            self.gravity = 5



        
    def run(self):
        clock = pygame.time.Clock()
        pygame.font.init()
        font = pygame.font.SysFont("Arial", 50)
        self.start_screen()
        pygame.mixer.music.load(path.join(self.snd_dir, 'themesong.ogg'))
        pygame.mixer.music.play(loops=-1)
        while True:
            clock.tick(60)    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not self.dead:
                    self.jump = 17
                    self.gravity = 5
                    self.jumpSpeed = 10

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.wallUp,
                             (self.wallx, 360 + self.gap - self.offset))
            self.screen.blit(self.wallDown,
                             (self.wallx, 0 - self.gap - self.offset))
            self.screen.blit(font.render(str(self.counter),
                                         -1,
                                         (255, 255, 255)),
                             (200, 50))
            if self.dead:
                self.sprite = 2
                clock.tick(60)
            elif self.jump:
                self.sprite = 1
            self.screen.blit(self.birdSprites[self.sprite], (70, self.birdY))
            if not self.dead: 
                self.sprite = 0
            self.updateWalls()
            self.birdUpdate()
            pygame.display.update()
        pygame.mixer.music.fadeout(500)
        


    def start_screen(self):
        self.screen.fill(BGCOLOR)
        pygame.mixer.music.load(path.join(self.snd_dir, 'Yippee.ogg'))
        pygame.mixer.music.play(loops=-1)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Space to jump", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        pygame.display.flip()
        pygame.mixer.music.fadeout(500)
        self.wait_for_key()

    def end_screen(self):
        #self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.counter), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press keys until the bird is at the bottom", 22, BLACK, WIDTH / 2, HEIGHT * 3 / 4)
        if self.counter > self.highscore:
            self.highscore = self.counter
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.counter))
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        self.wait_for_key()


    def wait_for_key(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False


    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


##class Pipes(pg.sprite.Sprite):
##    def __init__(self, game, x, y):
##        pg.sprite.Sprite.__init__(self, self.groups)
##        self.game = game
##        images = [self.game.spritesheet.get_image(0, 288, 380, 94),
##                  self.game.spritesheet.get_image(213, 1662, 201, 100)]
##        self.image = choice(images)
##        self.image.set_colorkey(BLACK)
##        self.rect = self.image.get_rect()
##        self.rect.x = x
##        self.rect.y = y
##        if randrange(100) < POW_SPAWN_PCT:
##            Pow(self.game, self)


        

if __name__ == "__main__":
    FlappyBird().run()



        
    
