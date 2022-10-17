import pygame as pg
import os


class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'audio')
        self.shotgun = pg.mixer.Sound(os.path.join(self.path, 'shotgun.wav'))
        self.npc_pain = pg.mixer.Sound(os.path.join(self.path, 'npc_pain.wav'))
        self.npc_death = pg.mixer.Sound(os.path.join(self.path, 'npc_death.wav'))
        self.npc_shot = pg.mixer.Sound(os.path.join(self.path, 'npc_attack.wav'))
        self.npc_shot.set_volume(0.2)
        self.player_pain = pg.mixer.Sound(os.path.join(self.path, 'player_pain.wav'))
        self.theme = pg.mixer.music.load(os.path.join(self.path, 'theme.mp3'))
        pg.mixer.music.set_volume(0.4)