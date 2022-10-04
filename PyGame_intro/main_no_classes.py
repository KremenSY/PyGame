from cgi import test
from turtle import color
import pygame
from sys import exit
import os
from random import randint

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
    # play walking aimation if player is on floor
    # display jump surface when player is not on floor
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
# test_font=pygame.font.Font(None, 50) #parameters: type andsizeof font
test_font=pygame.font.Font(os.path.join('font', 'Pixeltype.ttf'), 50) #parameters: type and size of font
game_active= False # True
start_time=0
score=0

# test_surface=pygame.Surface((100, 200))
# test_surface.fill('Red')
sky_surface=pygame.image.load(os.path.join('graphics','Sky.png')).convert()
ground_surface=pygame.image.load(os.path.join('graphics', 'Ground.png')).convert()
# text_surface=test_font.render('My text', False, 'Green') #parameters: text, Anti aliasing, color
# text_surface=test_font.render(os.path.join('My game'), False, 'Green')
# score_surface=test_font.render(os.path.join('My game'), False, (64,64,64))
# score_rectangle=score_surface.get_rect(center=(400, 50))

# snail_surface=pygame.image.load(os.path.join('graphics', 'Snail', 'snail1.png')).convert_alpha()
snail_frame_1=pygame.image.load(os.path.join('graphics', 'Snail', 'snail1.png')).convert_alpha()
snail_frame_2=pygame.image.load(os.path.join('graphics', 'Snail', 'snail2.png')).convert_alpha()
snail_frames=[snail_frame_1, snail_frame_2]
snail_frame_index=0
snail_surface=snail_frames[snail_frame_index]
# snail_x_position = 600
# snail_rectangle=snail_surface.get_rect(bottomright=(600, 300))

# fly_surface=pygame.image.load(os.path.join('graphics', 'Fly', 'Fly1.png')).convert_alpha()
fly_frame1=pygame.image.load(os.path.join('graphics', 'Fly', 'Fly1.png')).convert_alpha()
fly_frame2=pygame.image.load(os.path.join('graphics', 'Fly', 'Fly2.png')).convert_alpha()
fly_frames=[fly_frame1, fly_frame2]
fly_frame_index=0
fly_surface=fly_frames[fly_frame_index]


obstacle_rect_list=[]
# print(type(obstacle_rect_list))


#player_surface=pygame.image.load(os.path.join('graphics', 'Player', 'player_walk_1.png')).convert_alpha()
player_walk_1=pygame.image.load(os.path.join('graphics', 'Player', 'player_walk_1.png')).convert_alpha()
player_walk_2=pygame.image.load(os.path.join('graphics', 'Player', 'player_walk_2.png')).convert_alpha()
player_walk=[player_walk_1, player_walk_2]
player_index=0
player_jump=pygame.image.load(os.path.join('graphics', 'Player', 'player_jump.png')).convert_alpha()
# player_rectangle=pygame.Rect() # parameters: left, top, width, height

player_surface=player_walk[player_index]
player_rectangle=player_surface.get_rect(midbottom=(80, 300))
player_gravity=0

## Game over screen
player_stand=pygame.image.load(os.path.join('graphics', 'Player', 'player_stand.png')).convert_alpha()
# player_stand_scaled=pygame.transform.scale(player_stand, (200, 400))
# player_stand_scaled=pygame.transform.scale2x(player_stand)
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
    
    # to prevent window from clocing immediately after launch
    # draw wlwmwnts
    # update everything
    for event in pygame.event.get():
        if event.type==pygame.QUIT: # Quit game if user press [X] button
            pygame.quit()
            exit()
        # if event.type==pygame.MOUSEMOTION:
        #     print(event.pos)

        # if event.type==pygame.MOUSEBUTTONUP:
        #     print(event.pos, 'button up')

        # if event.type==pygame.MOUSEBUTTONDOWN:
        #     print(event.pos, 'button down')

        # if event.type==pygame.MOUSEMOTION:
        #     # print(event.pos)
        #     if player_rectangle.collidepoint(event.pos):
        #         print('collision')

        if game_active:
            if event.type==pygame.MOUSEBUTTONDOWN:
                if player_rectangle.collidepoint(event.pos):
                    player_gravity=-20

            if event.type==pygame.KEYDOWN:
                # print ('key down')
                if event.key==pygame.K_SPACE and player_rectangle.bottom>=300:
                    # print('jump')
                    player_gravity=-20
            
            if event.type==obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surface.get_rect(bottomright=(randint(900, 1100), 300)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(bottomright=(randint(900, 1100), 210)))
            
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
            #print(type(obstacle_rect_list))
        else:     
            if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                game_active=True
                # snail_rectangle.left=800
                start_time=int(pygame.time.get_ticks()/1000)

        # if event.type==pygame.KEYUP:
        #     print('key up')

        # if event.type==obstacle_timer and game_active:
        #     # print ('test')
        #     #print(type(obstacle_rect_list))
        #     obstacle_rect_list.append(snail_surface.get_rect(bottomright=(randint(900, 1100), 300)))
           




    #screen.blit(test_surface, (0,0)) 
    if game_active:
        screen.blit(sky_surface, (0,0)) 
        screen.blit(ground_surface, (0,300))
        score=display_score()
        # pygame.draw.rect(screen, '#c0e8ec', score_rectangle)
        # pygame.draw.rect(screen, '#c0e8ec', score_rectangle, 10, 20)
        
        #pygame.draw.ellipse(screen, 'Brown', pygame.Rect(50,200,100,100) )
        # pygame.draw.line(screen, 'Gold', (0,0),(800,400), 10)
        # pygame.draw.line(screen, 'Gold', (0,0),pygame.mouse.get_pos(), 10)
        # screen.blit(text_surface,(300, 50))
        # screen.blit(score_surface,(score_rectangle))
        # snail_x_position-=4
        # if snail_x_position < -100: snail_x_position=800
        # screen.blit(snail_surface, (snail_x_position, 250))
        
        # snail_rectangle.x-=4
        # if snail_rectangle.right <= 0: snail_rectangle.left=800
        # screen.blit(snail_surface, snail_rectangle)
        
        # player_rectangle.left+=1 # move a rectangle
        # print(player_rectangle.left) # to measure coordinates
        # screen.blit(player_surface, (80, 200))
        
        player_gravity+=1
        player_rectangle.y+=player_gravity
        if player_rectangle.bottom>=300:
            player_rectangle.bottom = 300
        player_animation()
        screen.blit(player_surface, player_rectangle)

        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        game_active=collisions(player_rectangle, obstacle_rect_list)

        # if snail_rectangle.colliderect(player_rectangle):
        #     # pygame.quit()
        #     # exit()
        #     game_active=False
        
        # print(pygame.key.get_pressed())
        # keys=pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        #         print('Jump')
        # print(player_rectangle.colliderect(snail_rectangle)) # returns 0 if no collision and 1 if collision
        # if player_rectangle.colliderect(snail_rectangle):
        #   print('collision')

        # mouse_position=pygame.mouse.get_pos()
        # if player_rectangle.collidepoint(mouse_position):
        #     # print('collision')
        #     #print(pygame.mouse.get_pos())
        #     print(pygame.mouse.get_pressed())
    else:
        # continue
        # screen.fill('Yellow')
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
    


 