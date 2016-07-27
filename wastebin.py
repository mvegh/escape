#!/usr/bin/python
# -*- coding: utf-8 -*-

# wastebin.py

import pygame
from pygame.locals import *

class WasteBin (pygame.sprite.Sprite):
	fileImage = None
	width, height = 0, 0

	def __init__ (self, xPos, yPos):
		pygame.sprite.Sprite.__init__(self)
		if WasteBin.fileImage == None:
			WasteBin.fileImage = pygame.image.load ("images/WasteBin.png").convert_alpha ()
			WasteBin.width, WasteBin.height = WasteBin.fileImage.get_size ()

		self.xPos = xPos
		self.yPos = yPos
		self.rect = pygame.Rect (self.xPos, self.yPos, WasteBin.width, WasteBin.height)
		self.image = WasteBin.fileImage.subsurface (0, 0, WasteBin.width, WasteBin.height)

	def update (self):
		pass

