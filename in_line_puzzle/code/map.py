# from asyncio.windows_events import NULL
NULL=0
import pygame as pg
from settings import *
import os
import math
import random

class Map:
    def __init__(self, game):
        self.game = game
        self.win_map=self.map_copy(WIN_MAP) # map state for win
        # self.map = self.map_copy(test_map) # create new map for testing win mechanics
        self.map = self.create_map() # create new random map
        self.rows = len(self.map)
        self.cols = len(self.map[0])
        self.first_click_pos=NULL
        self.second_click_pos=NULL
        self.active=False # on start screen active=False, on game screen active=True
        self.start_num=0 # count of starts of new game

    def map_copy(self, map): # create deep copy of map
        return [row[:] for row in map]

    def create_map(self): # create random map with fixed positions of immovable and free tiles by shuufling final map
        map = self.map_copy(WIN_MAP)
        while map==self.win_map: # to prevent random coinside of maps
            values=[]
            for i in  range(len(map)):
                for j in range(len(map[0])):
                    if map[i][j]!=4 and map[i][j]!=0:
                        values.append(map[i][j])
            random.shuffle(values)
            for i in  range(len(map)):
                for j in range(len(map[0])):
                    if map[i][j]!=4 and map[i][j]!=0:
                        map[i][j]=values.pop()
        return map

    def draw(self):
        if self.active==False: # draw start/WIN screen
            # write hint
            font_hint = pg.font.Font(os.path.join(BASE_DIR, 'font', 'doom.ttf'), 50)
            self.game.screen.blit(pg.image.load(os.path.join(BASE_DIR, 'graphics', 'start_screen.png')), (0,0))
            text_surf = font_hint.render(f'right click to start new game', False, (125,0,0))
            text_rect = text_surf.get_rect(center = (WIDTH//2,HEIGHT//2+100))
            self.game.screen.blit(text_surf,text_rect)
            # write WIN
            if self.start_num:
                font_win = pg.font.Font(os.path.join(BASE_DIR, 'font', 'doom.ttf'), 200)
                win_surf = font_win.render(f'Victory', False, (255,0,0))
                win_rect = win_surf.get_rect(center = (WIDTH//2,HEIGHT//2))
                self.game.screen.blit(win_surf,win_rect)
                return
        else: # draw game screen
            self.game.screen.blit(pg.image.load(os.path.join(BASE_DIR, 'graphics', 'background.png')), (0,0))
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.map[j][i]!=0:
                        self.game.screen.blit(pg.image.load(os.path.join(BASE_DIR, 'graphics', f'{self.map[j][i]}.png')), (HORIZONTAL_MARGIN+i * TILE_SIZE, VERTICAL_MARGIN+j * TILE_SIZE))

    def get_pos(self): # get position of mouse (click) as indexes of tile on map, return NULL if click out of map
        pos=pg.mouse.get_pos()
        row=NULL
        col=NULL
        if pos[0] in range(HORIZONTAL_MARGIN, HORIZONTAL_MARGIN+self.cols*TILE_SIZE) and pos[1] in range(VERTICAL_MARGIN, VERTICAL_MARGIN+self.cols*TILE_SIZE):
            col=(pos[0]-HORIZONTAL_MARGIN)//TILE_SIZE
            row=(pos[1]-VERTICAL_MARGIN)//TILE_SIZE
            return row, col
        return NULL

    def check_swap(self): # check if element in self.first_click_pos can be moved to self.second_click_pos
        if self.first_click_pos and self.second_click_pos: 
            if (math.fabs(self.first_click_pos[0]-self.second_click_pos[0])==1 and self.first_click_pos[1]==self.second_click_pos[1]) or (math.fabs(self.first_click_pos[1]-self.second_click_pos[1])==1 and self.first_click_pos[0]==self.second_click_pos[0]):
                if self.map[self.first_click_pos[0]][self.first_click_pos[1]]!=4 and self.map[self.second_click_pos[0]][self.second_click_pos[1]]==0:
                    return True
        return False
    
    def check_win(self):
        if self.map==self.win_map:
            return True
        return False

    def swap(self): # move element in self.first_click_pos to self.second_click_pos
        self.map[self.second_click_pos[0]][self.second_click_pos[1]]=self.map[self.first_click_pos[0]][self.first_click_pos[1]]
        self.map[self.first_click_pos[0]][self.first_click_pos[1]]=0
    
    def click(self): # event handler for mouse click: if on start screen -> start game; if on game screen -> select element to move or place it can be moved to
        
        if self.active==False:
            pg.mixer.Channel(2).play(pg.mixer.Sound(os.path.join(BASE_DIR, 'audio', 'start_end.wav')))
            # self.map = self.map_copy(test_map)
            self.map = self.create_map()
            self.active=True
            # print('Start Game')
            pg.time.wait(300)
            return 
           
        pos=self.get_pos()
        if pos:
            if not self.first_click_pos:
                self.first_click_pos=pos
                self.second_click_pos=NULL
            elif not self.second_click_pos:
                self.second_click_pos=pos
                if self.check_swap():
                    self.swap()
                    self.first_click_pos=NULL
                    self.second_click_pos=NULL
                    pg.mixer.Channel(1).play(pg.mixer.Sound(os.path.join(BASE_DIR, 'audio', 'click.mp3')))
                else:
                    self.first_click_pos=self.second_click_pos
                    self.second_click_pos=NULL
            else:
                pass
        
        if self.check_win():
            pg.mixer.Channel(2).play(pg.mixer.Sound(os.path.join(BASE_DIR, 'audio', 'start_end.wav')))
            self.active=False
            self.start_num+=1
            # print("Win")
            
        # print('pos=', pos)
        # print('self.first_click_pos=', self.first_click_pos)
        # print('self.second_click_pos=', self.second_click_pos)
        # print('check_move=', self.check_swap())
        # print(self.map)
        pg.time.wait(300)