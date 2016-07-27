#!/usr/bin/python
# -*- coding: utf-8 -*-

# room.py

import pygame
from pygame.locals import *


# class Room ===========================================================================================================

class Room:
	def __init__ (self, game):
		self.game = game
		self.roomIsChanged = False

		self.roomWidth = 0
		self.roomHeight = 0
		self.xOffs = 0
		self.yOffs = 0
		self.bgnd = None
		self.blockList = []

		self.bgSpriteGroup = pygame.sprite.Group ()
		self.spriteGroup = pygame.sprite.Group ()
		self.fgSpriteGroup = pygame.sprite.Group ()

	def LoadBgImage (self, imagePath):
		self.bgnd = pygame.image.load (imagePath).convert_alpha ()
		self.roomWidth = self.bgnd.get_width ()
		self.roomHeight = self.bgnd.get_height ()
		self.xOffs = (self.game.playField.get_width () - self.roomWidth) / 2
		self.yOffs = (self.game.playField.get_height () - self.roomHeight) / 2

	def Enter (self, position):
		pass

	def Update (self, userInput):
		self.bgSpriteGroup.update ();
		self.spriteGroup.update ();
		self.fgSpriteGroup.update ();

	def Draw (self, screen):
		if self.roomIsChanged:
			self.roomIsChanged = False
			black = (0, 0, 0)
			screen.fill (black)

		if (self.bgnd != None):
			screen.blit (self.bgnd, (self.xOffs, self.yOffs))
		self.bgSpriteGroup.draw (screen)
		self.spriteGroup.draw (screen)
		self.fgSpriteGroup.draw (screen)

# ===== Visualize blocking rectangles ================================================================================
#		color = Color (255, 0, 0, 92)
#		alphaSurface = pygame.Surface ((self.roomWidth, self.roomHeight), pygame.SRCALPHA)
#		for rect in self.blockList:
#			rc = rect.copy ()
#			rc.move_ip (-self.xOffs, -self.yOffs)
#			alphaSurface.fill (color, rc)
#		screen.blit (alphaSurface, (self.xOffs, self.yOffs))
# ======================================================================================================================
