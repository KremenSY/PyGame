import pygame
from settings  import *
from pytmx.util_pygame import load_pygame
from support import *
from random import choice
import os

class SoilTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image=surf
        self.rect=self.image.get_rect(topleft=pos)
        self.z=LAYERS['soil']

class WaterTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image=surf
        self.rect=self.image.get_rect(topleft=pos)
        self.z=LAYERS['soil water']

class Plant(pygame.sprite.Sprite):
    def __init__(self, plant_type, groups, soil, check_watered):
        super().__init__(groups)
        
        #setup
        self.plant_type=plant_type
        self.frames=import_folder(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'graphics', 'fruit', f'{plant_type}'))
        self.soil=soil
        self.check_watered=check_watered

        # plant growing
        self.age=0
        self.max_age=len(self.frames)-1
        self.grow_speed=GROW_SPEED[plant_type]
        self.harvestable=False
        
        #sprite setup
        self.image=self.frames[self.age]
        self.y_offset=-16 if plant_type=='corn' else -8
        self.rect=self.image.get_rect(midbottom=soil.rect.midbottom + pygame.math.Vector2(0, self.y_offset))
        self.z=LAYERS['ground plant']

    def grow(self):
        if self.check_watered(self.rect.center):
            self.age+=self.grow_speed

            # if plant age > 0 => plant should be on main layer
            if int(self.age)>0:
                self.z=LAYERS['main']
                self.hitbox=self.rect.copy().inflate(-26, -self.rect.height*0.4)

            if self.age>=self.max_age:
                self.age=self.max_age
                self.harvestable=True

            self.image=self.frames[int(self.age)]
            self.rect=self.image.get_rect(midbottom=self.soil.rect.midbottom + pygame.math.Vector2(0, self.y_offset))

class SoilLayer:
    def __init__(self, all_sprites, collision_sprites):

        # sprite groups
        self.all_sprites=all_sprites
        self.collision_sprites=collision_sprites
        self.soil_sprites=pygame.sprite.Group()
        self.water_sprites=pygame.sprite.Group()
        self.plant_sprites = pygame.sprite.Group()

        # graphics
        # self.soil_surf=pygame.image.load(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'graphics', 'soil', 'o.png'))
        self.soil_surfs=import_folder_dict(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'graphics', 'soil'))
        # print(self.soil_surfs)
        self.water_surfs=import_folder(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'graphics', 'soil_water'))

        self.create_soil_grid()
        self.create_hit_rects()
        
        # sounds
        self.hoe_sound=pygame.mixer.Sound(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'audio', 'hoe.wav'))
        self.hoe_sound.set_volume(0.1)

        self.plant_sound=pygame.mixer.Sound(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'audio', 'plant.wav'))
        self.hoe_sound.set_volume(0.2)
        # requirements for each of the tiles:
        # if area is farmable
        # if the soil has been watered
        # if the soil has a plant already
        # => store all this information in one grid
        pass

    def create_soil_grid(self):
        ground=pygame.image.load(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'graphics', 'world', 'ground.png'))
        h_tiles, v_tiles=ground.get_width()//TILE_SIZE, ground.get_height()//TILE_SIZE
        # print(h_tiles)
        # print(v_tiles)

        self.grid=[[[] for col in range(h_tiles)] for row in range(v_tiles)]
        # print(self.grid)
        for x, y, surf in load_pygame(
                                    os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                    'data', 'map.tmx')).get_layer_by_name(
                                    'Farmable').tiles():
            self.grid[y][x].append('F')
        # for row in self.grid: print(self.grid)
        pass # at the end of method to be able roll up method including comments at the end

    def create_hit_rects(self):
        self.hit_rects=[]
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'F' in cell:
                    x=index_col*TILE_SIZE
                    y=index_row*TILE_SIZE
                    rect=pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.hit_rects.append(rect)

    def get_hit(self, point):
        for rect in self.hit_rects:
            if rect.collidepoint(point):
                self.hoe_sound.play()

                x=rect.x//TILE_SIZE # // is floor devision
                y=rect.y//TILE_SIZE

                if 'F' in self.grid[y][x]:
                    # print('farmable')
                    self.grid[y][x].append('X')
                    self.create_soil_tiles()
                    if self.raining:
                        self.water_all()

    def water(self, target_pos):
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):
                # print('soil tile watered')
                x=soil_sprite.rect.x//TILE_SIZE
                y=soil_sprite.rect.y//TILE_SIZE
                self.grid[y][x].append('W')
                pos=soil_sprite.rect.topleft
                surf=choice(self.water_surfs)
                WaterTile(pos, surf, [self.all_sprites, self.water_sprites])

    def water_all(self):
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'X' in cell and 'W' not in cell:
                    cell.append('W')
                    x=index_col*TILE_SIZE
                    y=index_row*TILE_SIZE
                    surf=choice(self.water_surfs)
                    WaterTile((x, y), surf, [self.all_sprites, self.water_sprites])
    
    def remove_water(self):
        for sprite in self.water_sprites.sprites():
            sprite.kill()
        for row in self.grid:
            for cell in row:
                if 'W' in cell:
                    cell.remove('W')
    
    def check_watered(self, pos):
        x=pos[0]//TILE_SIZE
        y=pos[1]//TILE_SIZE
        cell = self.grid[y][x]
        is_watered = 'W' in cell
        return is_watered
    
    def plant_seed(self, target_pos, seed):
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):
                self.plant_sound.play()
                x=soil_sprite.rect.x//TILE_SIZE
                y=soil_sprite.rect.y//TILE_SIZE
                if 'P' not in self.grid[y][x]:
                    self.grid[y][x].append('P')
                    Plant(plant_type=seed, groups=[self.all_sprites, self.plant_sprites, self.collision_sprites], soil=soil_sprite, check_watered=self.check_watered) 

    def update_plants(self):
        for plant in self.plant_sprites.sprites():
            plant.grow()
    
    def create_soil_tiles(self):
        self.soil_sprites.empty()
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'X' in cell:
                   
                    # tile options''
                    # t='X' in self.grid[index_row-1][index_col] 
                    # b='X' in self.grid[index_row+1][index_col] 
                    # r='X' in row[index_col+1]
                    # l='X' in row[index_col-1]
                    ## print (f"t={t}; l={l}; b={b}; r={r}")

                    # tile_type='tlbr' # 'o'

                    # #tlbr
                    # # all sides
                    # if all ((t,l,b,r)): tile_type='xxxx' # 'x'
                    # # horizontal tiles only
                    # if l and not any((t, r,b )): tile_type= 'xlxx' # 'r'
                    # if r and not any((t, l, b)): tile_type= 'xxxr' # 'l'
                    # if l and r and not any((t, b)): tile_type= 'xlxr' # 'lr'
                    # # vertical only
                    # if t and not any((r, l, b)): tile_type= 'txxx' # 'b'
                    # if b and not any((r, l, t)): tile_type= 'xxbx' # 't'
                    # if t and b and not any((r, l)): tile_type= 'txbx' # 'tb'
                    # # corners
                    # if l and b and not any((t, r)): tile_type= 'xlbx' # 'tr'
                    # if b and r and not any((t, l)): tile_type= 'xxbr' # 'tl'
                    # if t and l and not any((b, r)): tile_type= 'tlxx' # 'br'
                    # if t and r and not any((b, l)): tile_type= 'txxr' # 'bl'
                    # # tshapes
                    # if all((t, b, r)) and not l: tile_type=  'txbr' # 'lm' # 'tbr' 
                    # if all((t, l, b)) and not r: tile_type=  'tlbx' # 'rm' # 'tbl' 
                    # if all((t, l, r)) and not b: tile_type=  'tlxr' # 'bm' # 'lrb' 
                    # if all((l, b, r)) and not t: tile_type=  'xlbr' # 'tm' # 'lrt'
                     
                    t='t' if 'X' in self.grid[index_row-1][index_col] else 'x'
                    b= 'b' if 'X' in self.grid[index_row+1][index_col] else 'x'
                    r= 'r' if 'X' in row[index_col+1] else 'x'
                    l= 'l' if 'X' in row[index_col-1] else 'x'
                    tile_type=t+l+b+r # images are renamed next way: in consequense top->left->bottom->right first letter [t,l,b,r] is set in corresponding position if edge is absent (if ther is soil in neighbour tile in corresponding direction), letter x is set otherwise

                    SoilTile(pos=(index_col*TILE_SIZE, index_row*TILE_SIZE), 
                            surf=self.soil_surfs[tile_type], 
                            groups=[self.all_sprites, self.soil_sprites])






