import os
import time

from multiprocessing import Process, Pipe

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame

class Launcher:
    def __init__(self):
        self.parent_conn, self.child_conn = Pipe()

        self.p = Process(target=self.LoadGame, args=(self.child_conn,))
        self.p.start()

        pygame.init()

        self.FADE_IN_TIME = 2.5
        self.FADE_OUT_TIME = 2.5

        self.ST_FADEIN = 0
        self.ST_FADEOUT = 1

        self.clock = pygame.time.Clock()

        infoObject = pygame.display.Info()
        self.width, self.height = infoObject.current_w, infoObject.current_h

        self.screen = pygame.display.set_mode(
            (self.width, self.height),
             pygame.FULLSCREEN
        )

        self.font = pygame.font.SysFont('sans-serif', 160, True)

        self.rendered_text1 = self.font.render('Made in Python', True, (255, 0, 0))
        self.rendered_text2 = self.font.render('By SirBergue', True, (255, 0, 0))

        self.text_rect = self.rendered_text1.get_rect(center=(
            self.width // 2,
            self.height // 2)
        )

        self.state = self.ST_FADEIN
        self.last_state_change = time.time()

        self.Run()

    def PollEvents(self):
        # Check for events
    	for event in pygame.event.get():
    	    if event.type == pygame.QUIT:
    	        pygame.quit()
    	        quit()

    def Update(self):
        # Update the state
        self.state_time = time.time() - self.last_state_change

        if self.state == self.ST_FADEIN:
            if self.state_time >= self.FADE_IN_TIME:
                self.state = self.ST_FADEOUT

                self.state_time -= self.FADE_IN_TIME
                self.last_state_change = time.time() - self.state_time

            self.alpha = (1.0 * self.state_time / self.FADE_IN_TIME)
            self.rt = self.rendered_text1

        elif self.state == self.ST_FADEOUT:
            if self.state_time >= self.FADE_OUT_TIME:
                if self.parent_conn.recv() == True:
                	self.parent_conn.send(True)
                	self.parent_conn.close()

                pygame.quit()
                quit()

            self.alpha = 1.0 - (1.0 * self.state_time / self.FADE_OUT_TIME)
            self.rt = self.rendered_text2

        self.surf2 = pygame.surface.Surface((self.text_rect.width, self.text_rect.height))
        self.surf2.set_alpha(255 * self.alpha)

    def Draw(self):
        self.screen.fill((0, 0, 0))

        self.surf2.blit(self.rt, (0, 0))
        self.screen.blit(self.surf2, self.text_rect)

        pygame.display.flip()

    def Run(self):
        while True:
            self.PollEvents()
            self.Update()
            self.Draw()

            self.clock.tick(60)

    def LoadGame(self, conn):
        from Sources import Loader
        Loader.Loader(conn)

Launcher()
