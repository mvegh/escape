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
from waterdrop import WaterDrop


# class Room00 =========================================================================================================

class Room00(Room):
	def __init__(self, game):
		Room.__init__(self, game)
		self.LoadBgImage("images/R00.bgnd.png")

		# Ventillation
		self.fan = Fan(self.xOffs + 165, self.yOffs + 16, 50, 1)
		self.bgSpriteGroup.add(self.fan)

		# Crate
		self.crate = Crate(self.xOffs + 134, self.yOffs + 57, self.blockList)
		self.bgSpriteGroup.add(self.crate)

		# Lower platform
		w = self.game.playField.get_width() + 20
		h = self.roomHeight - 81
		self.bottomPlatformRect = pygame.Rect(-10, self.yOffs + 81, w, h)
		self.blockList.append(self.bottomPlatformRect)

		# Ceiling
		w = self.game.playField.get_width() + 20
		h = 2
		self.ceilingRect = pygame.Rect(-10, self.yOffs + 0, w, h)
		self.blockList.append(self.ceilingRect)

		# SteelPlatform
		self.steelplatform = SteelPlatform(self.xOffs + 224, self.yOffs + 72, self.blockList, self.game.player)
		self.bgSpriteGroup.add(self.steelplatform)

		self.spriteGroup.add(self.game.player)

	def Enter(self, position):
		Room.Enter(self, position)
		if position == 'L':
			self.game.player.SetLeftPos(self.xOffs)
			self.game.player.SetBottomPos(self.bottomPlatformRect.top)
		elif position == 'R':
			self.game.player.SetLeftPos(self.xOffs + self.roomWidth - 20)
			self.game.player.SetBottomPos(self.bottomPlatformRect.top)

	def Update(self, userInput):
		Room.Update(self, userInput)

		if self.game.player.rect.right < self.xOffs + 15:
			self.game.player.SetRightPos(self.xOffs + 15)
		elif self.game.player.rect.left >= self.xOffs + self.roomWidth - 15:
			self.game.currentLevel.SetCurrentRoom(1, 'L')

	def Draw(self, screen):
		Room.Draw(self, screen)


# class Room01 =========================================================================================================

class Room01(Room):
	def __init__(self, game):
		Room.__init__(self, game)
		self.LoadBgImage("images/R01.bgnd.png")

		#self.blockList.append(pygame.Rect((left, top), (width, height)))

		self.fan = Fan(self.xOffs + 247, self.yOffs + 16, 180, -1)
		self.bgSpriteGroup.add(self.fan)
		self.spriteGroup.add(self.game.player)

		self.wasteBin = WasteBin(self.xOffs + 24, self.yOffs + 69)
		self.fgSpriteGroup.add(self.wasteBin)

		# Stone
		self.stone = Stone(self.xOffs + 184, self.yOffs + 73, self.blockList, self.game.player)
		self.bgSpriteGroup.add(self.stone)

		# Stairs
		self.s0Rect = pygame.Rect(self.xOffs + 0, self.yOffs + 111, 261, 116 - 111)
		self.blockList.append(self.s0Rect)

		self.s1Rect = pygame.Rect(self.xOffs + 0, self.yOffs + 106, 255, 111 - 106)
		self.blockList.append(self.s1Rect)

		self.s2Rect = pygame.Rect(self.xOffs + 0, self.yOffs + 101, 249, 106 - 101)
		self.blockList.append(self.s2Rect)

		self.s3Rect = pygame.Rect(self.xOffs + 0, self.yOffs + 96, 243, 101 - 96)
		self.blockList.append(self.s3Rect)

		self.s4Rect = pygame.Rect(self.xOffs + 0, self.yOffs + 91, 237, 96 - 91)
		self.blockList.append(self.s4Rect)

		self.s5Rect = pygame.Rect(self.xOffs + 0, self.yOffs + 86, 231, 91 - 86)
		self.blockList.append(self.s5Rect)

		self.s6Rect = pygame.Rect(self.xOffs + 0, self.yOffs + 81, 225, 86 - 81)
		self.blockList.append(self.s6Rect)

		# Lower platform
		self.bottomPlatformRect = pygame.Rect(self.xOffs + 0, self.yOffs + 116, self.roomWidth, self.roomHeight - 116)
		self.blockList.append(self.bottomPlatformRect)

		# Ceiling
		w = self.game.playField.get_width() + 20
		h = 2
		self.ceilingRect = pygame.Rect(-10, self.yOffs + 0, w, h)
		self.blockList.append(self.ceilingRect)

	def Enter(self, position):
		Room.Enter(self, position)
		if position == 'L':
			self.game.player.SetRightPos(self.xOffs + 20)
			self.game.player.SetBottomPos(self.s6Rect.top)
		elif position == 'R':
			self.game.player.SetLeftPos(self.xOffs + self.roomWidth - 20)
			self.game.player.SetBottomPos(self.bottomPlatformRect.top)

	def Update(self, userInput):
		Room.Update(self, userInput)
		if self.game.player.rect.right <= self.xOffs + 15:
			self.game.currentLevel.SetCurrentRoom(0, 'R')
		elif self.game.player.rect.left >= self.xOffs + self.roomWidth - 15:
			self.game.currentLevel.SetCurrentRoom(2, 'L')

	def Draw(self, screen):
		Room.Draw(self, screen)


# class Room02 =========================================================================================================

class Room02(Room):
	def __init__(self, game):
		Room.__init__(self, game)
		self.LoadBgImage("images/R02.bgnd.png")
		self.spriteGroup.add(self.game.player)

		# Lower platform
		self.bottomPlatformRect = pygame.Rect(self.xOffs + 0, self.yOffs + 116, self.roomWidth, self.roomHeight - 116)
		self.blockList.append(self.bottomPlatformRect)

		# Elevated platform
		for n in range(0, 5):
			rc = pygame.Rect(self.xOffs + 56 + 4 * n, self.yOffs + 115 - n, 153 - 8 * n, 1)
			self.blockList.append(rc)

		self.ticks = pygame.time.get_ticks()

	def Enter(self, position):
		Room.Enter(self, position)
		if position == 'L':
			self.game.player.SetRightPos(self.xOffs + 20)
		elif position == 'R':
			self.game.player.SetLeftPos(self.xOffs + self.roomWidth - 20)
		self.game.player.SetBottomPos(self.bottomPlatformRect.top)

	def Update(self, userInput):
		Room.Update(self, self.game.userInput)
		if self.game.player.rect.right <= self.xOffs + 15:
			self.game.currentLevel.SetCurrentRoom(1, 'R')
		elif self.game.player.rect.left > self.xOffs + self.roomWidth - 15:
			self.game.player.SetLeftPos(self.xOffs + self.roomWidth - 15)

		currentTicks = pygame.time.get_ticks()
		if currentTicks > self.ticks + 5000:
			self.ticks = currentTicks
			waterDrop = WaterDrop(self.xOffs + 97, self.yOffs + 85, self.yOffs + 102)
			self.bgSpriteGroup.add(waterDrop)

	def Draw(self, screen):
		Room.Draw(self, screen)


# class Level01 ========================================================================================================

class Level01(Level):
	def __init__(self, game):
		Level.__init__(self, game)
		self.roomList.append(Room00(game))
		self.roomList.append(Room01(game))
		self.roomList.append(Room02(game))

		self.SetCurrentRoom(0, 'L')
