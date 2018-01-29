#!/usr/bin/python
# -*- coding: utf-8 -*-

# player.py

import pygame
from pygame.locals import *

# class Player =========================================================================================================

class Player(pygame.sprite.Sprite):
	TileWidth = 40
	TileHeight = 48

	# Player state constants
	State_Idle = 0
	State_Run = 1
	State_Jump = 2
	State_Fall = 3

	# Player animation phase indexes in the player image
	Phase_Run = 0	# 8 images
	Phase_Idle = 8	# 1 image
	Phase_Jump = 9	# 2 images

	# Moving directions
	Dir_Left = 0
	Dir_Right = 1

	VStepLimit = 3	# Vertical distance that do not block running state
	HStep = 6		# Horizontal movement distance in pixels
	HMovementDelay = 12	# Horizontal movement timing (ms)

	YMax = 26.0		# Jump height in pixels
	TYMax = 300.0	# Time to reach the top position while jumping (ms)
	VAccel = YMax / (TYMax * TYMax)

	fileImage = None
	stepSound1 = None
	stepSound2 = None
	stepSound3 = None

	def __init__(self, game):
		pygame.sprite.Sprite.__init__(self)
		Player.fileImage = pygame.image.load("images/Player.png").convert_alpha()
		self.rect = pygame.Rect(0, 20, 40, 48)
		self.collideRect = self.rect.copy()
		self.collideRect.inflate_ip(-20, 0)

		self.direction = Player.Dir_Left
		self.hasHSpeed = False

		self.state = Player.State_Idle
		self.phaseIndex = 0

		self.ticks = pygame.time.get_ticks()
		self.lastHTicks = 0.0	# Horizontal movement timing

		self.x0 = 0
		self.y0 = 0	# Vertical start position of jumping/falling (bottom position of the player)
		self.t0 = self.ticks # Start time of jumping/falling

		self.game = game
		self.image = Player.fileImage.subsurface(Player.Phase_Idle * Player.TileWidth, self.direction * Player.TileHeight, Player.TileWidth, Player.TileHeight)

		if Player.stepSound1 == None:
			Player.stepSound1 = pygame.mixer.Sound ("sounds/FootStep1.ogg")
		if Player.stepSound2 == None:
			Player.stepSound2 = pygame.mixer.Sound ("sounds/FootStep2.ogg")
		if Player.stepSound3 == None:
			Player.stepSound3 = pygame.mixer.Sound ("sounds/FootStep3.ogg")

		self.sounds = []

	def Move(self, dx, dy):
		self.rect.move_ip(dx, dy)
		self.collideRect.move_ip(dx, dy)

	def SetLeftPos(self, x):
		self.rect.left = x
		self.collideRect.centerx = self.rect.centerx

	def SetRightPos(self, x):
		self.rect.right = x
		self.collideRect.centerx = self.rect.centerx

	def SetBottomPos(self, y):
		self.rect.bottom = y
		self.collideRect.bottom = y

	def GetPosition(self):
		return self.rect.centerx, self.rect.bottom

	def GetCollideRect(self):
		return self.collideRect

	def CalcJumpPos(self, t, t0):
		'''Calculate vertical position of the player in the jump state'''
		dt = t - t0 - Player.TYMax
		return Player.YMax - (Player.VAccel * dt * dt)

	def CalcFallPos(self, t, t0):
		'''Calculate vertical position of the player in the fall state'''
		dt = t - t0
		return Player.VAccel * dt * dt

	def CheckVerticalCollision(self, dy):
		'''Check and calculate new vertical change with the proposed change value. Value of dy is adjusted to have no collision.'''
		playerIsOnASurface = False

		rc = self.GetCollideRect().copy()
		rc.move_ip(0, dy) # The proposed new vertical position
		indexList = rc.collidelistall(self.game.currentLevel.currentRoom.blockList)

		rc = self.GetCollideRect()
		for index in indexList:
			collidingRect = self.game.currentLevel.currentRoom.blockList[index]
			# We have collision on bottom or top. Top collision is ignored if there is bottom collision!
			if rc.bottom + dy > collidingRect.top and rc.top < collidingRect.top:
				dy = collidingRect.top - rc.bottom
				playerIsOnASurface = True
			elif playerIsOnASurface == False and rc.top + dy < collidingRect.bottom and rc.bottom > collidingRect.bottom:
				dy = collidingRect.bottom - rc.top
		return dy, playerIsOnASurface

	def CheckHorizontalCollision(self, dx):
		'''Check and calculate new horizontal change with the proposed change value. Value of dx is adjusted to have no collision.'''
		hasCollision = False

		rc = self.GetCollideRect().copy()
		rc.move_ip(dx, 0) # The proposed new horizontal position
		indexList = rc.collidelistall(self.game.currentLevel.currentRoom.blockList)

		rc = self.GetCollideRect()
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

	def SetState(self, newState):
		self.state = newState
		self.x0, self.y0 = self.GetPosition ()
		self.t0 = self.ticks
		self.lastHTicks = self.ticks

		if newState == Player.State_Idle:
			self.hasHSpeed = False
			self.ProcessIdleState (True)
		elif newState == Player.State_Run:
			if self.game.userInput.left:
				self.direction = Player.Dir_Left
				self.hasHSpeed = True
			elif self.game.userInput.right:
				self.direction = Player.Dir_Right
				self.hasHSpeed = True
			self.ProcessRunState ()
		elif newState == Player.State_Jump:
			self.ProcessJumpState ()
		elif newState == Player.State_Fall:
			self.ProcessFallState ()

	def ProcessIdleState(self, enterToState):
		if self.game.userInput.left or self.game.userInput.right:
			self.SetState(Player.State_Run)
			return

		dy = 0.0

		# ------------------------------
		# Test and do vertical movement.
		# ------------------------------
		# Check if the player is on a (vertically moving?) surface by checking for collision one pixel down.
		# Change to jump state only if 1.: there it is not on a surface or 2.: up key is pressed and it is on a surface
		dy, playerIsOnASurface = self.CheckVerticalCollision(1)

		if (playerIsOnASurface and self.game.userInput.up):
			self.SetState(Player.State_Jump)
			return
		elif not playerIsOnASurface:
			self.SetState(Player.State_Fall)
			return

		#########################################################
		# TO DO: Check collision with horizontally moving objects
		#########################################################

		if enterToState:
			# Set player animation phase
			self.phaseIndex = 0
			# Update player image
			tileIndexX = Player.Phase_Idle
			tileIndexY = self.direction
			self.image = Player.fileImage.subsurface(tileIndexX * Player.TileWidth, tileIndexY * Player.TileHeight, Player.TileWidth, Player.TileHeight)

	def ProcessRunState(self):
		# ---------------------------
		# Do vertical movement first.
		# ---------------------------
		# Check if the player is on a surface. Check for collision with one pixel down
		dy = 0
		dy, playerIsOnASurface = self.CheckVerticalCollision(1)
		if not playerIsOnASurface:
			# No collision, player is in the air.
			# Check the new position and adjust vertical change. Bottom collision is updated.
			dy, playerIsOnASurface = self.CheckVerticalCollision(dy + Player.VStepLimit)

			if playerIsOnASurface:
				# Set new vertical position of the player. Player steps down instantly.
				self.Move(0, dy)

		if not playerIsOnASurface:
			# Stop horizontal movement depends on how long is the user running
			if self.ticks - self.t0 < 500:
				self.hasHSpeed = False
			self.SetState(Player.State_Fall)
			return

		if self.game.userInput.up: # Check for jump only after gravity is handled
			self.SetState(Player.State_Jump)
			return

		# Handle user input
		if self.game.userInput.left is False and self.game.userInput.right is False:
			self.SetState(Player.State_Idle)
			self.sounds.append ((Player.stepSound3, 0.2))
			return

		dx = 0
		dt = self.ticks - self.lastHTicks
		if dt > 6 * Player.HMovementDelay:
			self.lastHTicks += 6 * Player.HMovementDelay

			if self.game.userInput.left:
				dx = -Player.HStep
				self.direction = Player.Dir_Left
			elif self.game.userInput.right:
				dx = +Player.HStep
				self.direction = Player.Dir_Right

		# -----------------------
		# Do horizontal movement.
		# -----------------------
		# Check for horizontal collision with dx movement against fixed or moving objects
		dxNew, hasHorizontalCollision = self.CheckHorizontalCollision(dx)
		# Set new horizontal position
		if not hasHorizontalCollision:
			self.Move(dx, 0)
		else:
			# Player is colliding with dx movement. Try to step up VStepLimit pixels and move with dx then
			rc = self.GetCollideRect().copy()
			rc.move_ip(dx, -Player.VStepLimit) # The proposed new vertical position
			indexList = rc.collidelistall(self.game.currentLevel.currentRoom.blockList)
			if len(indexList) == 0:
				# No collision: try to step up on a small block
				self.Move(dx, -Player.VStepLimit)
				hasHorizontalCollision = False
			else:
				# Collision: move with the modified dx value
				self.Move(dxNew, 0)
				dx = dxNew
				if dx != 0:
					hasHorizontalCollision = False

		# Set new player state
		if hasHorizontalCollision:
			tileIndexX = Player.Phase_Idle
		else:
			if dx < 0:
				# Advance player animation phase
				self.phaseIndex += 1
				if self.phaseIndex > 7:
					self.phaseIndex = 0
				tileIndexX = Player.Phase_Run + self.phaseIndex
			elif dx > 0:
				# Advance player animation phase
				self.phaseIndex += 1
				if self.phaseIndex > 7:
					self.phaseIndex = 0
				tileIndexX = Player.Phase_Run + self.phaseIndex
			else:
				return

			if self.phaseIndex == 3:
				self.sounds.append ((Player.stepSound1, 0.2))
			elif self.phaseIndex == 7:
				self.sounds.append ((Player.stepSound2, 0.2))

		# Update player image
		tileIndexY = self.direction

		self.image = Player.fileImage.subsurface(tileIndexX * Player.TileWidth, tileIndexY * Player.TileHeight, Player.TileWidth, Player.TileHeight)

	def ProcessJumpState(self):
		yt = self.y0 - self.CalcJumpPos(self.ticks, self.t0)
		x, bottomPos = self.GetPosition()
		dy = yt - bottomPos

		# Check the new position and adjust vertical change. Bottom collision is updated.
		dyNew, playerIsOnASurface = self.CheckVerticalCollision(dy)

		# Set new vertical position
		self.Move(0, dyNew)

		# Check for horizontal collision
		dx = 0
		dt = self.ticks - self.lastHTicks
		if dt > Player.HMovementDelay:
			self.lastHTicks += Player.HMovementDelay
			if self.direction == Player.Dir_Left and self.hasHSpeed:
				dx = -1
			elif self.direction == Player.Dir_Right and self.hasHSpeed:
				dx = +1

		dx, hasCollision = self.CheckHorizontalCollision(dx)

		# Set new horizontal position
		self.Move(dx, 0)

		# Set new player state
		if playerIsOnASurface:
			if dyNew > 20:
				self.SetState(Player.State_Idle)	# ->Player dies!
				self.sounds.append ((Player.stepSound3, 0.2))
				return
			else:
				self.SetState(Player.State_Idle)
				self.sounds.append ((Player.stepSound3, 0.2))
				return
		elif dyNew != dy:	# Collision on top
			self.SetState(Player.State_Fall)
			return

		self.phaseIndex = 0

		# Update player image
		tileIndexX = Player.Phase_Jump
		tileIndexY = self.direction

		self.image = Player.fileImage.subsurface(tileIndexX * Player.TileWidth, tileIndexY * Player.TileHeight, Player.TileWidth, Player.TileHeight)

	def ProcessFallState(self):
		yt = self.y0 + self.CalcFallPos(self.ticks, self.t0)
		x, bottomPos = self.GetPosition()
		dy = yt - bottomPos

		# Check the new position and adjust vertical change. Bottom collision is updated.
		dy, playerIsOnASurface = self.CheckVerticalCollision(dy)

		# Set new vertical position
		self.Move(0, dy)

		# Check for horizontal collision
		dx = 0
		dt = self.ticks - self.lastHTicks
		if dt > Player.HMovementDelay:
			self.lastHTicks += Player.HMovementDelay
			if self.direction == Player.Dir_Left and self.hasHSpeed:
				dx = -1
			elif self.direction == Player.Dir_Right and self.hasHSpeed:
				dx = +1

		dx, hasCollision = self.CheckHorizontalCollision(dx)

		# Set new horizontal position
		self.Move(dx, 0)

		# Set new player state
		if playerIsOnASurface:
			if dy > 20:
				self.SetState(Player.State_Idle)	# Player dies!
				self.sounds.append ((Player.stepSound3, 0.2))
				return
			else:
				self.SetState(Player.State_Idle)
				self.sounds.append ((Player.stepSound3, 0.2))
				return

		self.phaseIndex = 0

		# Update player image
		tileIndexX = Player.Phase_Jump
		tileIndexY = self.direction

		self.image = Player.fileImage.subsurface(tileIndexX * Player.TileWidth, tileIndexY * Player.TileHeight, Player.TileWidth, Player.TileHeight)

	def update(self):
		if self.game.currentLevel == None or self.game.currentLevel.currentRoom == None:
			return

		self.ticks = pygame.time.get_ticks()
#		self.ticks += 10

		if self.state == Player.State_Idle:
			self.ProcessIdleState(False)
		elif self.state == Player.State_Run:
			self.ProcessRunState()
		elif self.state == Player.State_Jump:
			self.ProcessJumpState()
		elif self.state == Player.State_Fall:
			self.ProcessFallState()
		else:	# Unknown state
			pass

		if len(self.sounds) > 0:
			for snd, vol in self.sounds:
				snd.set_volume (vol)
				snd.play ()
			self.sounds = []
