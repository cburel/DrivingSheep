import pygame
from pygame.locals import *
import Constants

class Agent():
	def __init__(self, image, pos, size, spd, color):
		self.image = image
		self.pos = pos
		self.size = pygame.Vector2(size, size)
		self.spd = spd
		self.color = color
		self.angle = 0
		self.vel = pygame.Vector2(0,0)
		self.target = 0
		self.center = self.updateCenter()
		self.rect = self.updateRect()
		self.calcSurface()

	#pretty print agent information
	def __str__(self):
		return ("Size: " +  str(self.size) + ", " + "Pos: " + str(self.pos) + ", " + "Vel: " + str(self.vel) + ", " + "Center: " + str(self.center))

	def updateVelocity(self, velocity):
		self.vel = pygame.Vector2.normalize(velocity)

	# calculate the center of the agent's rect
	def updateCenter(self):
		return pygame.Vector2(self.pos.x + self.size.x / 2, self.pos.y + self.size.y / 2)

	# calculate the collision rect
	def updateRect(self):
		return pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)

	#calculate agent's surface and rect
	def calcSurface(self):
		self.surf = pygame.transform.rotate(self.image, self.angle)
		self.upperLeft = self.center - pygame.Vector2(self.surf.get_width(), self.surf.get_height()/2)
		self.boundingRect = self.surf.get_bounding_rect().move(self.upperLeft.x, self.upperLeft.y)

	# check for collision with another agent
	def isInCollision(self, agent):
		if agent != None:
			if self.rect.colliderect(agent.rect):
				print("collision!")
				return True
			else:
				return False

	# draw the agent
	def draw(self, screen):

		#update rect position
		self.rect = self.updateRect()

		#draw the rectangle
		pygame.draw.rect(screen, self.color, self.rect)
		
		#draw debug collision rect border
		pygame.draw.rect(screen, (0,0,0), self.rect, 1)

		# draw debug line
		lineStart = self.updateCenter()
		scaledVel = pygame.Vector2(self.vel.x, self.vel.y)
		
		if self.vel == (0,0):
			scaledVel = self.vel
		else:
			pygame.Vector2.scale_to_length(scaledVel, Constants.VECTOR_LINE_LENGTH)
		
		lineEnd = pygame.Vector2(self.updateCenter().x + scaledVel.x, self.updateCenter().y + scaledVel.y)
		pygame.draw.line(screen, (0, 0, 255), lineStart, lineEnd, 3)

		#screen.blit(self.surf, [self.upperLeft.x, self.upperLeft.y])

	#update the agent
	def update(self, bounds):

		#move the agent
		self.pos += pygame.Vector2.normalize(self.vel) * self.spd		
		self.rect = self.updateRect()
		self.center = self.updateCenter()

		#keep agent in bounds of world
		if self.pos.x <= 0:
			self.pos.x = Constants.BORDER_RADIUS + self.size.x
			self.vel.x = -self.vel.x
		if self.pos.x >= bounds.x:
			self.pos.x = bounds.x - Constants.BORDER_RADIUS - self.size.x
			self.vel.x = -self.vel.x
		if self.pos.y <= 0:
			self.pos.y = Constants.BORDER_RADIUS + self.size.y
			self.vel.y = -self.vel.y
		if self.pos.y >= bounds.y:
			self.pos.y = bounds.y - Constants.BORDER_RADIUS - self.size.y
			self.vel.y = -self.vel.y


			