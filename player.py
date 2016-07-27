#!/usr/bin/python
# -*- coding: utf-8 -*-

# player.py

import pygame
from pygame.locals import *

# class Player =========================================================================================================

class Player (pygame.sprite.Sprite):
	TileWidth = 40
	TileHeight = 48

	# Player state constants
	State_Idle = 0
	State_Run = 1
	State_Jump = 2

	# Player animation phase indexes in the player image
	Phase_Run = 0	# 8 images
	Phase_Idle = 8	# 1 image
	Phase_Jump = 9	# 2 images

	# Moving directions
	Direction_Left = 0
	Direction_Right = 1

	JumpValue = -14
	FallingValue = 3
	StepValue = 3	# Vertical distance that do not block user while running

	fileImage = None

	def __init__(self, game):
		pygame.sprite.Sprite.__init__(self)
		Player.fileImage = pygame.image.load ("images/Player.png").convert_alpha ()
		self.rect = pygame.Rect (0, 20, 40, 48)
		self.direction = Player.Direction_Left
		self.state = Player.State_Idle
		self.phaseIndex = 0

		self.dx = 0
		self.dy = 0

		self.image = Player.fileImage.subsurface (Player.Phase_Idle * Player.TileWidth, self.direction * Player.TileHeight, Player.TileWidth, Player.TileHeight)

		self.ticks = pygame.time.get_ticks ()
		self.updateTime = 65	# ms
		self.game = game

		self.collideRect = self.rect.copy ()
		self.collideRect.inflate_ip (-20, 0)

	def Move (self, dx, dy):
		self.rect.move_ip (dx, dy)
		self.collideRect.move_ip (dx, dy)

	def SetLeftPos (self, x):
		self.rect.left = x
		self.collideRect.centerx = self.rect.centerx

	def SetRightPos (self, x):
		self.rect.right = x
		self.collideRect.centerx = self.rect.centerx

	def SetBottomPos (self, y):
		self.rect.bottom = y
		self.collideRect.bottom = y

	def GetCollideRect (self):
		return self.collideRect

	def CheckVerticalCollision (self, dy):
		'''Check and calculate new vertical change with the proposed change value. Value of dy is adjusted to have no collision.'''
		playerIsOnASurface = False

		rc = self.GetCollideRect ().copy ()
		rc.move_ip (0, dy) # The proposed new vertical position
		indexList = rc.collidelistall (self.game.currentLevel.currentRoom.blockList)

		rc = self.GetCollideRect ()
		for index in indexList:
			collidingRect = self.game.currentLevel.currentRoom.blockList[index]
			# We have collision on bottom or top. Top collision is ignored if there is bottom collision!
			if rc.bottom + dy > collidingRect.top and rc.top < collidingRect.top:
				dy = collidingRect.top - rc.bottom
				playerIsOnASurface = True
			elif playerIsOnASurface == False and rc.top + dy < collidingRect.bottom and rc.bottom > collidingRect.bottom:
				dy = collidingRect.bottom - rc.top
		return dy, playerIsOnASurface

	def CheckHorizontalCollision (self, dx):
		'''Check and calculate new horizontal change with the proposed change value. Value of dx is adjusted to have no collision.'''
		hasCollision = False

		rc = self.GetCollideRect ().copy ()
		rc.move_ip (dx, 0) # The proposed new horizontal position
		indexList = rc.collidelistall (self.game.currentLevel.currentRoom.blockList)

		rc = self.GetCollideRect ()
		for index in indexList:
			collidingRect = self.game.currentLevel.currentRoom.blockList[index]
			# Check for collision on left and right and adjust horizontal change
			if rc.left + dx < collidingRect.right and rc.right > collidingRect.right:
				dx = collidingRect.right - rc.left
				hasCollision = True
			elif rc.right + dx > collidingRect.left and rc.left < collidingRect.left:
				dx = collidingRect.left - rc.right
				hasCollision = True
		return dx, hasCollision

	def ProcessIdleState (self):
		if self.game.userInput.left or self.game.userInput.right:
			self.state = Player.State_Run
			self.ProcessRunState ()
			return

		dy = 0

		# ---------------------
		# Do vertical movement.
		# ---------------------
		# Check if the player is on a surface. Check for collision with one pixel down
		dy, playerIsOnASurface = self.CheckVerticalCollision (1)
		if not playerIsOnASurface:
			# No collision, player is in the air. Initiate falling with gravity
			# Check the new position and adjust vertical change. Bottom collision is updated.
			dy, playerIsOnASurface = self.CheckVerticalCollision (self.dy + Player.FallingValue)

			# Set new vertical position of the player
			self.Move (0, dy)

		if playerIsOnASurface and self.game.userInput.up: # Check for jump only after gravity is handled
			self.dy = Player.JumpValue
			self.ProcessJumpState ()
			return

		self.state = Player.State_Idle
		self.dx = 0
		self.dy = dy

	def ProcessRunState (self):
		if self.game.userInput.left:
			dx = -6
		elif self.game.userInput.right:
			dx = +6
		else:
			self.state = Player.State_Idle
			self.ProcessIdleState ()
			return

		dy = 0

		# ---------------------------
		# Do vertical movement first.
		# ---------------------------
		# Check if the player is on a surface. Check for collision with one pixel down
		dy, playerIsOnASurface = self.CheckVerticalCollision (1)
		if not playerIsOnASurface:
			# No collision, player is in the air.
			# Check the new position and adjust vertical change. Bottom collision is updated.
			dy, playerIsOnASurface = self.CheckVerticalCollision (self.dy + Player.StepValue)

			# Set new vertical position of the player
			self.Move (0, dy)

		if not playerIsOnASurface:
			dx = 0 # Stop horizontal movement if there is no surface below the player
		elif self.game.userInput.up: # Check for jump only after gravity is handled
			self.dx = dx
			self.dy = Player.JumpValue
			self.state = Player.State_Jump
			self.ProcessJumpState ()
			return

		# -----------------------
		# Do horizontal movement.
		# -----------------------

		# Check for horizontal collision
		dxNew, hasCollision = self.CheckHorizontalCollision (dx)

		# Set new horizontal position
		if not hasCollision:
			self.Move (dxNew, 0)
		else:
			# Player is colliding with dx movement. Try to step up some pixels and move with dx
			rc = self.GetCollideRect ().copy ()
			rc.move_ip (dx, -Player.StepValue) # The proposed new vertical position
			indexList = rc.collidelistall (self.game.currentLevel.currentRoom.blockList)
			if len (indexList) == 0:
				# No collision: step up
				self.Move (dx, -Player.StepValue)
			else:
				# Collision: move with the modified dx value
				self.Move (dxNew, 0)

		# Set new player state
		if dx != 0:
			self.state = Player.State_Run
			self.dx = dx
			self.dy = dy
		else:
			self.state = Player.State_Idle
			self.dx = 0
			self.dy = dy

	def ProcessJumpState (self):
		dx = self.dx
		dy = self.dy + Player.FallingValue # Increase speed change (gravity acceleration)

		# Check the new position and adjust vertical change. Bottom collision is updated.
		dy, playerIsOnASurface = self.CheckVerticalCollision (dy)

		# Set new vertical position
		self.Move (0, dy)

		# Check for horizontal collision
		dx, hasCollision = self.CheckHorizontalCollision (dx)

		# Set new horizontal position
		self.Move (dx, 0)

		# Set new player state
		if playerIsOnASurface:
			if dy > 20:
				self.state = Player.State_Idle	# PLAYER DIES!
			else:
				self.state = Player.State_Idle
			self.dx = 0
			self.dy = 0
		else:
			self.state = Player.State_Jump
			self.dx = dx
			self.dy = dy

	def update (self):
		if self.game.currentLevel == None or self.game.currentLevel.currentRoom == None:
			return

		currentTicks = pygame.time.get_ticks ()
		if currentTicks > self.ticks + self.updateTime:
			self.ticks = currentTicks

			if self.state == Player.State_Idle:
				self.ProcessIdleState ()
			elif self.state == Player.State_Run:
				self.ProcessRunState ()
			elif self.state == Player.State_Jump:
				self.ProcessJumpState ()
			else:	# Unknown state
				pass

			# Advance player animation phase
			if self.state == Player.State_Run:
				if self.dx < 0:
					self.direction = Player.Direction_Left
					self.phaseIndex += 1
					if self.phaseIndex > 7:
						self.phaseIndex = 0

				elif self.dx > 0:
					self.direction = Player.Direction_Right
					self.phaseIndex += 1
					if self.phaseIndex > 7:
						self.phaseIndex = 0
			elif self.state == Player.State_Jump:
				if self.dx < 0:
					self.direction = Player.Direction_Left
				elif self.dx > 0:
					self.direction = Player.Direction_Right

				self.phaseIndex = 0
			else:
				self.phaseIndex = 0

			# Update player image
			tileIndexX = 0
			tileIndexY = 0
			if self.state == Player.State_Idle:
				tileIndexX = Player.Phase_Idle
				tileIndexY = self.direction
			elif self.state == Player.State_Run:
				tileIndexX = Player.Phase_Run + self.phaseIndex
				tileIndexY = self.direction
			elif self.state == Player.State_Jump:
				tileIndexX = Player.Phase_Jump
				tileIndexY = self.direction

			self.image = Player.fileImage.subsurface (tileIndexX * Player.TileWidth, tileIndexY * Player.TileHeight, Player.TileWidth, Player.TileHeight)
