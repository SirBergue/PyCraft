import pyglet
from pyglet.gl import *

from Sources.Settings import *

import time
import random

class Chunk:
	def __init__(self, tex_loader, chunk_x, chunk_z):
		self.batch  = pyglet.graphics.Batch()
		self.custom = pyglet.graphics.Batch()

		self.chunk_x = chunk_x * CHUNK_WIDTH
		self.chunk_z = chunk_z * CHUNK_WIDTH

		self.tex_loader = tex_loader

		self.blocks = {}

		self.tex_coords = (
			0, 0, 1, 0,
			1, 1, 0, 1,
		)

		self.texture_layer = {
			0:  self.tex_loader.bedrock_block,
			CHUNK_HEIGHT - 2: self.tex_loader.earth_block,
			CHUNK_HEIGHT - 1: self.tex_loader.grass_block
		}

		start = time.process_time()

		self.now = 0

		for x in range(CHUNK_WIDTH):
			for y in range(CHUNK_HEIGHT):
				for z in range(CHUNK_WIDTH):
					self.generate_world(x, y, z, chunk_x, chunk_z)

		self.generate_tree()

		print(f'Finished: {time.process_time() - start}')

	def generate_world(self, x, y, z, chunk_x, chunk_z):

		generate = False

		if not (y > 0 and y < (CHUNK_HEIGHT - 1)):
			generate = True
		else:
			if (chunk_x == (CHUNK_DISTANCE - 1) and chunk_z == (CHUNK_DISTANCE - 1)):
				# Border verification
				if not (x + chunk_x > 0 and x < (CHUNK_WIDTH - 1)):
					generate = True
				else:
					if not (z + chunk_z > 0 and z < (CHUNK_WIDTH - 1)):
						generate = True

			elif (chunk_x == (CHUNK_DISTANCE - 1)):
				# Border verification
				if not (x + chunk_x > 0 and x < (CHUNK_WIDTH - 1)):
					generate = True
				else:
					if not (z + chunk_z > 0 and z <= (CHUNK_WIDTH - 1)):
						generate = True

			elif (chunk_z == (CHUNK_DISTANCE - 1)):
				# Border verification
				if not (x + chunk_x > 0 and x <= (CHUNK_WIDTH - 1)):
					generate = True
				else:
					if not (z + chunk_z > 0 and z < (CHUNK_WIDTH - 1)):
						generate = True
			else:
				# Normal verification
				if not (x + chunk_x > 0 and x <= (CHUNK_WIDTH - 1)):
					generate = True
				else:
					if not (z + chunk_z > 0 and z <= (CHUNK_WIDTH - 1)):
						generate = True

		if generate:
			if int(100 * random.random()) <= 10:
				default = self.tex_loader.coal_block
			else:
				default = self.tex_loader.stone_block

			self.using_texture = self.texture_layer.get(y, default)

			self.blocks[self.now] = self.generate_block(
				x + self.chunk_x,
				y,
				z + self.chunk_z,
				self.using_texture,
				self.batch
			)
			self.now += 1

	def generate_tree(self):
		x = int(15 * random.random())
		z = int(15 * random.random())

		self.using_texture = self.tex_loader.tree_block

		for height in range(4):
			self.blocks[self.now] = self.generate_block(
				x + self.chunk_x,
				CHUNK_HEIGHT + height,
				z + self.chunk_z,
				self.using_texture,
				self.custom
			)

			self.now += 1

		height += 1

		self.using_texture = self.tex_loader.leaf_block

		for leaf_y in range(2):
			for leaf_x in range(2):
				for leaf_z in range(2):
					self.blocks[self.now] = self.generate_block(
						x + self.chunk_x + leaf_x,
						CHUNK_HEIGHT + height + leaf_y,
						z + self.chunk_z + leaf_z,
						self.using_texture,
						self.custom
					)

					self.now += 1

					self.blocks[self.now] = self.generate_block(
						x + self.chunk_x - leaf_x,
						CHUNK_HEIGHT + height + leaf_y,
						z + self.chunk_z - leaf_z,
						self.using_texture,
						self.custom
					)

					self.now += 1

	def generate_block(self, x, y, z, tex_sides, batch):
		square_dict_block = []

		X, Y, Z = x + 1, y + 1, z + 1

		vertex_back   = (X, y, z,  x, y, z,  x, Y, z,  X, Y, z)
		vertex_front  = (x, y, Z,  X, y, Z,  X, Y, Z,  x, Y, Z)
		vertex_top    = (x, Y, Z,  X, Y, Z,  X, Y, z,  x, Y, z)
		vertex_bottom = (x, y, z,  X, y, z,  X, y, Z,  x, y, Z)
		vertex_left   = (x, y, z,  x, y, Z,  x, Y, Z,  x, Y, z)
		vertex_right  = (X, y, Z,  X, y, z,  X, Y, z,  X, Y, Z)

		vertex = vertex_back + vertex_front + vertex_top + vertex_bottom + vertex_left + vertex_right
		vertex_side = vertex_back + vertex_front + vertex_left + vertex_right
		vertex_border = vertex_top + vertex_bottom

		if (len(tex_sides) == 1):
			texture = tex_sides[0]

			square_dict_block.append(
				self._generate_block(texture, vertex, 24, batch)
			)

			return square_dict_block

		elif (len(tex_sides) == 2):
			side_texture    = tex_sides[0]
			border_texture  = tex_sides[1]

			texture_vertex = (
				(side_texture,   vertex_side,  16),
				(border_texture, vertex_border, 8)
			)

		elif (len(tex_sides) == 3):
			side_texture    = tex_sides[0]
			top_texture     = tex_sides[1]
			bottom_texture  = tex_sides[2]

			texture_vertex = (
				(side_texture,   vertex_side,   16),
				(top_texture,    vertex_top,    4),
				(bottom_texture, vertex_bottom, 4)
			)

		else:
			back_texture   = tex_sides[0]
			front_texture  = tex_sides[1]
			top_texture    = tex_sides[2]
			bottom_texture = tex_sides[3]
			left_texture   = tex_sides[4]
			right_texture  = tex_sides[5]

			texture_vertex = (
				(back_texture,   vertex_back,   4),
				(front_texture,  vertex_front,  4),
				(top_texture,    vertex_top,    4),
				(bottom_texture, vertex_bottom, 4),
				(left_texture,   vertex_left,   4),
				(right_texture,  vertex_right,  4)
			)

		for key in range(len(texture_vertex)):
			square_dict_block.append(
				self._generate_block(
					texture_vertex[key][0],
					texture_vertex[key][1],
					texture_vertex[key][2],
					batch
				)
			)

		return square_dict_block

	def _generate_block(self, texture, vertex, size, batch):
		return batch.add(
			size,
			GL_QUADS,
			texture,
			('v3f/static', vertex),
			('t2f', self.tex_coords * int((size / 4)))
		)

class World:
	def __init__(self, tex_loader):
		self.chunks = []
		self.blocks = {}
		self.actual_block = 0

		for chunk_x in range(CHUNK_DISTANCE):
			for chunk_z in range(CHUNK_DISTANCE):
				chunk = Chunk(tex_loader, chunk_x, chunk_z)

				self.blocks[self.actual_block] = chunk.blocks
				self.chunks.append(chunk)

				self.actual_block += 1

	def remove_block(self, chunk, block):
		for i in range(len(self.blocks[chunk][block])):
			self.blocks[chunk][block][i].delete()
