# Kangaroo Parkour
# Copyright 2018 by Zhiheng Wang
# All rights reserved. 

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
		
	def get_self_rect(self, origin):
		rect = ALL_SURFACE[self.surface].get_rect()
		rect.topleft = (self.x, self.get_cameray(origin))
		return rect
		
		
class Kangaroo(object):
	def __init__(self):
		self.surface = "KANGAROO_R"
		self.rect = None


def showPauseScreen(origin):
	drawSprites(origin)
	DISPLAYSURF.blit(pauseTextSurf, pauseTextRect)
	DISPLAYSURF.blit(contButtonSurf, contButtonRect)
	pygame.display.update()
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			elif event.type == KEYUP:
				if event.key == K_c:
					return
			elif event.type == MOUSEBUTTONUP:
				if contButtonRect.collidepoint(event.pos):
					return
		
def showStartScreen():
	DISPLAYSURF.fill(BGCOLOR)
	DISPLAYSURF.blit(startTextSurf, startTextRect)
	DISPLAYSURF.blit(startButtonSurf, startButtonRect)
	pygame.display.update()
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			elif event.type == MOUSEBUTTONUP:
				if startButtonRect.collidepoint(event.pos):
					return
			elif event.type == KEYUP:
				if event.key == K_s:
					return
	
def drawSprites(origin):# without updating screen
	DISPLAYSURF.fill(BGCOLOR)
	DISPLAYSURF.blit(ALL_SURFACE[kangaroo.surface], kangaroo.rect)
	if showRects:
		pygame.draw.rect(DISPLAYSURF, (255, 0, 0), kangaroo.rect, 2)
	for barrier in barriers:
		DISPLAYSURF.blit(ALL_SURFACE[barrier.surface], barrier.get_self_rect(origin))
		if showRects:
			pygame.draw.rect(DISPLAYSURF, (255, 0, 0), barrier.get_self_rect(origin), 2)
	
def gameOverAni(origin):
	drawSprites(origin)
	DISPLAYSURF.blit(gameOverSurf, gameOverRect)
	pygame.display.update()
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			

def hasWonAni(origin):
	drawSprites(origin)
	DISPLAYSURF.blit(hasWonSurf, hasWonRect)
	pygame.display.update()
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
	
def terminate():
	pygame.quit()
	sys.exit()

def main():
	global ALL_SURFACE, hasWonSurf, hasWonRect, gameOverSurf, gameOverRect, DISPLAYSURF, kangaroo, barriers, BGCOLOR, showRects, startButtonSurf, startButtonRect, startTextSurf, startTextRect, pauseTextSurf, pauseTextRect, contButtonSurf, contButtonRect

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
	FPS = 60
	
	KANGAROO_WIDTH = 100
	KANGAROO_HEIGHT = 125
	BASIC_BARRIER_WIDTH = 100
	BASIC_BARRIER_HEIGHT = 20
	KANGAROO_F = pygame.image.load("sprites\\kangaroo_right.png")
	KANGAROO_R = pygame.transform.scale(KANGAROO_F, (KANGAROO_WIDTH, KANGAROO_HEIGHT))
	BASIC_BARRIER_F = pygame.image.load("sprites\\basic_barrier.png")
	ALL_SURFACE = {
		"KANGAROO_R" : KANGAROO_R.convert(),
		"KANGAROO_L" : pygame.transform.flip(KANGAROO_R, True, False).convert(),# TODO is it extra? 
		"BASIC_BARRIER" : pygame.transform.scale(BASIC_BARRIER_F, (BASIC_BARRIER_WIDTH, BASIC_BARRIER_HEIGHT)).convert()
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
	length = LEVEL["length"]
	
	SCREEN_SIZE = 50
	FONT = pygame.font.Font("fonts\\console.ttf", SCREEN_SIZE)
	hasWonSurf = FONT.render("YOU WON", True, GREEN)
	hasWonRect = hasWonSurf.get_rect()
	hasWonRect.center = (HALF_WINWIDTH, HALF_WINHEIGHT)
	gameOverSurf = FONT.render("GAME OVER", True, RED)
	gameOverRect = gameOverSurf.get_rect()
	gameOverRect.center = (HALF_WINWIDTH, HALF_WINHEIGHT)
	
	showRects = False
	
	kangarooSpeed = 3
	fallingSpeed = 3
	fallingSpeedAddAmont = 1
	fallingSpeedAddTime = 500
	pygame.time.set_timer(USEREVENT, fallingSpeedAddTime)
	
	SCREEN_FONT_SIZE = 30
	SCREEN_FONT = pygame.font.Font("fonts\\console.ttf", SCREEN_FONT_SIZE)
	startTextPos = (HALF_WINWIDTH, 200)
	startButtonPos = (HALF_WINWIDTH, 400)
	startTextSurf = SCREEN_FONT.render("Kangaroo Parkour", True, BLACK)
	startTextRect = startTextSurf.get_rect()
	startTextRect.center = startTextPos
	startButtonSurf = SCREEN_FONT.render("Start", True, BLACK, GREEN)
	startButtonRect = startButtonSurf.get_rect()
	startButtonRect.center = startButtonPos
	
	pauseTextPos = (HALF_WINWIDTH, 200)
	pauseTextSurf = SCREEN_FONT.render("Game Paused", True, BLACK)
	pauseTextRect = pauseTextSurf.get_rect()
	pauseTextRect.center = pauseTextPos
	contButtonPos = (HALF_WINWIDTH, 400)
	contButtonSurf = SCREEN_FONT.render("Continue", True, BLACK, GREEN)
	contButtonRect = contButtonSurf.get_rect()
	contButtonRect.center = contButtonPos
	pauseButtonPos = (0, 0)
	pauseButtonSurf = SCREEN_FONT.render("Pause", True, BLUE, GREEN)# TODO make it transparent
	pauseButtonRect = pauseButtonSurf.get_rect()
	pauseButtonRect.topleft = pauseButtonPos
	
	showStartScreen()
	
	while True:# MAIN LOOP
		if origin < length:
			origin += fallingSpeed
			if leftKeyPressed:
				kangaroo.rect.left -= kangarooSpeed
			if rightKeyPressed:
				kangaroo.rect.left += kangarooSpeed
			for barrier in barriers:
				if kangaroo.rect.colliderect(barrier.get_self_rect(origin)):
					gameOverAni(origin)
		else:
			hasWonAni(origin)
		
		drawSprites(origin)
		DISPLAYSURF.blit(pauseButtonSurf, pauseButtonRect)
		pygame.display.update()
		
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
				elif event.key == K_p:
					showPauseScreen(origin)
			elif event.type == USEREVENT:
				fallingSpeed += fallingSpeedAddAmont
			elif event.type == MOUSEBUTTONUP:
				if pauseButtonRect.collidepoint(event.pos):
					showPauseScreen(origin)
		
		FPSCLOCK.tick(FPS)
		
if __name__ == "__main__":
	main()