import pygame, sys # for sys.exit() 
from settings import *
from level import Level
from timer import Timer

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
		pygame.display.set_caption('Farming dimulator')

		self.clock = pygame.time.Clock()
		self.level = Level()
		
	def run(self):
		while True:
			for event in pygame.event.get(): # close with [X] button
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()  
  
			dt = self.clock.tick() / 1000 # getting delta time
			self.level.run(dt)
			pygame.display.update()

if __name__ == '__main__':
	game = Game()
	game.run()
 