import pygame
import sys
from pygame.locals import *

class Kangaroo(object):
	def __init__(self, surfPath, initx, inity):# initx and inity are map coordinates
		self.surface = pygame.image.load(surfPath)
		self.mapx = initx
		self.mapy = inity
		
	def get_camera_coords(self, origin):
		camerax = self.mapx - origin[0]
		cameray = self.mapy - origin[1]
		return camerax, cameray
	

def terminate():
	pygame.quit()
	sys.exit()

def main():
	pygame.init()
	WINWIDTH = 400
	WINHEIGHT = 300
	HALF_WINWIDTH = int(WINWIDTH / 2)
	HALF_WINHEIGHT = int(WINHEIGHT / 2)
	DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
	pygame.display.set_caption("Kangaroo Parkour - A Game By Zyzzyva038")
	FPSCLOCK = pygame.time.Clock()
	FPS = 40
	kangaroo = Kangaroo("sprites\\kangaroo_right.png", 200, 150)
	
	WHITE = (255, 255, 255)
	BGCOLOR = WHITE
	
	while True:
		DISPLAYSURF.fill(BGCOLOR)
		
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
		
		cameraOrigin = (kangaroo.mapx - HALF_WINWIDTH, kangaroo.mapy - HALF_WINHEIGHT)
		DISPLAYSURF.blit(kangaroo.surface, (200, 150))
		pygame.display.update()
		
		FPSCLOCK.tick(FPS)
	
if __name__ == "__main__":
	main()