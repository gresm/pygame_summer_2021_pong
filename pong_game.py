import pygame as pg
from enum import Enum


class App:

    def __init__(self):
        self.screen = pg.display.set_mode((256, 512))
        pg.display.set_caption("Pong")
        pg.display.set_icon(self.screen)
        self.game = Game(self)
        self.menu = Menu(self)
        self.settings = Settings(self)
        self.scene = Scenes.menu


    def draw(self):
        ...


class Player(pg.sprite.Sprite):
    friction = 0.99
    up_force = pg.Vector2(0, -1)
    down_force = pg.Vector2(0, 1)

    def __init__(self, pos: pg.Vector2, hit_box: pg.Rect, image: pg.Surface, walls: pg.Rect, control_delay: int):
        super().__init__()
        self.pos = pos
        self.vel = pg.Vector2(0, 0)
        self._hit_box = hit_box
        self.hit_box_offset = pg.Vector2(hit_box.x, hit_box.y)
        self.image = image
        self.size = self.image.get_size()
        self.walls = walls
        self.control_delay = control_delay
        self.last_press = 0
        self.move_buffer = 0

    @property
    def hit_box(self):
        return pg.Rect(*(self.pos + self.hit_box_offset), self._hit_box.w, self._hit_box.h)

    @property
    def rect(self):
        return pg.Rect(*self.pos, *self.size)

    def update(self, *args, **kwargs) -> None:
        old_pos = self.pos
        self.pos = self.pos + self.vel
        self.vel *= self.friction

        if not self.walls.contains(self.hit_box):
            self.pos = old_pos

        if self.last_press > 0:
            self.last_press -= 1
        else:
            self.control(self.move_buffer)

    def up(self):
        self.vel += self.up_force

    def down(self):
        self.vel += self.down_force

    def control(self, mode: int):
        if self.last_press:
            if self.move_buffer:
                return
            self.move_buffer = mode
        else:
            if mode == 1:
                self.up()
                self.last_press += self.control_delay
            elif mode == 2:
                self.down()
                self.last_press += self.control_delay


class Ball:
    friction = 0.99
    up_force = pg.Vector2(0, -1)
    down_force = pg.Vector2(0, 1)
    left_force = pg.Vector2(-1, )
    right_force = pg.Vector2(1, 0)

    def __init__(self, pos: pg.Vector2, hit_box: pg.Rect, image: pg.Surface, walls: pg.Rect):
        super().__init__()
        self.pos = pos
        self.vel = pg.Vector2(0, 0)
        self.hit_box = hit_box
        self.image = image
        self.size = self.image.get_size()
        self.walls = walls

    @property
    def rect(self):
        return pg.Rect(*self.pos, *self.size)

    def update(self, *args, **kwargs) -> None:
        self.pos += self.vel


class Scenes(Enum):
    menu = 1
    settings = 2
    game = 3


class Scene:
    app = None

    def __init__(self, app):
        self.app = self.app or app

    def draw(self):
        pass


class Game(Scene):

    def __init__(self, app):
        super(Game, self).__init__(app)
        self.player: Player = ...
        self.loop()

    def loop(self):
        go = True
        while go:
            pressed = pg.key.get_pressed()
            if pressed[pg.K_a]:
                self.player.up()
            elif pressed[pg.K_a]:
                self.player.down()
            elif pressed[pg.K_ESCAPE]:
                go = False


class Menu(Scene):
    pass


class Settings(Scene):
    pass
