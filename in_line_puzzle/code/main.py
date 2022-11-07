import pygame as pg
import sys
from settings import *
from map import *

pg.init()

class Game:
	def __init__(self):
		pg.init()
		pg.display.set_caption('Something')
		self.screen = pg.display.set_mode(RES)
		self.clock = pg.time.Clock()
		self.map=Map(self)

	def run(self):
		soundObj = pg.mixer.Sound(os.path.join(BASE_DIR, 'audio', 'theme.mp3'))
		soundChn = pg.mixer.Channel(0) #create Channel object to play sounds from
		soundChn.play(soundObj, -1) #play soundObj on the channel infinite - ERROR IS HERE


		# pg.mixer.Channel(0).play(-1, pg.mixer.Sound(os.path.join(BASE_DIR, 'audio', 'theme.mp3')))
		while True:

			for event in pg.event.get():
				if event.type == pg.QUIT:
					pg.quit()
					sys.exit()

			if event.type == pg.MOUSEBUTTONDOWN:
				self.map.click()
			
			dt = self.clock.tick()//1000
			self.map.draw()
			pg.display.update()

if __name__ == '__main__':

	game = Game()
	game.run()



