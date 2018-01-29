import pygame
from pygame.locals import *

#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import math
import os

from player import Player
import level1

os.environ['SDL_VIDEO_CENTERED'] = '1'

fullScreen = False
refreshRate = 60	# frames/sec
scale = 4#2#4
playFieldWidth = 320
playFieldHeight = 200
showBlocks = False # Debug option for visualizing blocking objects

windowWidth = playFieldWidth * scale
windowHeight = playFieldHeight * scale


# class UserInput ======================================================================================================

class UserInput:
	def __init__(self):
		self.down = False
		self.up = False
		self.left = False
		self.right = False
		self.space = False

		self.quit = False


# class Game ===========================================================================================================

class Game:
	def __init__(self):
		self.running = True

		pygame.mixer.pre_init(44100, -16, 2, 1024)	# To avoid sound latency mixer should be initialized first
		pygame.mixer.init()
		pygame.init()

		pygame.mouse.set_visible(0)
		fs = 0
		if fullScreen:
			fs = pygame.FULLSCREEN
		# Initialize monitor surface
		self.window = pygame.display.set_mode((windowWidth, windowHeight), pygame.HWSURFACE | pygame.DOUBLEBUF | fs)
		# Initialize offscreen playField
		self.playField = pygame.Surface((playFieldWidth, playFieldHeight), pygame.SRCALPHA)

		pygame.display.set_caption("Escape")
		self.clock = pygame.time.Clock()
		self.running = True

		self.userInput = UserInput()
		self.player = Player(self)

		self.levelList = []
		self.levelList.append(level1.Level01(self))
		self.currentLevel = self.levelList[0]

		self.playFieldWidth = playFieldWidth
		self.playFieldHeight = playFieldHeight

		self.showBlocks = showBlocks

	def UpdateGameState(self):
		self.currentLevel.Update(self.userInput)

	def Render(self):
		self.currentLevel.Draw(self.playField)

		# Draw playField to the monitor surface
		self.window.blit(pygame.transform.scale(self.playField, (windowWidth, windowHeight)), (0, 0))

	def HandleEvent(self, event):
		if event.type == pygame.QUIT:
			self.userInput.quit = True

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_q:
				self.userInput.quit = True

			if event.key == pygame.K_SPACE:
				self.userInput.space = True

			if event.key == pygame.K_LEFT:
				self.userInput.left = True

			if event.key == pygame.K_RIGHT:
				self.userInput.right = True

			if event.key == pygame.K_UP:
				self.userInput.up = True

			if event.key == pygame.K_DOWN:
				self.userInput.down = True

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_SPACE:
				self.userInput.space = False

			if event.key == pygame.K_LEFT:
				self.userInput.left = False

			if event.key == pygame.K_RIGHT:
				self.userInput.right = False

			if event.key == pygame.K_UP:
				self.userInput.up = False

			if event.key == pygame.K_DOWN:
				self.userInput.down = False

	def Cleanup(self):
		pygame.mixer.quit()
		pygame.quit()

	def Execute(self):
		self.running = True

		while self.running:
			for event in pygame.event.get():
				self.HandleEvent(event)
			self.UpdateGameState()
			self.Render()
			pygame.display.flip()
			self.clock.tick(refreshRate)
			if self.userInput.quit:
				self.running = False

		self.Cleanup()

if __name__ == "__main__":
	game = Game()
	game.Execute()
