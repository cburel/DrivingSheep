from dis import dis
import pygame
from pygame.locals import *
import random
import math
import Constants
from Agent import Agent

class Enemy(Agent):

	def __init__(self, image, pos, size, spd, color):
		super().__init__(image, pos, size, spd, color)
		self.isFleeing = False
		self.targetPos = None
	
	def switchMode(self):
		if self.isFleeing:
			self.isFleeing = False
		else:
			self.isFleeing = True

	def isPlayerClose(self, player):
		distance = self.pos - player.pos
		if distance.length() < Constants.FLEE_RANGE:
			self.isFleeing = True
			return True
		else:
			self.isFleeing = False
			return False

	def calcTrackingVelocity(self, player):
		self.targetPos = player.center

	def update(self, bounds, player):
		
		# flee if player is close enough
		isFleeing = self.isPlayerClose(player)
		if isFleeing:
			self.vel = pygame.Vector2.normalize(self.pos - player.pos)
			self.calcTrackingVelocity(player)

		# otherwise, wander
		else:
			rotationAngle = random.randrange(-1, 1)
			theta = math.acos(rotationAngle)

			pickTurn = random.randint(0, 100)
			if pickTurn < 50:
				theta += 0
			else:
				theta += 180

			self.vel.x += math.cos(theta) - math.sin(theta)
			self.vel.y += math.sin(theta) - math.cos(theta)

		super().update(bounds)

	def draw(self, screen):
		if self.isFleeing == True:
			pygame.draw.line(screen, (0, 0, 255), self.center, self.targetPos, 3)

		super().draw(screen)
