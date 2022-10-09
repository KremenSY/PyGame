import pygame
from settings import *
from support import *
from timer import Timer
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, tree_sprites, interaction, soil_layer, toggle_shop):
        super().__init__(group)

        self.import_assets()
        self.status='down_idle'
        self.frame_index=0

		# general setup
        self.image = self.animations[self.status][self.frame_index] # pygame.Surface((32, 64))
        # self.image.fill('green')
        self.rect = self.image.get_rect(center = pos)
        self.z=LAYERS['main']

		# movement attributes
        self.direction=pygame.math.Vector2()
        self.pos=pygame.math.Vector2(self.rect.center)
        self.speed=200

        # collision
        self.hitbox=self.rect.copy().inflate((-126, -70)) # inflate change dimensions, rectangle remaines centered
        self.collision_sprites = collision_sprites

        # timers
        self.timers={
            'tool use': Timer(350, self.use_tool),
            'tool switch': Timer(200),
            'seed use': Timer(350, self.use_seed),
            'seed switch': Timer(200)
        }

        #tools
        self.tools=['hoe', 'axe', 'water']
        self.tool_index=0
        self.selected_tool=self.tools[self.tool_index]

        # seeds
        self.seeds=['corn', 'tomato']
        self.seed_index=0
        self.selected_seed=self.seeds[self.seed_index]

        #inventory
        self.item_inventory={
            "wood":5,
            'apple':5,
            'corn':5,
            'tomato':5
        }
        self.seed_inventory={
            'corn':5,
            'tomato':5
        }
        self.money=200

        # iteractions
        self.tree_sprites=tree_sprites
        self.interaction=interaction
        self.sleep=False
        self.soil_layer=soil_layer
        self.toggle_shop=toggle_shop

        # sound
        self.watering=pygame.mixer.Sound(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'audio', 'water.mp3'))
        self.watering.set_volume(0.3)

    def use_tool(self):
        # print('tool use')
        # print(self.selected_tool)
        if self.selected_tool=='hoe':
            self.soil_layer.get_hit(self.target_pos)
        if self.selected_tool=='axe':
            for tree in self.tree_sprites.sprites():
                if tree.rect.collidepoint(self.target_pos):
                    tree.damage()
        if self.selected_tool=='water':
            self.soil_layer.water(self.target_pos)
            self.watering.play()

    def get_target_pos(self):
        self.target_pos=self.rect.center + PLAYER_TOOL_OFFSET[self.status.split('_')[0]]

    def use_seed(self):
        if self.seed_inventory[self.selected_seed]>0:
            self.soil_layer.plant_seed(self.target_pos, self.selected_seed)
            self.seed_inventory[self.selected_seed] -=1

    def import_assets(self):
        self.animations={'up':[], 'down':[], 'left':[], 'right': [],
                        'right_idle':[], 'left_idle':[], 'up_idle':[], 'down_idle':[],
                        'right_hoe':[], 'left_hoe':[], 'up_hoe':[], 'down_hoe': [],
                        'right_axe':[], 'left_axe':[], 'up_axe':[], 'down_axe':[],
                        'right_water':[], 'left_water':[], 'up_water':[], 'down_water':[]}

        for animation in self.animations.keys():
            # full_path="../graphics/character/"+animation
            full_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'graphics', 'character', animation)
            self.animations[animation]=import_folder(full_path) 
            # print(self.animations)
            pass
        
    def animate(self, dt):
        self.frame_index+=4*dt
        if self.frame_index>=len(self.animations[self.status]):
            self.frame_index=0
        self.image=self.animations[self.status][int(self.frame_index)]

    def input(self):
        keys=pygame.key.get_pressed()

        if not self.timers['tool use'].active and not self.sleep:
        # dyrections
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.direction.y=-1
                self.status='up'
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.direction.y=1
                self.status='down'
            else: 
                self.direction.y=0

            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.direction.x=1
                self.status='right'
            elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.direction.x=-1
                self.status='left'
            else:
                self.direction.x=0

            # tool use
            if keys[pygame.K_SPACE]:
                # timer for tool use
                self.timers['tool use'].activate()
                self.direction=pygame.math.Vector2()
                self.frame_index=0

            # change tool
            if keys[pygame.K_q] and not self.timers['tool switch'].active:
                self.timers['tool switch'].activate()
                self.tool_index+=1
                self.tool_index=self.tool_index if self.tool_index<len(self.tools) else 0
                self.selected_tool=self.tools[self.tool_index]

            # seed use
            if keys[pygame.K_r] or keys[pygame.K_RCTRL]:
                self.timers['seed use'].activate()
                self.direction=pygame.math.Vector2()
                self.frame_index=0
                # print('use seed') # no animation present

            # change seed
            if keys[pygame.K_e] and not self.timers['seed switch'].active:
                self.timers['seed switch'].activate()
                self.seed_index+=1
                self.seed_index=self.seed_index if self.seed_index<len(self.seeds) else 0
                self.selected_seed=self.seeds[self.seed_index]
                # print('change seed') # no animation present

            # sleep and shop
            if keys[pygame.K_TAB] or keys[pygame.K_RETURN]:
                collided_interaction_sprite=pygame.sprite.spritecollide(sprite=self, group=self.interaction, dokill=False) # false for we do not destroy Bed sprite after collision with player
                if collided_interaction_sprite:
                    if collided_interaction_sprite[0].name=='Trader':
                        self.toggle_shop()
                    if collided_interaction_sprite[0].name=='Bed':
                        self.status='left_idle'
                        self.sleep=True

    def get_status (self):
        # movement
        # if player is not moving add __idle to status
        if self.direction.magnitude()==0:
            self.status=self.status.split("_")[0]+'_idle'

        # tool use
        if self.timers['tool use'].active:
            # print('Tool is being used')
            self.status=self.status.split("_")[0]+'_'+self.selected_tool

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == "horizontal":
                        if self. direction.x>0: # player is moving right
                            self.hitbox.right=sprite.hitbox.left
                        if self.direction.x<0:
                            self.hitbox.left=sprite.hitbox.right
                        self.rect.centerx=self.hitbox.centerx
                        self.pos.x=self.hitbox.centerx
                    
                    if direction == 'vertical':
                        if self.direction.y>0: # player is moving down
                            self.hitbox.bottom=sprite.hitbox.top # putting bottom of player to top of obstacle
                        if self.direction.y<0: # player is moving up
                            self.hitbox.top=sprite.hitbox.bottom
                        self.rect.centery=self.hitbox.centery
                        self.pos.y=self.hitbox.centery

    def move(self, dt):
        # normalizinf vector - is used to
        if self.direction.magnitude()>0:
            self.direction=self.direction.normalize()

        # horizontal movement
        self.pos.x += self.direction.x*self.speed*dt
        self.hitbox.centerx=round(self.pos.x) # i f not use round it will be truncated
        self.rect.centerx=self.hitbox.centerx
        self.collision('horizontal')

        # vertical movement
        self.pos.y += self.direction.y*self.speed*dt
        self.hitbox.centery=round(self.pos.y)
        self.rect.centery=self.hitbox.centery
        self.collision('vertical')

    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()
        self.get_target_pos()

        self.move(dt)
        self.animate(dt)