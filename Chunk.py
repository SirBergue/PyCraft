import pyglet
from pyglet.gl import *

from Settings import *

import time
import random

class Chunk:
	def __init__(self, tex_loader, chunk_x, chunk_z):
		self.batch = pyglet.graphics.Batch()

		self.chunk_x = chunk_x * CHUNK_WIDTH
		self.chunk_z = chunk_z * CHUNK_WIDTH

		print(chunk_x)
		print(chunk_z)

		self.tex_loader = tex_loader

		self.blocks = {}

		self.tex_coords = (
			0, 0, 1, 0,
			1, 1, 0, 1,
		)

		i = 0

		start = time.process_time()

		# Generate world
		for x in range(CHUNK_WIDTH):
			for y in range(CHUNK_HEIGHT):
				for z in range(CHUNK_WIDTH):
					if y == 15:
						self.using_texture = self.tex_loader.grass_block
					elif y > 13 and y < 15:
						self.using_texture = self.tex_loader.earth_block
					elif y == 0:
						self.using_texture = self.tex_loader.bedrock_block
					else:
						chance = random.randint(0, 100)

						if chance <= 15:
							self.using_texture = self.tex_loader.coal_block
						else:
							self.using_texture = self.tex_loader.stone_block

					if not ((y > 0 and y < (CHUNK_HEIGHT - 1)) and
							(x + chunk_x > 0 and x < (CHUNK_WIDTH - 1)) and
							(z + chunk_z > 0 and z < (CHUNK_WIDTH - 1))):

						self.blocks[i] = self.generate_block(
							x + self.chunk_x,
							y,
							z + self.chunk_z,
							self.using_texture
						)

						i += 1

		x = random.randint(0, 15)
		y = 16
		z = random.randint(0, 15)

		self.using_texture = self.tex_loader.tree_block

		j = 0

		for j in range(4):
			self.blocks[i] = self.generate_block(
				x + self.chunk_x,
				y + j,
				z + self.chunk_z,
				self.using_texture
			)

			i += 1

		j += 1

		self.using_texture = self.tex_loader.leaf_block

		for n in range(2):
			for a in range(2):
				for b in range(2):
					self.blocks[i] = self.generate_block(
						x + self.chunk_x + a,
						y + j + n,
						z + self.chunk_z + b,
						self.using_texture
					)

					i += 1

					self.blocks[i] = self.generate_block(
						x + self.chunk_x - a,
						y + j + n,
						z + self.chunk_z - b,
						self.using_texture
					)

					i += 1

		print(f'Finished: {time.process_time() - start}')

	def generate_block(self, x, y, z, tex_sides):
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
				self._generate_block(texture, vertex, 24)
			)

			return square_dict_block

		elif (len(tex_sides) == 2):
			side_texture    = tex_sides[0]
			border_texture  = tex_sides[1]

			texture_vertex = {
				0: [side_texture,   vertex_side,   16],
				1: [border_texture, vertex_border, 8]
			}

		elif (len(tex_sides) == 3):
			side_texture    = tex_sides[0]
			top_texture     = tex_sides[1]
			bottom_texture  = tex_sides[2]

			texture_vertex = {
				0: [side_texture,   vertex_side,   16],
				1: [top_texture,    vertex_top,    4],
				2: [bottom_texture, vertex_bottom, 4],
			}

		else:
			back_texture   = tex_sides[0]
			front_texture  = tex_sides[1]
			top_texture    = tex_sides[2]
			bottom_texture = tex_sides[3]
			left_texture   = tex_sides[4]
			right_texture  = tex_sides[5]

			texture_vertex = {
				0: [back_texture,   vertex_back,   4],
				1: [front_texture,  vertex_front,  4],
				2: [top_texture,    vertex_top,    4],
				3: [bottom_texture, vertex_bottom, 4],
				4: [left_texture,   vertex_left,   4],
				5: [right_texture,  vertex_right,  4]
			}

		for key in texture_vertex:
			square_dict_block.append(
				self._generate_block(
					texture_vertex[key][0],
					texture_vertex[key][1],
					texture_vertex[key][2]
				)
			)

		return square_dict_block

	def _generate_block(self, texture, vertex, size):
		return self.batch.add(
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
