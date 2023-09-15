from turtle import Vec2D
import pygame
from pygame.locals import *
import Constants

class Agent():
	def __init__(self, pos, size, spd, color):
		self.pos = pos
		self.size = pygame.Vector2(size, size)
		self.spd = spd
		self.color = color
		self.vel = pygame.Vector2(0,0)
		self.target = 0
		self.center = self.updateCenter()
		self.rect = self.updateRect()

	#pretty print agent information
	def __str__(self):
		return ("Size: " +  str(self.size) + ", " + "Pos: " + str(self.pos) + ", " + "Vel: " + str(self.vel) + ", " + "Center: " + str(self.center))

	def updateVelocity(self, velocity):
		velocity = pygame.Vector2.normalize(velocity)

	# calculate the center of the agent's rect
	def updateCenter(self):
		return pygame.Vector2(self.pos.x + self.size / 2, self.pos.y + self.size / 2)

	def updateCenter(self):
		self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size, self.size)

	# check for collision with another agent
	def isInCollision(self, agent):

		if agent != None:
			# if collision is detected, execute collision 
			if self.rect.colliderect(agent.rect):
				return True

		return False

	def draw(self, screen):

		#draw the rectangle
		pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x, self.pos.y, self.size, self.size))
		self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size, self.size)
		
		#draw debug collision rect border
		pygame.draw.rect(screen, (0,0,0), self.rect, 1)

		# draw debug line
		lineStart = self.calcCenter()
		scaledVel = pygame.Vector2(self.vel.x, self.vel.y)
		
		if self.vel == (0,0):
			scaledVel = self.vel
		else:
			pygame.Vector2.scale_to_length(scaledVel, self.size)
		
		lineEnd = pygame.Vector2(self.calcCenter().x + scaledVel.x, self.calcCenter().y + scaledVel.y)
		pygame.draw.line(screen, (0, 0, 255), lineStart, lineEnd, 3)

	def update(self, bounds):

		#move the agent and its collision rect
		self.pos += pygame.Vector2.normalize(self.vel) * self.spd
		self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size, self.size)

		#keep agent in bounds of world and make them move off borders a little nicer
		if self.pos.x <= 0:
			self.pos.x = Constants.BORDER_RADIUS + self.size
			self.vel.x = -self.vel.x
		if self.pos.x >= Constants.DISPLAY_WIDTH:
			self.pos.x = Constants.DISPLAY_WIDTH - Constants.BORDER_RADIUS - self.size
			self.vel.x = -self.vel.x
		if self.pos.y <= 0:
			self.pos.y = Constants.BORDER_RADIUS + self.size
			self.vel.y = -self.vel.y
		if self.pos.y >= Constants.DISPLAY_HEIGHT:
			self.pos.y = Constants.DISPLAY_HEIGHT - Constants.BORDER_RADIUS - self.size
			self.vel.y = -self.vel.y

		self.updateRect()
		self.updateCenter()


			