import config as cfg
from pygame.rect import Rect

class Snake:
    def __init__(self, positions):
        self._positions = positions
        self._body = []
        self.init_body()
        self._direction = 2
    
    def body(self):
        return self._body

    def init_body(self):
        self._body.append(Body(self._positions[0][0], self._positions[0][1], cfg.HEAD_COLOR))
        self._body.append(Body(self._positions[1][0], self._positions[1][1], cfg.BODY_COLOR))
        self._body.append(Body(self._positions[2][0], self._positions[2][1], cfg.BODY_COLOR))

    def positions(self):
        return self._snake_positions

    def set_positions(self, new_value):
        self.__snake_positions = new_value

    def direction(self):
        return self._direction

    def set_direction(self, new_dir):
        # UP - 1
        # RIGHT - 2
        # DOWN - 3
        # LEFT - 4
        if (new_dir == 1):
            if self._direction != 3:
                self._direction = new_dir
        elif (new_dir == 2):
            if self._direction != 4:
                self._direction = new_dir
        elif (new_dir == 3):
            if self._direction != 1:
                self._direction = new_dir
        else:
            if self._direction != 2:
                self._direction = new_dir

    def new_body(self):
        new_body_x, new_body_y = self._positions[-1]
        new_body = Body(new_body_x, new_body_y)
        self._positions.append(self._positions[-1])
        self._body.append(new_body)

    def move(self):
        head_x_position, head_y_position = self._positions[0]
        if self._direction == 1:
            new_head_positions = (head_x_position, head_y_position-cfg.PIXEL)
            if new_head_positions[1] < cfg.MARGIN:
                new_head_positions = (head_x_position, cfg.HEIGHT-cfg.PIXEL)
        elif self._direction == 3:
            new_head_positions = (head_x_position, head_y_position+cfg.PIXEL)
            if new_head_positions[1] == cfg.HEIGHT:
                new_head_positions = (head_x_position, cfg.MARGIN)
        elif self._direction == 4:
            new_head_positions = (head_x_position-cfg.PIXEL, head_y_position)
            if new_head_positions[0] < 0:
                new_head_positions = (cfg.WIDTH-cfg.PIXEL, head_y_position)
        elif self._direction == 2:
            new_head_positions = (head_x_position+cfg.PIXEL, head_y_position)
            if new_head_positions[0] == cfg.WIDTH:
                new_head_positions = (0, head_y_position)
        
        self._positions = [new_head_positions] + self._positions[:-1]
        for segment, position in zip(self._body, self._positions):
            segment.set_position(position[0], position[1])


class Body:
    def __init__(self, x, y, color=(100,100,200)):
        self._x = x
        self._y = y
        self._color = color
        self._hitbox = Rect(self._x, self._y, cfg.PIXEL, cfg.PIXEL)

    def x(self):
        return self._x

    def y(self):
        return self._y

    def set_position(self, x, y):
        self._x = x
        self._y = y
        self.update_hitbox()

    def color(self):
        return self._color

    def hitbox(self):
        return self._hitbox

    def update_hitbox(self):
        self._hitbox.update(self._x, self._y, cfg.PIXEL, cfg.PIXEL)
