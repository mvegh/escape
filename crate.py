#!/usr/bin/python
# -*- coding: utf-8 -*-

# crate.py

import pygame
from pygame.locals import *

class Crate(pygame.sprite.Sprite):
	fileImage = None
	width, height = 0, 0

	def __init__(self, xPos, yPos, blockList):
		pygame.sprite.Sprite.__init__(self)
		if Crate.fileImage == None:
			Crate.fileImage = pygame.image.load("images/Crate.png").convert_alpha()
			Crate.width, Crate.height = Crate.fileImage.get_size()

		self.xPos = xPos
		self.yPos = yPos
		self.rect = pygame.Rect(self.xPos, self.yPos, Crate.width, Crate.height)
		self.image = Crate.fileImage.subsurface(0, 0, Crate.width, Crate.height)

		blockList.append(self.rect)

	def update(self):
		pass

