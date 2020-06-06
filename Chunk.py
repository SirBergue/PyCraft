import pyglet
from pyglet.gl import *

from Settings import *

class Chunk:
	def __init__(self, tex_loader, chunk_x, chunk_z):
		self.batch = pyglet.graphics.Batch()

		self.chunk_x = chunk_x * CHUNK_WIDTH
		self.chunk_z = chunk_z * CHUNK_WIDTH

		self.tex_loader = tex_loader

		self.tex_coords = (
			't2f', (
				0, 0, 1, 0,
				1, 1, 0, 1,
			)
		)

		self.blocks = {}

		i = 0

		for x in range(CHUNK_WIDTH):
			for y in range(CHUNK_HEIGHT):
				for z in range(CHUNK_WIDTH):
					self.blocks[i] = self.generate_block(x + self.chunk_x, y, z + self.chunk_z,
						self.tex_loader.earth_block)

					i += 1

	def generate_block(self, x, y, z, tex_sides):
		square_dict_block = []

		back_texture   = tex_sides[0]
		front_texture  = tex_sides[1]
		top_texture    = tex_sides[2]
		bottom_texture = tex_sides[3]
		left_texture   = tex_sides[4]
		right_texture  = tex_sides[5]

		X, Y, Z = x + 1, y + 1, z + 1

		self.vertex_back   = (X, y, z,  x, y, z,  x, Y, z,  X, Y, z)
		self.vertex_front  = (x, y, Z,  X, y, Z,  X, Y, Z,  x, Y, Z)
		self.vertex_top    = (x, Y, Z,  X, Y, Z,  X, Y, z,  x, Y, z)
		self.vertex_bottom = (x, y, z,  X, y, z,  X, y, Z,  x, y, Z)
		self.vertex_left   = (x, y, z,  x, y, Z,  x, Y, Z,  x, Y, z)
		self.vertex_right  = (X, y, Z,  X, y, z,  X, Y, z,  X, Y, Z)

		square_dict_block.append(self.batch.add(4, GL_QUADS, back_texture, ('v3f/static', self.vertex_back), self.tex_coords))
		square_dict_block.append(self.batch.add(4, GL_QUADS, front_texture, ('v3f/static', self.vertex_front), self.tex_coords))
		square_dict_block.append(self.batch.add(4, GL_QUADS, top_texture, ('v3f/static', self.vertex_top), self.tex_coords))
		square_dict_block.append(self.batch.add(4, GL_QUADS, bottom_texture, ('v3f/static', self.vertex_bottom), self.tex_coords))
		square_dict_block.append(self.batch.add(4, GL_QUADS, left_texture, ('v3f/static', self.vertex_left), self.tex_coords))
		square_dict_block.append(self.batch.add(4, GL_QUADS, right_texture, ('v3f/static', self.vertex_right), self.tex_coords))

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
		for i in range(6):
			try:
				self.blocks[chunk][block][i].delete()
			except:
				pass
