

import pygame
import pygame.mixer_music
from sys import exit
import random

pygame.init()
clock = pygame.time.Clock()

# Window
win_height = 720
win_width = 551
window = pygame.display.set_mode((win_width, win_height))

#Images and loaded assets(More to add)
bird_images = [pygame.image.load("assets/bird_down.png"),
               pygame.image.load("assets/bird_mid.png"),
               pygame.image.load("assets/bird_up.png")]
skyline_image = pygame.image.load("assets/background.png")
ground_image = pygame.image.load("assets/ground.png")
top_pipe_image = pygame.image.load("assets/pipe_top.png")
bottom_pipe_image = pygame.image.load("assets/pipe_bottom.png")
game_over_image = pygame.image.load("assets/game_over.png")
start_image = pygame.image.load("assets/start.png")
turkey_flap_image = pygame.image.load("assets/turkey_flap.png")

#Game Variables
scrolling_speed=1
bird_start=(100,250)
score=0
font=pygame.font.SysFont('Segoe',26)
game_stop = True

pygame.mixer.music.load("assets/background_music.mp3")

flap_sound = pygame.mixer.Sound("assets/flap_sound.mp3")
game_over_sound = pygame.mixer.Sound("assets/crash.mp3")

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = bird_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = bird_start
        self.image_index=0
        self.vel=0
        self.flap=False
        self.alive=True

    def update (self, user_input):
        #animation bird
        if self.alive:
            self.image_index += 1
        if self.image_index >= 30:
            self.image_index = 0
        self.image = bird_images[self.image_index // 10]

        #Gravity
        self.vel += 0.5
        if self.vel > 7:
            self.vel=7
        if self.rect. y < 500:
            self.rect.y += int(self.vel)
        if self.vel == 0:
            self.flap = False

        #bird rotation
        self.image=pygame.transform.rotate(self.image, self. vel * -7)

        #user inputs
        if user_input[pygame.K_SPACE] and not self.flap and self.rect.y > 0 and self.alive:
            self.flap= True
            self.vel = -7
            flap_sound.play()


#pipe setup
class Pipe (pygame.sprite.Sprite):
    def __init__(self, x, y, image, pipe_type):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x,y
        self.enter, self.exit, self.passed = False, False, False
        self.pipe_type = pipe_type

    def update(self):
        self.rect.x -= scrolling_speed
        if self.rect.x <= -win_width:
            self.kill()

        #score
        global score
        if self.pipe_type == 'bottom':
            if bird_start[0] > self.rect.topleft[0] and not self.passed:
                self.enter = True
                if bird_start[0] > self.rect.topright[0] and not self.passed:
                    self.exit = True
                if self.enter and self.exit and not self.passed:
                    self.passed = True
                    score += 1

#ground setup
class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = ground_image
        self.rect=self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):
        #moving ground
        self.rect.x -=scrolling_speed
        if self.rect.x <= -win_width:
            self.kill()



def quitgame():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

def main():

    global score


    #initalize bird
    bird=pygame.sprite.GroupSingle()
    bird.add(Bird())

    #pipes
    pipe_timer = 0
    pipes = pygame.sprite.Group()


    #Initalize ground
    x_pos_ground, y_pos_ground = 0,520
    ground = pygame.sprite.Group()
    ground.add(Ground (x_pos_ground, y_pos_ground))

    pygame.mixer.music.play(-1)


    run=True
    while run:
        #Quit
        quitgame()
        #Frame reset
        window.fill((0,0,0))

        #user input
        user_input=pygame.key.get_pressed()

        #Backround set (background name)
        window.blit(skyline_image,(0,0))


        #continually spawning ground
        if len(ground) <=2:
            ground.add(Ground(win_width, y_pos_ground))

        #Drawing pipes ground and bird
        pipes.draw(window)
        ground.draw(window)
        bird.draw(window)

        #showing score
        score_text = font.render('Score: ' +str(score), True, pygame.Color(255, 255, 255))
        window.blit(score_text, (20,20))


        #Updating elements
        if bird.sprite.alive:
            pipes.update()
            ground.update()
        bird.update(user_input)

        #Collision stuff
        collision_pipes = pygame.sprite.spritecollide(bird.sprites()[0], pipes, False)
        collision_ground= pygame.sprite.spritecollide(bird.sprites()[0], ground, False)
        if collision_ground or collision_pipes:
            bird.sprite.alive = False

            if collision_ground:
                window.blit(game_over_image, (win_width // 2 - game_over_image.get_width() // 2, win_height //2 - game_over_image.get_height() // 2))

                pygame.mixer.music.stop()
                game_over_sound.play()
                if user_input[pygame.K_r]:
                    score = 0
                    pygame.mixer.music.play(-1)
                    break

        #spawning pipes
        if pipe_timer <= 0 and bird.sprite.alive:
            x_top, x_bottom= 550,550
            y_top = random.randint(-600,-480)
            y_bottom= y_top + random.randint (90,130) + bottom_pipe_image.get_height()
            pipes.add(Pipe(x_top, y_top, top_pipe_image, 'top'))
            pipes.add(Pipe(x_bottom, y_bottom, bottom_pipe_image, 'bottom'))
            pipe_timer = random.randint (180,250)
        pipe_timer -= 1



        ground.update()
        clock.tick(60)
        pygame.display.update()

#Menu
def menu():
    global game_stop

    while game_stop:
        quitgame()

        #draw Menu
        window.fill((0,0,0))
        window.blit(skyline_image, (0,0))
        window.blit(ground_image, Ground (0,520))
        window.blit(bird_images[0], (100, 250))
        window.blit(start_image, (win_width // 2 - start_image.get_width() // 2,
                                  win_height // 2 - start_image.get_height() // 2))

        #Uinput
        user_input = pygame.key.get_pressed()
        if user_input[pygame.K_SPACE]:
            main()
        pygame.display.update()
menu()



