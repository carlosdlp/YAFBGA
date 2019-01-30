import pygame
import numpy as np
import math
import random
import settings
from NN import *

settings.init() 

class Bird:
	def __init__(self):
		self.pos = np.array([50,int(settings.height/2)])
		self.r = 7
		self.g = settings.gravity
		self.j = settings.jump
		self.v = 0
		self.Dtop = 0
		self.Dbottom = 0
		self.score = 0
		self.best = False

		self.brain = NeuralNetwork(4,[2,3],1)

	def show(self,screen, color):
		pygame.draw.circle(screen,color,self.pos,self.r,0)

	def update(self):
		self.v = self.v + self.g
		self.pos[1] = self.pos[1] + self.v
		self.score = self.score +  1


	def jump(self):
		self.v = 0
		self.v = self.v + self.j

	def think(self):
		action = self.brain.predict([self.pos[1]/settings.height,self.v/10,self.Dtop/100,self.Dbottom/100])
		if action[0] > 0.5:
			self.jump()

	def calcDist(self, pipe):
		top = math.sqrt((self.pos[0] - pipe.x)**2 + (self.pos[1] - pipe.y)**2)
		bottom = math.sqrt((self.pos[0] - pipe.x)**2 + (self.pos[1] - pipe.y+80)**2)

		self.Dtop = top
		self.Dbottom = bottom


class Pipe:
	def __init__(self):
		self.x = settings.width-30
		self.y = random.randint(int(settings.height / 6), int(3 / 4 * settings.height))
		self.v = -3

	def show(self,screen,color):
		pygame.draw.rect(screen, color, pygame.Rect(self.x, 0, 30, self.y))
		pygame.draw.rect(screen, color, pygame.Rect(self.x, self.y+80, 30, settings.height-self.y-80))

	def update(self):
		self.x = self.x + self.v


