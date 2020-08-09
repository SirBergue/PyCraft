import pyglet
from pyglet.gl import *
from pyglet.window import key

from Sources.Settings import *

class Inventory:
    def __init__(self, width, height, texture_loader):
        self.base_distance = 60
        self.inv_size = 9
        self.life = 9

        self.width = width

        self.start_y = 0
        self.start_x = (width - self.base_distance * self.inv_size) // 2

        self.pickaxe = texture_loader.diamond_pickaxe

        self.hearts  = texture_loader.hearts
        self.food    = texture_loader.food

        self.indice = 0

    def draw(self):
        glClearColor(0, 0, 0, 0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        add = 25
        i = 0

        for i in range(self.life):
            self.hearts.blit(
                self.start_x + (add * i),
                self.base_distance + 10,
                width=25, height=25
            )

        for i in range(9):
            self.food.blit(
                self.start_x + (self.base_distance * self.inv_size) - (add * i) - 25,
                self.base_distance + 10,
                width=25, height=30
            )

        glClearColor(0.5, 0.6, 1.0, 1.0)
        glDisable(GL_BLEND)

        for i in range(self.inv_size):
            if i == self.indice:
                glColor3d(0.9, 0.9, 0.9)
            else:
                glColor3d(0.7, 0.7, 0.7)

            start_x = self.start_x + self.base_distance * i
            start_y = self.start_y

            self.box = pyglet.graphics.vertex_list(
                4,
                ('v2i',
                    (start_x, start_y, # LEFT-BOTTOM
                     start_x + self.base_distance, start_y, # RIGHT-BOTTOM
                     start_x + self.base_distance, start_y + self.base_distance, # RIGHT-TOP
                     start_x, start_y + self.base_distance) # LEFT-BOTTOM
                     )
                )

            self.box.draw(GL_QUADS)

        for i in range(self.inv_size + 1):
            glColor3d(0, 0, 0)

            start_x = self.start_x + self.base_distance * i
            start_y = self.start_y

            pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                ('v2i',
                    (start_x, start_y,
                     start_x, start_y + self.base_distance)
                )
            )

        glColor3d(1, 1, 1)

    def update(self, keys):
        if keys[key._1]:
            self.indice = 0
        if keys[key._2]:
            self.indice = 1
        if keys[key._3]:
            self.indice = 2
        if keys[key._4]:
            self.indice = 3
        if keys[key._5]:
            self.indice = 4
        if keys[key._6]:
            self.indice = 5
        if keys[key._7]:
            self.indice = 6
        if keys[key._8]:
            self.indice = 7
        if keys[key._9]:
            self.indice = 8
