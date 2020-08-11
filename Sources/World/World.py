import pyglet
from pyglet.gl import *

from Sources.Settings import *
from Sources.World.Chunk import *

class World:
	def __init__(self, tex_loader):
		self.chunks = []

		for chunk_x in range(CHUNK_DISTANCE):
			for chunk_z in range(CHUNK_DISTANCE):
				chunk = Chunk(tex_loader, chunk_x, chunk_z)
				self.chunks.append(chunk)

	def get_chunk(self, x, z):
		for chunk in self.chunks:
			if chunk.x == x and chunk.z == z:
				return chunk

	def get_block_chunk(self, player_x, player_y, player_z, chunk):
		for element in chunk.blocks:
			if block := (
				element.get(player_x, {}).get(player_y, {}).get(player_z, {})):
				return block

	def relation_block(self, player_x, player_y, player_z):
		chunk_x = player_x // 16
		chunk_z = player_z // 16

		chunk = self.get_chunk(chunk_x, chunk_z)

		if chunk:
			player_x = (player_x // 1) - (16 * chunk_x)
			player_y = (player_y // 1)
			player_z = (player_z // 1) - (16 * chunk_z)

			return self.get_block_chunk(player_x, player_y, player_z, chunk)

	def _remove_block(self, block):
		for n in block:
			n.delete()

		block.clear()

	def remove_block(self, player_x, player_y, player_z):
		block_remove = self.relation_block(player_x, player_y, player_z)

		if block_remove:
			self._remove_block(block_remove)
