#!/usr/bin/python
# -*- coding: utf-8 -*-

# stone.py

import pygame
from pygame.locals import *

class Stone (pygame.sprite.Sprite):
	fileImage = None
	width, height = 0, 0

	def __init__ (self, xPos, yPos, blockList, player):
		pygame.sprite.Sprite.__init__(self)
		if Stone.fileImage == None:
			Stone.fileImage = pygame.image.load ("images/Stone.png").convert_alpha ()
			Stone.width, Stone.height = Stone.fileImage.get_size ()

		self.xPos = xPos
		self.yPos = yPos
		self.rect = pygame.Rect (self.xPos, self.yPos, Stone.width, Stone.height)
		self.image = Stone.fileImage.subsurface (0, 0, Stone.width, Stone.height)

		blockList.append (self.rect)

		self.player = player

		self.ticks = pygame.time.get_ticks ()
		self.updateTime = 60	# ms
		self.dx = +1

	def update (self):
		currentTicks = pygame.time.get_ticks ()
		if currentTicks > self.ticks + self.updateTime:
			self.ticks = currentTicks

			playerRect = self.player.GetCollideRect ()

			# Check if player is on the stone
			rc = self.rect.copy ()
			rc.move_ip (0, -1)
			playerIsOnStone = rc.colliderect (playerRect)

			if self.dx > 0:
				if self.rect.centerx > self.xPos + 40:
					self.dx = -1
					self.updateTime = 30	# ms
			elif self.dx < 0:
				if self.rect.centerx < self.xPos - 30:
					self.dx = +1
					self.updateTime = 60	# ms

			self.rect.move_ip (self.dx, 0)

			# Move player with stone
			if playerIsOnStone:
				self.player.Move (self.dx, 0)

			# Adjust player position on collision
			if self.rect.colliderect (playerRect):
				if playerRect.right > self.rect.left and playerRect.left < self.rect.left:
					self.player.Move (self.rect.left - playerRect.right, 0)

				if playerRect.left < self.rect.right and playerRect.right > self.rect.right:
					self.player.Move (self.rect.right - playerRect.left, 0)
