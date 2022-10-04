import pygame
from sys import exit
import os
from random import randint, choice

class Player(pygame.sprite.Sprite): # Sprite is a combination ofsurface  and rectangle
    def __init__ (self): # Constructor
        super().__init__() # Call constructor of parent class
        player_walk_1=pygame.image.load(os.path.join('graphics', 'Player', 'player_walk_1.png')).convert_alpha() # use os.path.join for different OS compability
        player_walk_2=pygame.image.load(os.path.join('graphics', 'Player', 'player_walk_2.png')).convert_alpha() # does not  need .self as we do not need  access it from outside __init__ method
        self.player_walk=[player_walk_1, player_walk_2] # need self. as we will useit outsideof this method
        self.player_index=0
        self.player_jump=pygame.image.load(os.path.join('graphics', 'Player', 'player_jump.png')).convert_alpha()
        self.image=self.player_walk[self.player_index]
        self.rect=self.image.get_rect(midbottom=(80, 300))
        self.gravity=0
        self.jump_sound=pygame.mixer.Sound(os.path.join('audio', 'jump.mp3'))
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys=pygame.key.get_pressed() # can create a delay, but it is not  significant in this example
        if keys[pygame.K_SPACE] and self.rect.bottom>=300:
            self.gravity=-20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity+=1
        self.rect.y+=self.gravity
        if self.rect.bottom>=300:
            self.rect.bottom=300

    def animation_state(self):
        if self.rect.bottom<300:
            self.image=self.player_jump
        else:
            self.player_index+=0.1
            if self.player_index>=len(self.player_walk):
                self.player_index=0
            self.image=self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type=='fly':
            fly_frame1=pygame.image.load(os.path.join('graphics', 'Fly', 'Fly1.png')).convert_alpha()
            fly_frame2=pygame.image.load(os.path.join('graphics', 'Fly', 'Fly2.png')).convert_alpha()
            self.frames=[fly_frame1, fly_frame2]
            y_pos=210
        else:
            snail_frame_1=pygame.image.load(os.path.join('graphics', 'Snail', 'snail1.png')).convert_alpha()
            snail_frame_2=pygame.image.load(os.path.join('graphics', 'Snail', 'snail2.png')).convert_alpha()
            self.frames=[snail_frame_1, snail_frame_2]
            y_pos=300
        self.animation_index=0
        self.image=self.frames[self.animation_index]
        self.rect=self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index+=0.1
        if self.animation_index>=len(self.frames):
            self.animation_index=0
        self.image=self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x-=6
        self.destroy()

    def destroy(self):
        if self.rect.x<=-100:
            self.kill
 
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False): # parameters sprite, group, bool=if colliding object should be deleted
        obstacle_group.empty()
        return False
    else:
        return True

def display_score():
    current_time=int(pygame.time.get_ticks()/1000)-start_time
    # print(current_time)
    score_surface=test_font.render(f'{current_time}', False, (64,64,64))
    score_rectangle=score_surface.get_rect(center=(400,50))
    screen.blit (score_surface, score_rectangle)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom==300:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen .blit(fly_surface, obstacle_rect)
        obstacle_list=[obstackle for obstackle in obstacle_list if obstackle.x>-100]
    return obstacle_list

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def player_animation():
    global player_surface, player_index
    if player_rectangle.bottom<300:
        player_surface=player_jump
    else:
        player_index+=0.1
        if player_index >= len(player_walk):
            player_index=0
        player_surface=player_walk[int(player_index)]

pygame.init()
screen_width=800 #px
screen_height=400 #px
screen=pygame.display.set_mode((screen_width, screen_height)) # Open game window with specified resolution
pygame.display.set_caption('Runner') # Title 0f window
clock=pygame.time.Clock()
test_font=pygame.font.Font(os.path.join('font', 'Pixeltype.ttf'), 50) #parameters: type and size of font
game_active= False # True
start_time=0
score=0
bg_music=pygame.mixer.Sound(os.path.join('audio', 'music.wav'))
bg_music.play(loops=-1)

player=pygame.sprite.GroupSingle() # Group containing a sprite
player.add(Player()) # Add sprite to group
obstacle_group=pygame.sprite.Group()
sky_surface=pygame.image.load(os.path.join('graphics','Sky.png')).convert()
ground_surface=pygame.image.load(os.path.join('graphics', 'Ground.png')).convert()
snail_frame_1=pygame.image.load(os.path.join('graphics', 'Snail', 'snail1.png')).convert_alpha()
snail_frame_2=pygame.image.load(os.path.join('graphics', 'Snail', 'snail2.png')).convert_alpha()
snail_frames=[snail_frame_1, snail_frame_2]
snail_frame_index=0
snail_surface=snail_frames[snail_frame_index]
fly_frame1=pygame.image.load(os.path.join('graphics', 'Fly', 'Fly1.png')).convert_alpha()
fly_frame2=pygame.image.load(os.path.join('graphics', 'Fly', 'Fly2.png')).convert_alpha()
fly_frames=[fly_frame1, fly_frame2]
fly_frame_index=0
fly_surface=fly_frames[fly_frame_index]
obstacle_rect_list=[]
player_walk_1=pygame.image.load(os.path.join('graphics', 'Player', 'player_walk_1.png')).convert_alpha()
player_walk_2=pygame.image.load(os.path.join('graphics', 'Player', 'player_walk_2.png')).convert_alpha()
player_walk=[player_walk_1, player_walk_2]
player_index=0
player_jump=pygame.image.load(os.path.join('graphics', 'Player', 'player_jump.png')).convert_alpha()
player_surface=player_walk[player_index]
player_rectangle=player_surface.get_rect(midbottom=(80, 300))
player_gravity=0
player_stand=pygame.image.load(os.path.join('graphics', 'Player', 'player_stand.png')).convert_alpha()
player_stand_scaled=pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rectangle=player_stand.get_rect(center=(400,200))
player_stand_rectangle_scaled=player_stand_scaled.get_rect(center=(400,200))
game_name=test_font.render('Pixel runner', False, (111,196, 169))
game_name_rectangle=game_name.get_rect(center=(400,60))
game_message=test_font.render('Press space to run', False, (111,196,169))
game_message_rectangle=game_message.get_rect(center=(400, 340))
obstacle_timer = pygame.USEREVENT+1
pygame.time.set_timer(obstacle_timer, 1500)
snail_animation_timer=pygame.USEREVENT+2
pygame.time.set_timer(snail_animation_timer, 500)
fly_animation_timer=pygame.USEREVENT+3
pygame.time.set_timer(fly_animation_timer, 200)

while True:

    for event in pygame.event.get():
        if event.type==pygame.QUIT: # Quit game if user press [X] button
            pygame.quit()
            exit()

        if game_active:
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE and player_rectangle.bottom>=300:
                    player_gravity=-20
            
            if event.type==obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
            
            if event.type==snail_animation_timer:
                if snail_frame_index<1.8: 
                    snail_frame_index+=0.2
                else:
                    snail_frame_index=0
                snail_surface=snail_frames[int(snail_frame_index)]

            if event.type==fly_animation_timer:
                if fly_frame_index==0: 
                    fly_frame_index=1
                else:
                    fly_frame_index=0
                fly_surface=fly_frames[fly_frame_index]    
        else:     
            if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                game_active=True
                start_time=int(pygame.time.get_ticks()/1000)
    
    if game_active:
        screen.blit(sky_surface, (0,0)) 
        screen.blit(ground_surface, (0,300))
        score=display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active=collision_sprite()

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand_scaled, player_stand_rectangle_scaled)
        obstacle_rect_list.clear()
        player_rectangle.midbottom=(80, 300)
        player_gravity=0
        score_message=test_font.render(f'Your score is {score}', False, (111, 196, 169))
        score_message_rectangle=score_message.get_rect(center=(400,330))
        screen.blit(game_name, game_name_rectangle)
        
        if score==0:
            screen.blit(game_message, game_message_rectangle)
        else:
            screen.blit(score_message, score_message_rectangle)

    pygame.display.update()
    clock.tick(60) # This while True loop should not run faster  then 60 fps
    


 