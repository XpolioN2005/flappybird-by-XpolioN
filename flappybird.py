import pygame
from sys import exit
import random as rnd



pygame.init()

# required vars
screen = pygame.display.set_mode((288,512))
icon_surface = pygame.image.load('favicon.ico')
icon = pygame.display.set_icon(icon_surface)
clock = pygame.time.Clock()
pygame.display.set_caption('FlappyBird by XpolioN')
game_images = {}


# game vars
base_move = 0
base_move_speed = 2.5
started = False
game_over = False
pipe_gap = 120
pipe_fr = 1500 #ms
last_pipe = pygame.time.get_ticks() - pipe_fr
pass_pipe = False
score = 0

#surfs
bg_day_surf = pygame.image.load('assets/sprites/background-day.png')
bg_night_surf = pygame.image.load('assets/sprites/background-night.png')
base_surf = pygame.image.load('assets/sprites/base.png')
base_rect = base_surf.get_rect()

greet = pygame.image.load('assets/sprites/message.png')
greet_rect = greet.get_rect(center = (288/2,512/2))

gameover_img = pygame.image.load('assets/sprites/gameover.png')
gameover_img_rect = gameover_img.get_rect(center = (144,256-100))

restart_btn = pygame.image.load('assets/sprites/restart.png')
restart_btn_rect = restart_btn.get_rect(center = (144,256))

game_images['scoreimages'] = ( 
        pygame.image.load('assets/sprites/0.png').convert_alpha(), 
        pygame.image.load('assets/sprites/1.png').convert_alpha(), 
        pygame.image.load('assets/sprites/2.png').convert_alpha(), 
        pygame.image.load('assets/sprites/3.png').convert_alpha(), 
        pygame.image.load('assets/sprites/4.png').convert_alpha(),         
        pygame.image.load('assets/sprites/5.png').convert_alpha(), 
        pygame.image.load('assets/sprites/6.png').convert_alpha(), 
        pygame.image.load('assets/sprites/7.png').convert_alpha(), 
        pygame.image.load('assets/sprites/8.png').convert_alpha(), 
        pygame.image.load('assets/sprites/9.png').convert_alpha() 
    ) 

# sounds
die_sfx = pygame.mixer.Sound('assets/audio/die.ogg')
hit_sfx = pygame.mixer.Sound('assets/audio/hit.ogg')
point_sfx = pygame.mixer.Sound('assets/audio/point.ogg')
swoosh_sfx = pygame.mixer.Sound('assets/audio/swoosh.ogg')
wing_sfx = pygame.mixer.Sound('assets/audio/wing.ogg')

def restart_game():
    global game_over
    global score
    global started
    pos = pygame.mouse.get_pos()
    if restart_btn_rect.collidepoint(pos):
        if pygame.mouse.get_pressed()[0] == 1:
            pipe_group.empty()
            started = False
            game_over = False
            score = 0
            bird.rect.x = 50
            bird.rect.y = 256





class player(pygame.sprite.Sprite):
    def __init__(self, x , y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1,4):
            img = pygame.image.load(f'assets/sprites/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.velocity = 0
        self.click = False
    
    def update(self):
        if started == True:
            # gravity
            self.velocity += 0.15
            if self.rect.bottom <= 420:
                self.rect.y += int(self.velocity)
            else:
                self.velocity = 0
        if game_over == False:        
            # player input
            if (pygame.mouse.get_pressed()[0] == 1 and self.click == False):
                self.click = True
                pygame.mixer.Sound.play(swoosh_sfx)
                pygame.mixer.Sound.play(wing_sfx)
                self.velocity = -5
            elif pygame.mouse.get_pressed()[0] == 0 and not pygame.key.get_pressed()[pygame.K_SPACE]:
                self.click = False
            if pygame.key.get_pressed()[pygame.K_SPACE] and self.click == False:
                self.click = True
                pygame.mixer.Sound.play(wing_sfx)
                pygame.mixer.Sound.play(swoosh_sfx)
                self.velocity = -5



            # animation
            self.counter += 1
            ani_cd = 8
            if self.counter > ani_cd and self.rect.bottom <= 420:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
                self.image = self.images[self.index]
                # rotate
                self.image = pygame.transform.rotate(self.images[self.index], self.velocity*-3)
        else:
            self.image = pygame.transform.rotate(self.images[self.index],-90)

class pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/sprites/pipe-green.png')
        self.rect = self.image.get_rect()
        if pos == -1:  # -1 = from bottom & 1 = from top
            self.rect.topleft = [x,(y+ int(pipe_gap /2))]
        if pos == 1:
            self.image = pygame.transform.flip(self.image , False,True)
            self.rect.bottomleft = [x,(y- int(pipe_gap /2))]
    def update(self):
        if game_over == False:
            self.rect.x -= base_move_speed
        if self.rect.right <0:
            self.kill()


player_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

bird = player(50,256)
player_group.add(bird)


# gameloop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN and started == False and game_over == False:
            started = True

    screen.blit(bg_day_surf,(0,0))

    if len(pipe_group)>0:
        if player_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and player_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
                pass_pipe = True
        if pass_pipe == True:
            if player_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pygame.mixer.Sound.play(point_sfx)
                pass_pipe = False

    if game_over == False:
        if pygame.sprite.groupcollide(player_group,pipe_group,False,False) or bird.rect.top <0\
            or bird.rect.bottom >= 420:
            pygame.mixer.Sound.play(hit_sfx)
            pygame.mixer.Sound.play(die_sfx)
            game_over = True
            


    if game_over == False and started == True:
        #gen pipe
        time_now = pygame.time.get_ticks()
        if time_now-last_pipe > pipe_fr:
            pipe_h = rnd.randint(-70,70)
            btm_pipe = pipe(290,256 + pipe_h, -1)
            top_pipe = pipe(290,256 + pipe_h, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe =time_now
        base_move -= base_move_speed
        if abs(base_move)> 48:
            base_move = 0


    pipe_group.draw(screen)
    pipe_group.update()

    screen.blit(base_surf, (base_move, 420))

    if started == True:
        player_group.draw(screen)
        player_group.update() 
            
        # Fetching the digits of score. 
        numbers = [int(x) for x in list(str(score))] 
        width = 0
            
        # finding the width of score images from numbers. 
        for num in numbers: 
            width += game_images['scoreimages'][num].get_width() 
        Xoffset = (288 - width)/1.1
            
        # Blitting the images on the window. 
        for num in numbers: 
            screen.blit(game_images['scoreimages'][num], (Xoffset, 288*0.02)) 
            Xoffset += game_images['scoreimages'][num].get_width() 

                    

    elif started == False and game_over == False:
        screen.blit(greet,greet_rect)

    if game_over == True:
        screen.blit(gameover_img,gameover_img_rect)
        screen.blit(restart_btn,restart_btn_rect)
        restart_game()


    pygame.display.update()
    clock.tick(60)