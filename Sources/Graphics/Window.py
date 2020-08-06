import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse

from Sources.Settings import *
from Sources.Physics.Player import *
from Sources.World.Chunk import *
from Sources.Utils.Inventory import *

import time

""" Window Class

Here we will be creating a Class used by Pyglet to generate windows;
Parcially main game class
"""
class Window(pyglet.window.Window):
	def push_update(self, pos, rot):
		glPushMatrix()

		rot = self.player.rot
		pos = self.player.pos

		glRotatef(-rot[0], 1, 0, 0)
		glRotatef(-rot[1], 0, 1, 0)

		glTranslatef(-pos[0], -pos[1], -pos[2])

	def matrix_projection(self):
		""" Enter in matrix mode projection """
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()

	def matrix_model(self):
		""" Enter in matrix mode model """
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

	def set_3d(self):
		""" Method used to OpenGL draw in 3D """

		glEnable(GL_DEPTH_TEST)
		self.matrix_projection()
		gluPerspective(70, self.width / self.height, 0.05, 1000)
		self.matrix_model()

	def set_2d(self):
		""" Method used to opengl draw 2d """

		glDisable(GL_DEPTH_TEST)
		self.matrix_projection()
		glOrtho(0, max(1, self.width), 0, max(1, self.height), -1, 1)
		self.matrix_model()

	def draw_framerate(self):
		""" Method used to draw a framerate """

		if time.time() - self.last_time_framerate >= 1:
			self.framerate.text = str(self.frames_passed)
			self.frames_passed = 0
			self.last_time_framerate = time.time()
		else:
			self.frames_passed += 1

		self.framerate.draw()

	def draw_player_location(self):
		self.player_location_label.text = f'X: {self.player.pos[0] // 1}   Y: {self.player.pos[1] // 1}   Z: {self.player.pos[2] // 1}'
		self.player_location_label.draw()

	def draw_player_target(self):
		""" Method used to draw a target to a Player"""
		glColor3d(0, 0, 0)
		self.player_target.draw(GL_LINES)
		glColor3d(1, 1, 1)

	def __init__(self, *args, **kwargs):
		""" Main class constructor """
		super().__init__(*args, **kwargs)

        # Set the mouse exclusive
		self.set_exclusive_mouse(True)

        # Load key handlers
		self.key_handler = pyglet.window.key.KeyStateHandler()
		self.push_handlers(self.key_handler)

		# Load texture loader
		self.texture_loader = TextureLoader(TEXTURE_PATH)

		# Implements update function to pyglet
		pyglet.clock.schedule(self.update)

		# Framerate variables
		self.last_time_framerate = time.time()
		self.frames_passed = 0
		self.framerate = pyglet.text.Label(text='Unknown', font_size=32, x=10, y=10, color=(255, 255, 255, 255))

		self.player_location_label = pyglet.text.Label(
			text='Unknown',
			font_size=24,
			x=self.width - (self.width / 4),
			y=self.height - 40,
			color=(255, 255, 255, 255)
		)

		self.player = Player((0.5, 18, 0.5), (60, 90))
		self.world = World(self.texture_loader)
		self.inv = Inventory(self.width, self.height)

		# Creates a player target
		self.player_target = pyglet.graphics.vertex_list(4, ('v2i', (
			self.width // 2 - TARGET_SIZE,
			self.height // 2,
			self.width // 2 + TARGET_SIZE,
			self.height // 2,

			self.width // 2,
			self.height // 2 - TARGET_SIZE,
			self.width // 2,
			self.height // 2 + TARGET_SIZE
		)))

	def on_mouse_motion(self, x, y, dx, dy):
		self.player.mouse_motion(dx, dy)

	def on_mouse_press(self, x, y, button, mod):
		player_x, player_y, player_z = self.player.pos

		if player_x // 16 > player_z // 16:
			chunk = player_x // 16
		else:
			chunk = player_z // 16

		block_x = player_x // 1
		block_y = player_y // 1
		block_z = player_z // 1

		block_number = block_x * block_y * block_z
		# idea

		self.world.remove_block(chunk, block_number)

	def on_key_press(self, symbol, modifiers):
		if symbol == key.ESCAPE:
			self.close()

	def update(self, dt):
		self.player.update(dt, self.key_handler)
		self.inv.update(self.key_handler)

		if not self.player.flying:
			self.player.pos[1] -= self.player.vel

			if self.player.gravity < 1:
				self.player.vel += self.player.gravity
				self.player.vel = self.player.vel

		if self.player.pos[1] <= -20:
			self.player.pos[1] = 18
			self.player.vel = 0

	def on_draw(self):
		""" Method called by Pyglet to draw Canvas """
		self.clear()

		self.set_3d()
		self.push_update(self.player.pos, self.player.rot)

		for chunk in self.world.chunks:
			if not chunk.chunk_x - CHUNK_WIDTH * RENDER_VISION > self.player.pos[0]:
				if not self.player.pos[0] > chunk.chunk_x + CHUNK_WIDTH * RENDER_VISION:
					if not chunk.chunk_z - CHUNK_WIDTH * RENDER_VISION > self.player.pos[2]:
						if not self.player.pos[2] > chunk.chunk_z + CHUNK_WIDTH * RENDER_VISION:
							chunk.batch.draw()

		for chunk in self.world.chunks:
			if not chunk.chunk_x - CHUNK_WIDTH * RENDER_VISION > self.player.pos[0]:
				if not self.player.pos[0] > chunk.chunk_x + CHUNK_WIDTH * RENDER_VISION:
					if not chunk.chunk_z - CHUNK_WIDTH * RENDER_VISION > self.player.pos[2]:
						if not self.player.pos[2] > chunk.chunk_z + CHUNK_WIDTH * RENDER_VISION:
							# Enable transparecy
							glClearColor(0, 0, 0, 0)
							glEnable(GL_BLEND)
							glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

							chunk.custom.draw()

							# Disable transparecy
							glClearColor(0.5, 0.6, 1.0, 1.0)
							glDisable(GL_BLEND)

		self.set_2d()
		self.draw_player_target()
		self.draw_framerate()
		self.draw_player_location()
		self.inv.draw()

		glPopMatrix()

class TextureLoader:
	def __init__(self, path):
		self.raw_spritesheet = pyglet.image.load(path)

		start = time.process_time()

		self.grass_block   = self.load_texture_with_sides(16, GRASS_SIDES)
		self.earth_block   = self.load_texture_with_sides(16, EARTH_SIDES)
		self.stone_block   = self.load_texture_with_sides(16, STONE_SIDES)
		self.bedrock_block = self.load_texture_with_sides(16, BEDROCK_SIDES)
		self.coal_block    = self.load_texture_with_sides(16, COAL_SIDES)
		self.leaf_block    = self.load_texture_with_sides(16, LEAF_SIDES)
		self.tree_block    = self.load_texture_with_sides(16, TREE_SIDES)

		print(f'Finished Block Loading: {time.process_time() - start}')

	def load_texture_with_sides(self, size, sides_location:dict):
		""" Method called to return a spritesheet loaded and its sides"""

		sides = []

		for i in range(len(sides_location)):
			sides.append(pyglet.graphics.TextureGroup(
					self.raw_spritesheet.get_region(
							x=sides_location[i][0] * size,
							y=sides_location[i][1] * size,
							width=size,
							height=size
						).get_texture()
				))

			glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
			glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

		return sides
