#!/usr/bin/python
# -*- coding: utf-8 -*-

# level.py

# class Level ==========================================================================================================

class Level:
	def __init__(self, game):
		self.game = game
		self.roomList = []
		self.currentRoom = None
		self.roomIsChanged = False

	def SetCurrentRoom(self, roomIndex, position):
		self.currentRoom = self.roomList[roomIndex]
		self.currentRoom.roomIsChanged = True
		self.currentRoom.Enter(position)

	def Update(self, userInput):
		if self.currentRoom is not None:
			self.currentRoom.Update(userInput)

	def Draw(self, screen):
		if self.roomIsChanged:
			self.roomIsChanged = False
			black = (0, 0, 0)
			screen.fill(black)

		if self.currentRoom is not None:
			self.currentRoom.Draw(screen)
