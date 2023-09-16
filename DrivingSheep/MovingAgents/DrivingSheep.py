import pygame
from pygame.locals import *
import Constants
import random
from Enemy import Enemy
from Player import Player

#initialize pygame
pygame.init()

#setup
clock = pygame.time.Clock();
screen = pygame.display.set_mode((Constants.DISPLAY_WIDTH, Constants.DISPLAY_HEIGHT))
dogImage = pygame.image.load('dog.png')
sheepImage = pygame.image.load('sheep.png')

player = Player(dogImage, pygame.Vector2(Constants.PLAYER_XPOS, Constants.PLAYER_YPOS), (Constants.PLAYER_SIZE), Constants.PLAYER_SPD, Constants.PLAYER_COLOR)
bounds = pygame.Vector2(Constants.DISPLAY_WIDTH, Constants.DISPLAY_HEIGHT)

enemies = []
for i in range (1, Constants.MAX_ENEMIES + 1):
	enemies.append(Enemy(sheepImage, pygame.Vector2(random.randrange(0, bounds.x), random.randrange(0, bounds.y)), Constants.ENEMY_SIZE, Constants.ENEMY_SPD, Constants.ENEMY_COLOR))

#main gameplay loop
hasQuit = False
while not hasQuit:

	# event handler
	for event in pygame.event.get():

		#quit the game
		if event.type == QUIT:
			hasQuit = True
				
	#make screen cornflower blue
	screen.fill(Constants.BACKGROUND_COLOR)
	
	#update the agents
	player.update(bounds, enemies)
	for enemy in enemies:
		enemy.update(bounds, player)

	#draw the agents
	player.draw(screen)
	for enemy in enemies:
		enemy.draw(screen)

	#detect player-enemy tag
	if player.isInCollision(enemy):
		enemies.remove(enemy)
	
	#flip display buffer
	pygame.display.flip()

	#constrain to 60 fps
	clock.tick(60)

#quit the game
pygame.quit()
quit()