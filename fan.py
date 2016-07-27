#!/usr/bin/python
# -*- coding: utf-8 -*-

# fan.py

import pygame
from pygame.locals import *

class Fan (pygame.sprite.Sprite):
	fileImage = None
	width, height = 0, 0
	phaseCount = 4

	def __init__ (self, xPos, yPos, updateTime, direction):
		pygame.sprite.Sprite.__init__(self)
		if Fan.fileImage == None:
			Fan.fileImage = pygame.image.load ("images/Fan.png").convert_alpha ()
			Fan.width, Fan.height = Fan.fileImage.get_size ()

			Fan.tileSizeX = Fan.width / Fan.phaseCount
			Fan.tileSizeY = Fan.height

		self.xPos = xPos
		self.yPos = yPos
		self.rect = pygame.Rect (self.xPos, self.yPos, Fan.tileSizeX, Fan.tileSizeY)
		self.image = Fan.fileImage.subsurface (0, 0, Fan.tileSizeX, Fan.tileSizeY)

		self.phaseIndex = 0
		self.ticks = pygame.time.get_ticks ()

		self.direction = direction
		self.updateTime = updateTime	# ms

	def SetDirection (self, direction):
		self.direction = direction

	def SetUpdateTime (self, updateTime):
		self.updateTime = updateTime	# ms

	def update (self):
		currentTicks = pygame.time.get_ticks ()
		if currentTicks > self.ticks + self.updateTime:
			self.ticks = currentTicks

			if self.direction > 0:
				self.phaseIndex += 1
				if self.phaseIndex >= Fan.phaseCount:
					self.phaseIndex = 0
			elif self.direction < 0:
				self.phaseIndex -= 1
				if self.phaseIndex < 0:
					self.phaseIndex = Fan.phaseCount - 1

			rc = pygame.Rect (self.phaseIndex * Fan.tileSizeX, 0, Fan.tileSizeX, Fan.tileSizeY)
			self.image = Fan.fileImage.subsurface (rc)

