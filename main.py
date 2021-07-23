import pygame
import random
from pygame.constants import *


pygame.font.init()
HELV30 = pygame.font.SysFont('Helvetica',30)
WIDTH, HEIGHT = 500, 540
FPS = 20
PIXEL = 20
MARGIN = 40

class Engine:
    def __init__(self):
        self.__root = pygame.display.set_mode((WIDTH, HEIGHT))
        self.__snake = Snake([DEFAULT_HEAD, DEFAULT_BP1, DEFAULT_BP2], [(60, 60),(40,60),(20,60)])
        self.__fruit = pygame.Rect(0,0,PIXEL,PIXEL)
        self.__run = True
        self.__end = False
        self.__mouse_pos = (0,0)

    def game_loop(self):
        clock = pygame.time.Clock()
        self.generate_fruit()
        while self.__run:
            clock.tick(FPS)
            if self.__end:
                self.end_game_screen()
            else:
                self.__root.fill((50,100,50))
                self.draw_snake()
                self.playing_display()
                self.__snake.move()
                self.get_key()
                self.draw_fruit()
                self.check_collisions()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.__run = False
                elif event.type == MOUSEBUTTONDOWN:
                    self.get_mouse_pos()
            
            pygame.display.update()

    def draw_snake(self):
        for segment in self.__snake.body:
            pygame.draw.rect(self.__root, segment.color, segment.hitbox)

    def get_key(self):
        keys = pygame.key.get_pressed()
        if keys[K_w]:
            if self.__snake.direction == 'DOWN':
                pass
            else:
                self.__snake.direction = 'UP'
        elif keys[K_s]:
            if self.__snake.direction == 'UP':
                pass
            else:
                self.__snake.direction = 'DOWN'
        elif keys[K_d]:
            if self.__snake.direction == 'LEFT':
                pass
            else:
                self.__snake.direction = 'RIGHT'
        elif keys[K_a]:
            if self.__snake.direction == 'RIGHT':
                pass
            else:
                self.__snake.direction = 'LEFT'

    def playing_display(self):
        bg = pygame.draw.rect(self.__root, (0,0,0), pygame.Rect(0,0,WIDTH,MARGIN))
        score_label = HELV30.render(f'Score: {self.__snake.score}', False, (255,255,255))
        self.__root.blit(score_label, (5,5))

    def generate_fruit(self):
        test = True
        while test:
            x = random.randrange(0,500-PIXEL,PIXEL)
            y = random.randrange(MARGIN,HEIGHT-PIXEL,PIXEL)
            self.__fruit.update(x,y,PIXEL, PIXEL)
            test = self.fruit_aux()

    def fruit_aux(self):
        for segment in self.__snake.body:
            if self.__fruit.colliderect(segment.hitbox):
                repeat = True
                break
            else:
                repeat = False
        return repeat

    def draw_fruit(self):
        pygame.draw.rect(self.__root, (255,0,0), self.__fruit)

    def check_collisions(self):
        head = self.__snake.body[0]
        if head.hitbox.colliderect(self.__fruit):
            self.__snake.new_body()
            self.generate_fruit()
            self.__snake.score += 1
        for pos,segment in enumerate(self.__snake.body):
            if pos > 1:
                if segment.hitbox.colliderect(head.hitbox):
                    self.__end = True
        
    def end_game_screen(self):
        bg = pygame.draw.rect(self.__root, (0,0,0), pygame.Rect(0,0,WIDTH,HEIGHT))
        lose_info = HELV30.render('YOU LOSE!', False, (255,255,255))
        lose_rect = lose_info.get_rect(center=(WIDTH/2, (HEIGHT/2)-50))
        self.__root.blit(lose_info, lose_rect)
        play_again = HELV30.render('Play again?',False, (255,255,255))
        play_again_rect = play_again.get_rect(center=(WIDTH/2, (HEIGHT/2)))
        self.__root.blit(play_again, play_again_rect)
        yes = HELV30.render('YES', False, (255,255,255))
        yes_rect = yes.get_rect(center=((WIDTH/2)-50, (HEIGHT/2)+60))
        self.__root.blit(yes, yes_rect)
        no = HELV30.render('NO', False, (255,255,255))
        no_rect = no.get_rect(center=((WIDTH/2)+50, (HEIGHT/2)+60))
        self.__root.blit(no, no_rect)
        if no_rect.collidepoint(self.__mouse_pos):
            self.__run = False
        elif yes_rect.collidepoint(self.__mouse_pos):
            self.reset()

    def get_mouse_pos(self):
        self.__mouse_pos = pygame.mouse.get_pos()

    def reset(self):
        self.__snake.score = 0
        self.__snake.snake_positions = [(60, 60),(40,60),(20,60)]
        self.__snake.body.clear()
        self.__snake.body = [DEFAULT_HEAD, DEFAULT_BP1, DEFAULT_BP2]
        self.generate_fruit()
        self.__end = False




class Snake:
    def __init__(self, body, positions):
        self.__body = body
        self.__snake_positions = positions
        self.__direction = 'RIGHT'
        self.__score = 0
    
    @property
    def body(self):
        return self.__body

    @body.setter
    def body(self, new_value):
        self.__body = new_value

    @property
    def snake_positions(self):
        return self.__snake_positions

    @snake_positions.setter
    def snake_positions(self, new_value):
        self.__snake_positions = new_value

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, new_dir):
        self.__direction = new_dir

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, new_score):
        self.__score = new_score

    def new_body(self):
        new_body_x, new_body_y = self.__snake_positions[-1]
        new_body = Body(new_body_x, new_body_y)
        self.__snake_positions.append(self.__snake_positions[-1])
        self.__body.append(new_body)
        

    def move(self):
        head_x_position, head_y_position = self.__snake_positions[0]
        if self.__direction == 'UP':
            new_head_positions = (head_x_position, head_y_position-PIXEL)
            if new_head_positions[1] < MARGIN:
                new_head_positions = (head_x_position, HEIGHT-PIXEL)
        elif self.__direction == 'DOWN':
            new_head_positions = (head_x_position, head_y_position+PIXEL)
            if new_head_positions[1] == HEIGHT:
                new_head_positions = (head_x_position, MARGIN)
        elif self.__direction == 'LEFT':
            new_head_positions = (head_x_position-PIXEL, head_y_position)
            if new_head_positions[0] < 0:
                new_head_positions = (WIDTH-PIXEL, head_y_position)
        elif self.__direction == 'RIGHT':
            new_head_positions = (head_x_position+PIXEL, head_y_position)
            if new_head_positions[0] == WIDTH:
                new_head_positions = (0, head_y_position)
        self.__snake_positions = [new_head_positions] + self.__snake_positions[:-1]
        for segment, position in zip(self.__body, self.__snake_positions):
            segment.x = position[0]
            segment.y = position[1]
            segment.update_hitbox()


class Body:
    def __init__(self, x, y, color=(100,100,200)):
        self.__x = x
        self.__y = y
        self.__color = color
        self.__hitbox = pygame.Rect(self.__x, self.__y, PIXEL, PIXEL)

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, new_x):
        self.__x = new_x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, new_y):
        self.__y = new_y

    @property
    def color(self):
        return self.__color

    @property
    def hitbox(self):
        return self.__hitbox

    def update_hitbox(self):
        self.__hitbox.update(self.__x, self.__y, PIXEL, PIXEL)


DEFAULT_HEAD = Body(60,60,(50,50,150))
DEFAULT_BP1 = Body(40,60)
DEFAULT_BP2 = Body(20,60)

game = Engine()
game.game_loop()
