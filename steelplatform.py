#!/usr/bin/python
# -*- coding: utf-8 -*-

# steelplatform.py

import pygame
from pygame.locals import *

class SteelPlatform (pygame.sprite.Sprite):
	fileImage = None
	width, height = 0, 0

	def __init__ (self, xPos, yPos, blockList, player):
		pygame.sprite.Sprite.__init__(self)
		if SteelPlatform.fileImage == None:
			SteelPlatform.fileImage = pygame.image.load ("images/SteelPlatform.png").convert_alpha ()
			SteelPlatform.width, SteelPlatform.height = SteelPlatform.fileImage.get_size ()

		self.xPos = xPos
		self.yPos = yPos
		self.rect = pygame.Rect (self.xPos, self.yPos, SteelPlatform.width, SteelPlatform.height)
		self.image = SteelPlatform.fileImage.subsurface (0, 0, SteelPlatform.width, SteelPlatform.height)

		blockList.append (self.rect)

		self.player = player

		self.ticks = pygame.time.get_ticks ()
		self.updateTime = 16	# ms
		self.dy = +1

	def update (self):
		currentTicks = pygame.time.get_ticks ()
		if currentTicks > self.ticks + self.updateTime:
			self.ticks = currentTicks

			playerRect = self.player.GetCollideRect ()

			# Check if player is on the stone
			rc = self.rect.copy ()
			rc.move_ip (0, -1)
			playerIsOnThePlatform = rc.colliderect (playerRect)

			if self.dy > 0:
				if self.rect.top > self.yPos + 10:
					self.dy = -1
					self.updateTime = 50
			elif self.dy < 0:
				if self.rect.top < self.yPos - 20:
					self.dy = +1
					self.updateTime = 16

			self.rect.move_ip (0, self.dy)

			# Move player with the platform
			if playerIsOnThePlatform:
				self.player.Move (0, self.dy)

			# Adjust player position on collision due to vertical movement
			if self.rect.colliderect (playerRect):
				if playerRect.bottom > self.rect.top and playerRect.top < self.rect.top:
					self.player.Move (0, playerRect.bottom - self.rect.top)
