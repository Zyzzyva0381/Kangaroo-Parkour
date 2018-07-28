import pygame
import sys
import json
from pygame.locals import *


class BasicBarrier(object):
	def __init__(self, x, mapy):
		self.surface = "BASIC_BARRIER"
		self.x = x
		self.mapy = mapy
		
	def get_cameray(self, origin):
		return self.mapy - origin
		
		
class Kangaroo(object):
	def __init__(self):
		self.surface = "KANGAROO_R"
		self.rect = None
	

def terminate():
	pygame.quit()
	sys.exit()

def main():
	pygame.init()
	WINWIDTH = 500
	WINHEIGHT = 600
	HALF_WINWIDTH = int(WINWIDTH / 2)
	HALF_WINHEIGHT = int(WINHEIGHT / 2)
	DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
	pygame.display.set_caption("Kangaroo Parkour 0.1.0 Alpha")
	
	leftKeyPressed = False
	rightKeyPressed = False
	
	WHITE = (255,255,255)
	BLACK = (0,0,0)
	RED = (225,0,0)
	GREEN = (0,225,0)
	BLUE = (10,10,225)
	BGCOLOR = WHITE
	
	FPSCLOCK = pygame.time.Clock()
	FPS = 30
	
	KANGAROO_WIDTH = 100
	KANGAROO_HEIGHT = 125
	BASIC_BARRIER_WIDTH = 100
	BASIC_BARRIER_HEIGHT = 20
	KANGAROO_F = pygame.image.load("sprites\\kangaroo_right.png")
	KANGAROO_R = pygame.transform.scale(KANGAROO_F, (KANGAROO_WIDTH, KANGAROO_HEIGHT))
	BASIC_BARRIER_F = pygame.image.load("sprites\\basic_barrier.png")
	ALL_SURFACE = {
		"KANGAROO_R" : KANGAROO_R,
		"KANGAROO_L" : pygame.transform.flip(KANGAROO_R, True, False),
		"BASIC_BARRIER" : pygame.transform.scale(BASIC_BARRIER_F, (BASIC_BARRIER_WIDTH, BASIC_BARRIER_HEIGHT))
	}
	origin = 0
	kangaroo = Kangaroo()
	kangaroo.rect = ALL_SURFACE[kangaroo.surface].get_rect()
	kangaroo.rect.center = (HALF_WINWIDTH, HALF_WINHEIGHT)
	del KANGAROO_F, KANGAROO_R, BASIC_BARRIER_F
	
	LEVEL_F = open("levels\\level_1.json", "r")
	LEVEL_T = LEVEL_F.read()
	LEVEL_F.close()
	LEVEL = json.loads(LEVEL_T)
	barriers = []
	for pos in LEVEL["barriers"]:
		barriers.append(BasicBarrier(pos["x"], pos["y"]))
	
	while True:# MAIN LOOP
		DISPLAYSURF.fill(BGCOLOR)
		
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			elif event.type == KEYDOWN:
				if event.key in (K_a, K_LEFT):
					kangaroo.surface = "KANGAROO_L"
					leftKeyPressed = True
					#print("leftKeyPressed = True")
				elif event.key in (K_d, K_RIGHT):
					kangaroo.surface = "KANGAROO_R"
					rightKeyPressed = True
					#print("rightKeyPressed = True")
			elif event.type == KEYUP:
				if event.key in (K_a, K_LEFT):
					leftKeyPressed = False
					#print("leftKeyPressed = False")
				elif event.key in (K_d, K_RIGHT):
					rightKeyPressed = False
					#print("rightKeyPressed = False")
				
		DISPLAYSURF.blit(ALL_SURFACE[kangaroo.surface], kangaroo.rect)
		for barrier in barriers:
			DISPLAYSURF.blit(ALL_SURFACE[barrier.surface], (barrier.x, barrier.get_cameray(origin)))
		pygame.display.update()
		
		FPSCLOCK.tick(FPS)
		
if __name__ == "__main__":
	main()