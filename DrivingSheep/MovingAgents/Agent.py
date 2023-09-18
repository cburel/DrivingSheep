from asyncio import constants
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
		return pygame.Rect(self.pos, self.size)

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
		
		#draw the rectangle
		pygame.draw.rect(screen, self.color, self.rect)
				
		#draw black debug collision rect border
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

		#draw line representing each boundary force when it is applied from the boundary to the agent.
		#pygame.draw.line(screen, (0, 0, 255), boundsForce, self.center)

		#screen.blit(self.surf, [self.upperLeft.x, self.upperLeft.y])

	def computeBoundaryForces(self, bounds, screen):	
		boundsNearbyList = []
		boundsForce = pygame.Vector2(0,0)
		boundsSum = pygame.Vector2(0,0)

		#for each boundary agent is near, add boundary's normal force to list, compute force pushing away from boundary. add this force to a sum.
		if self.center.x < Constants.BORDER_RADIUS:
			boundsNearby = pygame.Vector2(0, self.center.y)
			boundsForce = pygame.Vector2(Constants.BORDER_RADIUS, 0) - (self.center - boundsNearby)
			boundsSum += boundsForce
			boundsNearbyList.append(boundsNearby)
		elif self.center.x > bounds.x - Constants.BORDER_RADIUS:
			boundsNearby = pygame.Vector2(bounds.x, self.center.y)
			boundsForce = (pygame.Vector2(Constants.BORDER_RADIUS, 0) + (self.center - boundsNearby)) * -1
			boundsSum += boundsForce
			boundsNearbyList.append(boundsNearby)

		if self.center.y < Constants.BORDER_RADIUS:
			boundsNearby = pygame.Vector2(self.center.x, 0)
			boundsForce = pygame.Vector2(0, Constants.BORDER_RADIUS) - (self.center - boundsNearby)
			boundsSum += boundsForce
			boundsNearbyList.append(boundsNearby)
		elif self.center.y > bounds.y - Constants.BORDER_RADIUS:
			boundsNearby = pygame.Vector2(self.center.x, bounds.y)
			boundsForce = (pygame.Vector2(0, Constants.BORDER_RADIUS) + (self.center - boundsNearby)) * -1
			boundsSum += boundsForce
			boundsNearbyList.append(boundsNearby)

		#scale total boundary force by the weight
		if boundsSum != pygame.Vector2(0,0):
			pygame.Vector2.scale_to_length(boundsSum, Constants.DELTATIME * 1000 * self.spd)

		#add scaled boundary force to applied force we have before (seek, flee, wander)
		self.vel += boundsSum

		#normalize applied force, scale by dt, and modify agent velocity
		#self.vel += pygame.Vector2.normalize(self.vel) * Constants.DELTATIME

		#draw a force line between boundary and agent
		if len(boundsNearbyList) > 0:
			for bound in boundsNearbyList:
				pygame.draw.line(screen, (255, 0, 0), self.center, bound, 1)
		
	#update the agent
	def update(self, bounds, screen):

		#move the agent
		self.pos += pygame.Vector2.normalize(self.vel) * self.spd
		
		# ensure agent stays within the world
		self.computeBoundaryForces(bounds, screen)		

		# update agent's position
		self.rect = self.updateRect()
		self.center = self.updateCenter()


			