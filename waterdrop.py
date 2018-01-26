#!/usr/bin/python
# -*- coding: utf-8 -*-

# waterdrop.py

import pygame
from pygame.locals import *

class WaterDrop(pygame.sprite.Sprite):
	fileImage = None
	width, height = 0, 0
	phaseCount = 6
	sound = None

	VAccel = 0.00029 #26.0 / (300.0 * 300.0)

	def __init__(self, xPos, topPos, bottomPos):
		pygame.sprite.Sprite.__init__(self)
		if WaterDrop.fileImage == None:
			WaterDrop.fileImage = pygame.image.load("images/WaterDrop.png").convert_alpha()
			WaterDrop.width, WaterDrop.height = WaterDrop.fileImage.get_size()

			WaterDrop.tileSizeX = WaterDrop.width / WaterDrop.phaseCount
			WaterDrop.tileSizeY = WaterDrop.height

		if WaterDrop.sound == None:
			WaterDrop.sound = pygame.mixer.Sound ("sounds/WaterDrop.ogg")

		self.ticks = pygame.time.get_ticks()
		self.x0 = xPos
		self.y0 = topPos + WaterDrop.height
		self.t0 = self.ticks
		self.hitPos = bottomPos

		self.phaseIndex = 0
		self.phaseUpdateTime = 200 # ms

		self.hit = False

		self.rect = pygame.Rect(self.x0 - WaterDrop.width / 2, self.y0 - WaterDrop.height, WaterDrop.width, WaterDrop.height)
		self.image = WaterDrop.fileImage.subsurface(0, 0, WaterDrop.tileSizeX, WaterDrop.tileSizeY)

	def GetPosition(self):
		return self.rect.centerx, self.rect.bottom

	def CalcVerticalPos(self, t, t0):
		dt = t - t0
		yt = self.y0 + WaterDrop.VAccel * dt * dt
		return yt

	def update(self):
		currentTicks = pygame.time.get_ticks()

		if not self.hit:
			y = self.CalcVerticalPos(currentTicks, self.t0)
			x, bottomPos = self.GetPosition()
			dy = y - bottomPos
			if dy < 1.0:
				return

			if y >= self.hitPos:
				y = self.hitPos
				self.hit = True
				WaterDrop.sound.play ()

			self.rect.move_ip(0, dy)

		if currentTicks > self.ticks + self.phaseUpdateTime:
			self.ticks = currentTicks

			if self.hit:
				if self.phaseIndex < 3:
					self.phaseIndex = 3
				elif self.phaseIndex == 3:
					self.phaseIndex = 4
				elif self.phaseIndex == 4:
					self.phaseIndex = 5
				elif self.phaseIndex == 5:
					self.kill ()
			else:
				self.phaseIndex += 1
				if self.phaseIndex >= 3:
					self.phaseIndex = 0

		rc = pygame.Rect(self.phaseIndex * WaterDrop.tileSizeX, 0, WaterDrop.tileSizeX, WaterDrop.tileSizeY)
		self.image = WaterDrop.fileImage.subsurface(rc)






