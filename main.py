import pygame
#its make us use some systems functionalities
import sys,random

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 600))
    screen.blit(floor_surface, (floor_x_pos+576 , 600))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom =(700, random_pipe_pos - 200))
    return top_pipe,bottom_pipe

def moves_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >=800:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe,pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 600:
         return False
    return True

def rotate_bird(bird):
    rotate_bird = pygame.transform.rotozoom(bird,bird_movement*3,1)
    return rotate_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird,new_bird_rect

def scoreDisplay(game_state):
    if game_state == 'main_game':
        score_surface =game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,60))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 160))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 570))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score,high_score):
    if score > high_score:
        high_score=score
    return high_score

#initialize mixer
pygame.mixer.pre_init(frequency=44100,size=16,channels = 1, buffer=512)
pygame.init()

#after initializing the pygame module we should create the display and store it in a var
#there is one important argument that method need ands its a list or tuple of (W,H)
screen = pygame.display.set_mode((567, 800)) # this is the canvas we can draw on
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF',40)

# Game Variables
gravity = 0.25
bird_movement =0
bird_speed = 6
game_active = True
score = 0
high_score = 0
#Background Surface
bg_surface = pygame.image.load("assets/background-day.png")
bg_surface = pygame.transform.scale2x(bg_surface).convert()

#floor Surface
floor_surface = pygame.transform.scale2x(pygame.image.load('assets/base.png')).convert()
floor_x_pos = 0

#Animated bird
bird_upflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-upflap.png").convert_alpha())
bird_midflap =pygame.transform.scale2x(pygame.image.load("assets/bluebird-midflap.png").convert_alpha())
bird_downflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-downflap.png").convert_alpha())
bird_frames = [bird_downflap,bird_midflap,bird_upflap ]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100,400))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)
#Bird Surface
#bird_surface = pygame.image.load("assets/bluebird-midflap.png")
#bird_surface = pygame.transform.scale2x(bird_surface).convert_alpha()
#bird_rect = bird_surface.get_rect(center = (100,400))



#Pipe
pipe_surface = pygame.image.load("assets/pipe-green.png")
pipe_surface = pygame.transform.scale2x(pipe_surface).convert()
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [550, 400, 350]

#game over surface
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png')).convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (288,270))

#Sounds
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 200

# game logic
# game loop
while True:
 # event loop
 for event in pygame.event.get():
     if event.type == pygame.QUIT:
         pygame.quit()
         sys.exit()
     if event.type == pygame.KEYDOWN:
         if event.key == pygame.K_SPACE:
             bird_movement = 0
             bird_movement -= bird_speed
             flap_sound.play()
         if event.key == pygame.K_SPACE and game_active == False:
             game_active = True
             pipe_list.clear()
             bird_rect.center = (100, 400)
             bird_movement=2
             score = 0

     if event.type == SPAWNPIPE:
         pipe_list.extend(create_pipe())

     #animation of bird
     if event.type == BIRDFLAP:
         if(bird_index < 2):
             bird_index += 1
         else:
             bird_index = 0

         bird_surface,bird_rect = bird_animation()
     #end animation of bird

 #draw background
 screen.blit(bg_surface,(0,0))

 if game_active :
     #controlling bird and Drawing the bird
     bird_movement += gravity
     rotated_bird = rotate_bird(bird_surface)
     bird_rect.centery +=bird_movement
     screen.blit(rotated_bird,bird_rect)
     game_active = check_collision(pipe_list)

     #pipes
     pipe_list = moves_pipe(pipe_list)
     draw_pipes(pipe_list)

     #Score
     score +=0.01
     score_sound_countdown-=1
     if score_sound_countdown == 0:
        score_sound.play()
        score_sound_countdown=200
     scoreDisplay('main_game')
 else:
     screen.blit(game_over_surface,game_over_rect)
     high_score = update_score(score,high_score)
     scoreDisplay('game_over')

 floor_x_pos-=1
 draw_floor()
 if floor_x_pos <= -576:
     floor_x_pos= 0

 #updating the frame
 pygame.display.update()
 clock.tick(120)
# quiting pygame

