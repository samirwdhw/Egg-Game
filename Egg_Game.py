#Egg catching Game

import pygame, random, sys
from pygame.locals import *

pygame.init()

#Font
myfont = pygame.font.Font("freesansbold.ttf", 30)

FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 640 # size of window's width in pixels
WINDOWHEIGHT = 480 # size of windows' height in pixels
BGCOLOR = (102,205,170)
MOTIONSPEED = 10   #Speed of the moving duck
fpsClock = pygame.time.Clock()

#to render the text
def render_textrect(string, font, rect, text_color, background_color, justification=0):
    """Returns a surface containing the passed text string, reformatted
    to fit within the given rect, word-wrapping as necessary. The text
    will be anti-aliased.

    Takes the following arguments:

    string - the text you wish to render. \n begins a new line.
    font - a Font object
    rect - a rectstyle giving the size of the surface requested.
    text_color - a three-byte tuple of the rgb value of the
                 text color. ex (0, 0, 0) = BLACK
    background_color - a three-byte tuple of the rgb value of the surface.
    justification - 0 (default) left-justified
                    1 horizontally centered
                    2 right-justified

    Returns the following values:

    Success - a surface object with the text rendered onto it.
    Failure - raises a TextRectException if the text won't fit onto the surface.
    """

    import pygame
    
    final_lines = []

    requested_lines = string.splitlines()

    # Create a series of lines that will fit on the provided
    # rectangle.

    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            # if any of our words are too long to fit, return.
            for word in words:
                if font.size(word)[0] >= rect.width:
                    raise TextRectException, "The word " + word + " is too long to fit in the rect passed."
            # Start a new line
            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " "
                # Build the line while the words fit.    
                if font.size(test_line)[0] < rect.width:
                    accumulated_line = test_line 
                else: 
                    final_lines.append(accumulated_line) 
                    accumulated_line = word + " " 
            final_lines.append(accumulated_line)
        else: 
            final_lines.append(requested_line) 

    # Let's try to write the text out on the surface.

    surface = pygame.Surface(rect.size) 
    surface.fill(background_color) 

    accumulated_height = 0 
    for line in final_lines: 
        if accumulated_height + font.size(line)[1] >= rect.height:
            raise TextRectException, "Once word-wrapped, the text string was too tall to fit in the rect."
        if line != "":
            tempsurface = font.render(line, 1, text_color)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulated_height))
            elif justification == 1:
                surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
            elif justification == 2:
                surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
            else:
                raise TextRectException, "Invalid justification argument: " + str(justification)
        accumulated_height += font.size(line)[1]

    return surface


#To keep score
SCORE = 0

#To check if game over
gameLost = False

#Initialize displaysurf
DISPLAYSURF	= pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)

#Duck Things
duck_w = 600/10
duck_h = 540/10
duckImg = pygame.image.load('duck.png')
duckImg = pygame.transform.scale(duckImg, (int(duck_w), int(duck_h)))
movingRight = False
movingLeft = False
movingUp = False

#Speed of duck in y direction
MOTIONSPEED_Y = 8

#Height of duck jump
JUMPHEIGHT = 40

#To see direction of jump
jumpDirection = False

#To see time since game started
time = pygame.time.get_ticks()


#Time after which eggs fall(miliseconds)
egg_delay = 2000

#Y co-ordinate of duck base
BASELINE = 400


#Co-ordinates of the duck

duck_x = 0
duck_y = BASELINE


#To store all the eggs
eggs = []
egg_w = 589/25
egg_h = 800/25

#To store broken eggs
omlets = []


class Omlet(object):

	def __init__(self,x,y):
		self.w = 600/10
		self.h = 303/10
		self.Img = pygame.image.load('broke_egg.png')
		self.Img = pygame.transform.scale(self.Img, (self.w, self.h))
		self.x = x
		self.y = y
		self.time = pygame.time.get_ticks()
		#To check if omlet has turned into a chick
		self.chick_there = 0
		#To see direction of motion
		self.motionDir = "none"
		#Denotes time for which broken egg persists
		self.lag = 1000

	def makeChick(self):
		self.w = 1291/40
		self.h = 2394/40
		self.y = BASELINE
		self.Img = pygame.image.load('chick.png')
		self.Img = pygame.transform.scale(self.Img, (self.w, self.h))

		if duck_x > self.x:
			self.motionDir = "right"
		else:
			self.motionDir = "left"

	def move(self):
		
		if self.motionDir == "right":
			self.x += MOTIONSPEED/2
		else:
			self.x -= MOTIONSPEED/2

	def checkValid(self, chick_there):

		self.chick_there = chick_there

		if pygame.time.get_ticks() > self.time + self.lag and self.motionDir == "none":      
			
			if self.chick_there == 0:
				omlets.remove(self)
			else:
				self.makeChick()
		elif pygame.time.get_ticks() > self.time + self.lag:
			self.move()

	def destroy(self):
		omlets.remove(self)

def Eggbreak(x,y):
	
	omlet = Omlet(x,y)
	omlets.append(omlet)

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

#Things to do when the game starts

def startScreen():

	global myfont

	BGCOLOR = (220,20,60)

	welcome_string = "Welcome to the game\n Hope You enjoy it\n Click any button to continue"
	story_string = "One day mummy duck was walking down the road. Soon the weather turned bad and it started raining. But, it wasn't water, Her eggs were falling!!!"
	controls_string = "-> : Move right\n<- : Move Left\nSPACEBAR: Jump\n(Hint: Dont let the chicks get away)"
	
	welcome = myfont.render(welcome_string, 1, (0,0,128))

 	my_rect = pygame.Rect((40, 40, 300, 300))
 	rendered_text = render_textrect(welcome_string, myfont, my_rect, (216, 216, 216), (48, 48, 48), 0)

	DISPLAYSURF.fill(BGCOLOR)
	DISPLAYSURF.blit(rendered_text, (WINDOWWIDTH/2, WINDOWHEIGHT/2))
	
	pygame.display.update()
	
	event = pygame.event.wait()

	while event.type != KEYDOWN:
		event = pygame.event.wait()

		if event.type == QUIT:
			pygame.quit()
			sys.exit()



#Things after the game is over

def gameOverScreen():
	global myfont

	BGCOLOR = (220,20,60)
	
	
	label = myfont.render("GAME OVER!", 1, (255,255,0))

	text_w, text_h = myfont.size("GAME OVER!")

	DISPLAYSURF.fill(BGCOLOR)
	DISPLAYSURF.blit(label, (WINDOWWIDTH/2 - text_w/2, WINDOWHEIGHT/2 - text_h/2))
	
	score_string = "SCORE: " + str(SCORE)
	score = myfont.render( score_string, 1, (0,0,128))

	score_w, score_h = myfont.size(score_string)

	DISPLAYSURF.blit(score, (WINDOWWIDTH/2 - score_w/2, WINDOWHEIGHT/2 + text_h/2 + 50))


	pygame.display.update()

	pygame.event.wait()
	#pygame.event.wait()
	pygame.quit()
	sys.exit()


def jump():
	global movingUp

	movingUp = True;


startScreen()

while True: 

	DISPLAYSURF.fill(BGCOLOR)
	DISPLAYSURF.blit(duckImg, (duck_x, duck_y))

	#To display score
	score = myfont.render("SCORE: " + str(SCORE), 1, (0,0,128))

	DISPLAYSURF.blit(score, (20, 20))

	#To see if jump is executed

	if movingUp == True:
		
		
		if duck_y >= BASELINE - JUMPHEIGHT and jumpDirection == True:
			duck_y -= MOTIONSPEED_Y
		else:
			duck_y += MOTIONSPEED_Y
			jumpDirection = False


		if duck_y >= BASELINE:
			movingUp = False
			jumpDirection = True
			duck_y = BASELINE

	#To generate randomly falling eggs


	if( pygame.time.get_ticks() >= time + egg_delay):
		time = pygame.time.get_ticks()
		eggs.append(Egg(random.randint(max(duck_x - 50, 10), min(duck_x + 50, WINDOWWIDTH - 10)),egg_h))
		
		#To make game tough <Add code for delay> probably exponential
		#egg_delay -= 100

	#To do with omlets

	for omlet in omlets:
		
		#Pudh 1 if chick should be there and 0 if it shouldnt be there
		omlet.checkValid(1)

		if omlet.x in range(duck_x, duck_x + duck_w) and duck_y < BASELINE and omlet.chick_there == 1:
			SCORE += 50
			omlet.destroy()

		if omlet.x <=0 or omlet.x >= WINDOWWIDTH:
			gameLost = True

		DISPLAYSURF.blit(omlet.Img, (omlet.x, omlet.y))


	#To do with eggs

	for egg in eggs:
		
		if( egg.x in range(duck_x, duck_x + duck_w) and egg.y in range(duck_y, duck_y + duck_h)):
			SCORE += 25
			egg.destroy()

		elif( egg.y >= duck_h + BASELINE):
			SCORE -= 10
			Eggbreak(egg.x,BASELINE + duck_h)
			egg.destroy()

		else:
			DISPLAYSURF.blit(egg.Img, (egg.x, egg.y))
			egg.move()

	#Checking for events

	for event in pygame.event.get():
		
		if event.type == KEYDOWN:

			if event.key == K_LEFT:
				movingLeft = True
			elif event.key == K_RIGHT:
				movingRight = True
			if event.key == K_SPACE:
				jump()

		if event.type == KEYUP:
			
			if event.key in (K_LEFT, K_a):
				movingLeft = False
			elif event.key in (K_RIGHT, K_d):
				movingRight = False 

		if event.type == QUIT:
			pygame.quit()
			sys.exit()		

	#To do if the game has ended
	if gameLost:
		gameOverScreen()


	if movingLeft == True and duck_x - MOTIONSPEED > 0:
		duck_x  -= MOTIONSPEED
	elif movingRight == True and duck_x + MOTIONSPEED < (WINDOWWIDTH- duck_w ):
		duck_x	+= MOTIONSPEED 

	pygame.display.update()
	fpsClock.tick(FPS)