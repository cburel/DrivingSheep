from asyncio.windows_events import NULL
from typing import List
import pygame
from pygame.locals import *
from Agent import Agent

#setup
clock = pygame.time.Clock();


class Dog(Agent):

	def __init__(self, image, pos, size, spd, color):
		super().__init__(image, pos, size, spd, color)
		self.targetAgent = NULL

	def update(self, bounds, enemies: List):
		# gets nearest enemy and moves player towards it
		# shoutout to Rabbid76 on SO for the basics on this next line

		if len(enemies) != 0:
			self.targetAgent = min([e for e in enemies], key=lambda e: self.pos.distance_to(pygame.math.Vector2(e.pos.x, e.pos.y)))

			self.vel = self.targetAgent.pos - self.pos
			
			super().updateVelocity(self.vel)
			super().update(bounds)

		return self.targetAgent