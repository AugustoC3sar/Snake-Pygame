import pygame
import random
import config as cfg
from pygame.constants import *
from window import Window
from snake import Snake

class Controller:
    def __init__(self):
        self._window = Window()
        self._snake = Snake([cfg.DEFAULT_HEAD, cfg.DEFAULT_BP1, cfg.DEFAULT_BP2])
        self._fruit = pygame.Rect(0,0,cfg.PIXEL,cfg.PIXEL)
        self._running = True
        self._game_in_progress = True
        self._paused = False
        self._score = 0
        self._highscore = 0
        pygame.key.set_repeat()

    def run(self):
        clock = pygame.time.Clock()
        self.generate_fruit()
        while self._running:
            clock.tick(cfg.FPS)
            if self._game_in_progress and not self._paused:
                self._snake.move()
                self.check_collisions()
                self.check_new_highscore()
            self._window.display(self._snake, self._fruit, self._score, self._highscore, self._game_in_progress, self._paused)
            for event in pygame.event.get():
                if event.type == QUIT:
                    self._running = False
                if event.type == KEYDOWN:
                    self.keyboard_input()
            
            pygame.display.update()

    def draw_snake(self):
        for segment in self.__snake.body:
            pygame.draw.rect(self.__root, segment.color, segment.hitbox)

    def keyboard_input(self):
        keys = pygame.key.get_pressed()
        if not self._paused:
            if keys[K_w]:
                self._snake.set_direction(1)
            elif keys[K_s]:
                self._snake.set_direction(3)
            elif keys[K_d]:
                self._snake.set_direction(2)
            elif keys[K_a]:
                self._snake.set_direction(4)
        if keys[K_p] and self._game_in_progress:
            if self._paused:
                self.unpause()
            else:
                self.pause()
        if keys[K_q]:
            exit(1)
        if keys[K_r]:
            if not self._game_in_progress:
                self.restart();

    def generate_fruit(self):
        test = True
        while test:
            x = random.randrange(0,cfg.WIDTH-cfg.PIXEL,cfg.PIXEL)
            y = random.randrange(cfg.MARGIN,cfg.HEIGHT-cfg.PIXEL,cfg.PIXEL)
            self._fruit.update(x,y,cfg.PIXEL, cfg.PIXEL)
            test = self.fruit_aux()

    def fruit_aux(self):
        for segment in self._snake.body():
            if self._fruit.colliderect(segment.hitbox()):
                repeat = True
                break
            else:
                repeat = False
        return repeat

    def check_collisions(self):
        head = self._snake.body()[0]
        if head.hitbox().colliderect(self._fruit):
            self._snake.new_body()
            self.generate_fruit()
            self._score += 1
        for pos,segment in enumerate(self._snake.body()):
            if pos > 1:
                if segment.hitbox().colliderect(head.hitbox()):
                    self._game_in_progress = False

    def check_new_highscore(self):
        if self._score > self._highscore:
            self._highscore = self._score

    def pause(self):
        self._paused = True
    
    def unpause(self):
        self._paused = False

    def restart(self):
        self._score = 0
        self._snake = Snake([cfg.DEFAULT_HEAD, cfg.DEFAULT_BP1, cfg.DEFAULT_BP2])
        self.generate_fruit()
        self._game_in_progress = True
