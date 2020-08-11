import pyglet
from pyglet.gl import *
from pyglet.window import key

import math

from Sources.Settings import *

class Player:
	def __init__(self, pos=(0, 0, 0), rot=(0, 0)):
		self.pos = list(pos)
		self.rot = list(rot)

		self.flying = True

		self.vel = 0
		self.gravity = 0.005

	def mouse_motion(self, dx, dy):

		dx /= 3
		dy /= 3

		self.rot[0] += dy
		self.rot[1] -= dx

		if self.rot[0] > 90:
			self.rot[0] = 90

		elif self.rot[0] < -90:
			self.rot[0] = -90

	def update(self, dt, keys, relation_block):
		sens = 1
		d = dt * 15

		rotY = -self.rot[1] / 180 * math.pi

		dx = d * math.sin(rotY)
		dz = d * math.cos(rotY)

		if keys[key.W]:
			print(self.pos)
			if not relation_block(self.pos[0] + dx * sens, self.pos[1], self.pos[2] - dz * sens):
				self.pos[0] += dx * sens
				self.pos[2] -= dz * sens

		if keys[key.S]:
			if not relation_block(self.pos[0] - dx * sens, self.pos[1], self.pos[2] + dz * sens):
				self.pos[0] -= dx * sens
				self.pos[2] += dz * sens

		if keys[key.A]:
			if not relation_block(self.pos[0] - dx * sens, self.pos[1], self.pos[2] - dz * sens):
				self.pos[0] -= dz * sens
				self.pos[2] -= dx * sens

		if keys[key.D]:
			if not relation_block(self.pos[0] + dx * sens, self.pos[1], self.pos[2] + dz * sens):
				self.pos[0] += dz * sens
				self.pos[2] += dx * sens

		if keys[key.SPACE]:
			if self.flying:
				if not relation_block(self.pos[0], self.pos[1] + d, self.pos[2]):
					self.pos[1] += d

		if keys[key.LSHIFT]:
			if self.flying:
				if not relation_block(self.pos[0], self.pos[1] - d, self.pos[2]):
					self.pos[1] -= d
