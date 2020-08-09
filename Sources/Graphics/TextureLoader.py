import pyglet
from pyglet.gl import *

from Sources.Settings import *

import time

class TextureLoader:
	def __init__(self):
		self.raw_spritesheet   = pyglet.image.load(TEXTURE_PATH)
		self.items_spritesheet = pyglet.image.load(ITEMS_PATH)
		self.heart_spritesheet = pyglet.image.load(HEART_PATH)
		self.food_spritesheet  = pyglet.image.load(FOOD_PATH)

		self.load_blocks()
		self.load_items()
		self.load_utils()

	def load_utils(self):
		start = time.process_time()

		self.hearts = self.load_texture_2d(
			200, [0, 0], self.heart_spritesheet
		)

		self.food = self.load_texture_2d(
			200, [0, 0], self.food_spritesheet
		)

		print(f'Finished Utils Loading: {time.process_time() - start}')

	def load_items(self):
		start = time.process_time()

		self.diamond_pickaxe = self.load_texture_2d(
			16, PICKAXE, self.items_spritesheet)

		print(f'Finished Items Loading: {time.process_time() - start}')

	def load_blocks(self):
		start = time.process_time()

		self.grass_block   = self.load_texture_with_sides(
			16, GRASS_SIDES, self.raw_spritesheet)
		self.earth_block   = self.load_texture_with_sides(
			16, EARTH_SIDES, self.raw_spritesheet)
		self.stone_block   = self.load_texture_with_sides(
			16, STONE_SIDES, self.raw_spritesheet)
		self.bedrock_block = self.load_texture_with_sides(
			16, BEDROCK_SIDES, self.raw_spritesheet)
		self.coal_block    = self.load_texture_with_sides(
			16, COAL_SIDES, self.raw_spritesheet)
		self.leaf_block    = self.load_texture_with_sides(
			16, LEAF_SIDES, self.raw_spritesheet)
		self.tree_block    = self.load_texture_with_sides(
			16, TREE_SIDES, self.raw_spritesheet)

		print(f'Finished Block Loading: {time.process_time() - start}')

	def load_texture_with_sides(self, size, sides_location:dict, spritesheet):
		""" Method called to return a spritesheet loaded and its sides"""

		sides = []

		for i in range(len(sides_location)):
			sides.append(pyglet.graphics.TextureGroup(
					spritesheet.get_region(
							x=sides_location[i][0] * size,
							y=sides_location[i][1] * size,
							width=size,
							height=size
						).get_texture()
				))

			glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
			glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

		return sides

	def load_texture_2d(self, size, location, spritesheet):
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

		return spritesheet.get_region(
			x=location[0] * size,
			y=location[1] * size,
			width=size,
			height=size
		).get_texture()
