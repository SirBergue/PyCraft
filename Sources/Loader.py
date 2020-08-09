import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse

from Sources.Graphics.Window import *

#https://ratcave.readthedocs.io/en/latest/tutorial1.html

class Loader:
	def __init__(self, conn):
		# Create Window Object
		window = Window(
			caption='PyCraft',
			fullscreen=True,
			vsync=True,
			visible=False
		)

		# Setup the OpenGL
		self.setup_gl()

		conn.send(True)

		if conn.recv() == True:
			conn.close()

			# Set the window visible
			window.set_visible(True)

			# Start pyglet window
			pyglet.app.run()

	def setup_gl(self):
		""" Method used to load GL """

		# Clear the window
		glClearColor(0.5, 0.6, 1.0, 1.0)

		# Enable face culling
		glEnable(GL_CULL_FACE)

		# Enables a simple fog
		glEnable(GL_FOG)
		glFogfv(GL_FOG_COLOR, (GLfloat * 4)(0.5, 0.6, 1.0, 0))

		glHint(GL_FOG_HINT, GL_DONT_CARE)
		glFogi(GL_FOG_MODE, GL_LINEAR)

		glFogf(GL_FOG_START, 20.0)
		glFogf(GL_FOG_END, 80.0)
