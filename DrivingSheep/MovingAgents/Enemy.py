from dis import dis
import pygame
from pygame.locals import *
import random
import math
import Constants
from Agent import Agent

class Sheep(Agent):

	def __init__(self, image, pos, size, spd, color, turnSpd):
		super().__init__(image, pos, size, spd, color, turnSpd)
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

	def update(self, bounds, screen, player):

		if pygame.Vector2.length(self.vel) == 0:
			angle = math.acos(random.randrange(-1, 1))
			self.vel = pygame.Vector2(math.cos(angle), math.sin(angle))
		
		self.isFleeing = self.isPlayerClose(player)

		boundsForce = self.computeBoundaryForces(bounds, screen)

		# wander if player isn't close
		if not self.isFleeing:
			rotationAngle = random.randrange(-1, 1)
			theta = math.acos(rotationAngle)

			pickTurn = random.randint(0, 100)
			if pickTurn < 50:
				theta += 0
			else:
				theta += 180

			#apply wander force			
			wanderDir = pygame.Vector2.normalize(self.pos)
			wanderDirForce = wanderDir * Constants.ENEMY_WANDER_FORCE
			wanderDirForceNorm = pygame.Vector2.normalize(wanderDirForce)
			#pygame.Vector2.scale_to_length(wanderDirForceNorm, Constants.DELTATIME * self.spd)

			totalForce = wanderDirForceNorm + boundsForce

			#self.vel.x += (math.cos(theta) - math.sin(theta)) * wanderDirForceNorm.x
			#self.vel.y += (math.sin(theta) - math.cos(theta)) * wanderDirForceNorm.y

		# otherwise, flee
		else:
			#apply flee force
			#store the calculated, normalized direction to the dog
			dirToDog = pygame.Vector2.normalize(player.pos - self.pos)

			#scale direction by the weight of this force to get applied force and store it
			dirToDogForce = -dirToDog * Constants.ENEMY_FLEE_FORCE

			#take applied force, normalize it, scale it by deltatime and speed to modify sheep's velocity
			dirToDogForceNorm = pygame.Vector2.normalize(dirToDogForce)
			#pygame.Vector2.scale_to_length(dirToDogForceNorm, Constants.DELTATIME * self.spd)
			
			totalForce = dirToDogForceNorm + boundsForce

			self.calcTrackingVelocity(player)
			

		self.clampTurn(Constants.ENEMY_TURN_SPEED, totalForce)

		super().update(bounds, screen)

	def draw(self, screen):
		if self.isFleeing == True:
			pygame.draw.line(screen, (0, 0, 255), self.center, self.targetPos, 3)

		super().draw(screen)
