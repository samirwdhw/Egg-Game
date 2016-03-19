#Egg catching Game

import pygame, random, sys
from pygame.locals import *

FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 640 # size of window's width in pixels
WINDOWHEIGHT = 480 # size of windows' height in pixels
BGCOLOR = (102,205,170)
MOTIONSPEED = 10   #Speed of the moving duck
fpsClock = pygame.time.Clock()

#Initialize displaysurf
DISPLAYSURF	= pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)

#Duck Things
duck_w = 600/10
duck_h = 540/10
duckImg = pygame.image.load('duck.png')
duckImg = pygame.transform.scale(duckImg, (int(duck_w), int(duck_h)))
movingRight = False
movingLeft = False

#To see time since game started
time = pygame.time.get_ticks()


#Time after which eggs fall(miliseconds)
egg_delay = 5000

#Co-ordinates of the duck

duck_x = 0
duck_y = 400

#To store all the eggs
eggs = []
egg_w = 589/25
egg_h = 800/25

#Egg things

class Egg(object):

	def __init__ (self, x, y):
		self.w = 589/25
		self.h = 800/25
		self.Img = pygame.image.load('egg.png')
		self.Img = pygame.transform.scale(self.Img, (self.w, self.h))
		self.x = x
		self.y = y

	def move(self):
		self.y += MOTIONSPEED

	def destroy(self):
		eggs.remove(self)


while True: 

	DISPLAYSURF.fill(BGCOLOR)
	DISPLAYSURF.blit(duckImg, (duck_x, duck_y))


	if( pygame.time.get_ticks() >= time + egg_delay):
		time = pygame.time.get_ticks()
		eggs.append(Egg(random.randint(duck_x - 50, duck_x + 50),egg_h))


	for egg in eggs:
		
		if( egg.x in range(duck_x, duck_x + duck_w) and egg.y in range(duck_y, duck_y + duck_h)):
			egg.destroy()

		elif( egg.y >= duck_h + duck_y):
			egg.destroy()

		else:
			DISPLAYSURF.blit(egg.Img, (egg.x, egg.y))
			egg.move()

	for event in pygame.event.get():
		
		if event.type == KEYDOWN:

			if event.key == K_LEFT:
				movingLeft = True
			elif event.key == K_RIGHT:
				movingRight = True

		if event.type == KEYUP:
			
			if event.key in (K_LEFT, K_a):
				movingLeft = False
			elif event.key in (K_RIGHT, K_d):
				movingRight = False 

		if event.type == QUIT:
			pygame.quit()
			sys.exit()		

	if movingLeft == True and duck_x - MOTIONSPEED > 0:
		duck_x  -= MOTIONSPEED
	elif movingRight == True and duck_x + MOTIONSPEED < (WINDOWWIDTH- duck_w ):
		duck_x	+= MOTIONSPEED 

	pygame.display.update()
	fpsClock.tick(FPS)