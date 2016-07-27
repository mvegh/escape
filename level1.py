#!/usr/bin/python
# -*- coding: utf-8 -*-

# level1.py

import pygame
from pygame.locals import *

import random
import math
import os

from crate import Crate
from fan import Fan
from level import Level
from player import Player
from room import Room
from steelplatform import SteelPlatform
from stone import Stone
from wastebin import WasteBin


# class Room00 =========================================================================================================

class Room00 (Room):
	def __init__ (self, game):
		Room.__init__ (self, game)
		self.LoadBgImage ("images/R00.bgnd.png")

		# Ventillation
		self.fan = Fan (self.xOffs + 162, self.yOffs + 20, 50, 1)
		self.bgSpriteGroup.add (self.fan)

		# Crate
		self.crate = Crate (self.xOffs + 134, self.yOffs + 57, self.blockList)
		self.bgSpriteGroup.add (self.crate)

		# Lower platform
		w = self.game.playField.get_width () + 20
		h = self.roomHeight - 81
		self.bottomPlatformRect = pygame.Rect (-10, self.yOffs + 81, w, h)
		self.blockList.append (self.bottomPlatformRect)

		# Ceiling
		w = self.game.playField.get_width () + 20
		h = 2
		self.ceilingRect = pygame.Rect (-10, self.yOffs + 0, w, h)
		self.blockList.append (self.ceilingRect)

		# SteelPlatform
		self.steelplatform = SteelPlatform (self.xOffs + 224, self.yOffs + 72, self.blockList, self.game.player)
		self.bgSpriteGroup.add (self.steelplatform)

		self.spriteGroup.add (self.game.player)

	def Enter (self, position):
		Room.Enter (self, position)
		if position == 'L':
			self.game.player.SetLeftPos (self.xOffs)
			self.game.player.SetBottomPos (self.bottomPlatformRect.top)
		elif position == 'R':
			self.game.player.SetLeftPos (self.xOffs + self.roomWidth - 15)
			self.game.player.SetBottomPos (self.bottomPlatformRect.top)

	def Update (self, userInput):
		Room.Update (self, userInput)

		if self.game.player.rect.right < self.xOffs + 10:
			self.game.player.SetRightPos (self.xOffs + 10)
		elif self.game.player.rect.left >= self.xOffs + self.roomWidth - 10:
			self.game.currentLevel.SetCurrentRoom (1, 'L')

	def Draw (self, screen):
		Room.Draw (self, screen)


# class Room01 =========================================================================================================

class Room01 (Room):
	def __init__ (self, game):
		Room.__init__ (self, game)
		self.LoadBgImage ("images/R01.bgnd.png")

		#self.blockList.append (pygame.Rect ((left, top), (width, height)))

		self.fan = Fan (self.xOffs + 235, self.yOffs + 21, 180, -1)
		self.bgSpriteGroup.add (self.fan)
		self.spriteGroup.add (self.game.player)

		self.wasteBin = WasteBin (self.xOffs + 24, self.yOffs + 69)
		self.fgSpriteGroup.add (self.wasteBin)

		# Stone
		self.stone = Stone (self.xOffs + 184, self.yOffs + 72, self.blockList, self.game.player)
		self.bgSpriteGroup.add (self.stone)

		# Stairs
		self.s0Rect = pygame.Rect (self.xOffs + 0, self.yOffs + 112, 252, 119 - 112)
		self.blockList.append (self.s0Rect)

		self.s1Rect = pygame.Rect (self.xOffs + 0, self.yOffs + 104, 243, 112 - 104)
		self.blockList.append (self.s1Rect)

		self.s2Rect = pygame.Rect (self.xOffs + 0, self.yOffs + 97, 237, 104 - 97)
		self.blockList.append (self.s2Rect)

		self.s3Rect = pygame.Rect (self.xOffs + 0, self.yOffs + 90, 230, 97 - 90)
		self.blockList.append (self.s3Rect)

		self.s4Rect = pygame.Rect (self.xOffs + 0, self.yOffs + 81, 222, 90 - 81)
		self.blockList.append (self.s4Rect)

		# Lower platform
		self.bottomPlatformRect = pygame.Rect (self.xOffs + 0, self.yOffs + 119, self.roomWidth, self.roomHeight - 119)
		self.blockList.append (self.bottomPlatformRect)

		# Ceiling
		w = self.game.playField.get_width () + 20
		h = 2
		self.ceilingRect = pygame.Rect (-10, self.yOffs + 0, w, h)
		self.blockList.append (self.ceilingRect)

	def Enter (self, position):
		Room.Enter (self, position)
		if position == 'L':
			self.game.player.SetRightPos (self.xOffs + 15)
			self.game.player.SetBottomPos (self.s4Rect.top)
		elif position == 'R':
			self.game.player.SetLeftPos (self.xOffs + self.roomWidth - 15)
			self.game.player.SetBottomPos (self.bottomPlatformRect.top)

	def Update (self, userInput):
		Room.Update (self, userInput)
		if self.game.player.rect.right <= self.xOffs + 10:
			self.game.currentLevel.SetCurrentRoom (0, 'R')
		elif self.game.player.rect.left >= self.xOffs + self.roomWidth - 10:
			self.game.currentLevel.SetCurrentRoom (2, 'L')

	def Draw (self, screen):
		Room.Draw (self, screen)


# class Room02 =========================================================================================================

class Room02 (Room):
	def __init__ (self, game):
		Room.__init__ (self, game)
		self.LoadBgImage ("images/R02.bgnd.png")
		self.spriteGroup.add (self.game.player)

		# Lower platform
		self.bottomPlatformRect = pygame.Rect (self.xOffs + 0, self.yOffs + 120, self.roomWidth, self.roomHeight - 120)
		self.blockList.append (self.bottomPlatformRect)

		# Test blocks
		for n in range (0, 10):
			rc = pygame.Rect (self.xOffs + 80 + 4 * n, self.yOffs + 120 - n, 30, 1)
			self.blockList.append (rc)


	def Enter (self, position):
		Room.Enter (self, position)
		if position == 'L':
			self.game.player.SetRightPos (self.xOffs + 15)
		elif position == 'R':
			self.game.player.SetLeftPos (self.xOffs + self.roomWidth - 15)
		self.game.player.SetBottomPos (self.bottomPlatformRect.top)

	def Update (self, userInput):
		Room.Update (self, self.game.userInput)
		if self.game.player.rect.right <= self.xOffs + 10:
			self.game.currentLevel.SetCurrentRoom (1, 'R')
		elif self.game.player.rect.left > self.xOffs + self.roomWidth - 10:
			self.game.player.SetLeftPos (self.xOffs + self.roomWidth - 10)

	def Draw (self, screen):
		Room.Draw (self, screen)


# class Level01 ========================================================================================================

class Level01 (Level):
	def __init__(self, game):
		Level.__init__ (self, game)
		self.roomList.append (Room00 (game))
		self.roomList.append (Room01 (game))
		self.roomList.append (Room02 (game))

		self.SetCurrentRoom (0, 'L')
