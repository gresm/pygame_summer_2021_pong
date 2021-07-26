import pygame as pg
from pygame.font import SysFont
from assets.source.button import Button
from assets.source.switch_case import switch, case


def multiply_vec(vec1: pg.Vector2, vec2: pg.Vector2):
    return pg.Vector2(vec1.x * vec2.x, vec1.y * vec2.y)


class App:
    all_keycodes = tuple(getattr(pg.constants, key_str) for key_str in
                         filter(lambda k: k.startswith("K_"), dir(pg.constants)))
    fps = 30

    def __init__(self):
        self.screen = pg.display.set_mode((1024, 512))
        pg.display.set_caption("Pong")
        pg.display.set_icon(self.screen)
        self.game = Game(self)
        self.menu = Menu(self)
        self.settings = Settings(self)
        self.scene = self.game
        self.done = False
        self.clock = pg.time.Clock()

    def draw(self):
        self.screen.blit(pg.transform.scale2x(self.scene.draw()), (0, 0))
        pg.display.update()

    def update(self):
        self.scene.update()

    def run(self):
        while not self.done:
            self.update()
            self.draw()
            self.handle_events()
            self.handle_input()
            self.clock.tick(self.fps)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True

    def handle_input(self):
        keys_pressed = pg.key.get_pressed()
        for keycode in self.all_keycodes:
            if keys_pressed[keycode]:
                self.scene.handle_input(keycode)


class Player(pg.sprite.Sprite):
    friction = 0.9
    up_force = pg.Vector2(0, -10)
    down_force = pg.Vector2(0, 10)

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
        # old_pos = self.pos
        self.pos = self.pos + self.vel
        self.vel *= self.friction

        self.clamp_pos()

        if self.last_press > 0:
            self.last_press -= 1

    def up(self):
        self.vel += self.up_force

    def down(self):
        self.vel += self.down_force

    def control(self, mode: int):
        if self.last_press:
            self.move_buffer = mode
        else:
            if mode == 1:
                self.up()
                self.last_press += self.control_delay
                self.move_buffer = 0
            elif mode == 2:
                self.down()
                self.last_press += self.control_delay
                self.move_buffer = 0

    def clamp_pos(self):
        if self.hit_box.left < self.walls.left:
            self.pos.x = self.walls.left + 1
        if self.hit_box.right > self.walls.right:
            self.pos.x = self.walls.right - self.hit_box.w - 1
        if self.hit_box.top < self.walls.top:
            self.pos.y = self.walls.top + 1
        if self.hit_box.bottom > self.walls.bottom:
            self.pos.y = self.walls.bottom - self.hit_box.h - 1


class Ball(pg.sprite.Sprite):
    friction = 0.99
    horizontal = pg.Vector2(-1, 1)
    vertical = pg.Vector2(1, -1)

    def __init__(self, pos: pg.Vector2, vel: pg.Vector2, hit_box: pg.Rect, image: pg.Surface, walls: pg.Rect):
        super().__init__()
        self.pos = pos
        self.vel = vel
        self._hit_box = hit_box
        self.hit_box_offset = pg.Vector2(hit_box.x, hit_box.y)
        self.image = image
        self.size = self.image.get_size()
        self.walls = walls

    @property
    def hit_box(self):
        return pg.Rect(*(self.pos + self.hit_box_offset), self._hit_box.w, self._hit_box.h)

    @property
    def rect(self):
        return pg.Rect(*self.pos, *self.size)

    def update(self, *args, **kwargs) -> None:
        self.pos += self.vel
        self.bounce()
        self.clamp_pos()

    def bounce(self):
        if self.hit_box.left < self.walls.left:
            self.vel = multiply_vec(self.vel, self.horizontal)
            self.pos += self.vel
        if self.hit_box.right > self.walls.right:
            self.vel = multiply_vec(self.vel, self.horizontal)
            self.pos += self.vel
        if self.hit_box.top < self.walls.top:
            self.vel = multiply_vec(self.vel, self.vertical)
            self.pos += self.vel
        if self.hit_box.bottom > self.walls.bottom:
            self.vel = multiply_vec(self.vel, self.vertical)
            self.pos += self.vel

    def clamp_pos(self):
        if self.hit_box.left < self.walls.left:
            self.pos.x = self.walls.left + 21
        if self.hit_box.right > self.walls.right:
            self.pos.x = self.walls.right + self.hit_box.w - 21
        if self.hit_box.top < self.walls.top:
            self.pos.y = self.walls.top + self.vel.y + 21
        if self.hit_box.bottom > self.walls.bottom:
            self.pos.y = self.walls.bottom + self.hit_box.h - 21


class Scene:
    app = None

    def __init__(self, app):
        self.app = self.app or app

    def draw(self) -> pg.Surface:
        pass

    def update(self):
        pass

    def handle_input(self, k_id: int):
        pass

    def handle_event(self):
        pass


class Game(Scene):
    def __init__(self, app: App):
        super(Game, self).__init__(app)
        pl_img = pg.Surface((10, 50))
        pl_img.fill((255, 255, 255))
        bl_img = pg.Surface((10, 10))
        bl_img.fill((255, 255, 255))
        self.player = Player(pg.Vector2(10, 128), pg.Rect(0, 0, 10, 50), pl_img, pg.Rect(0, 0, 512, 256), 10)
        self.bot = Player(pg.Vector2(502, 128), pg.Rect(0, 0, 10, 50), pl_img, pg.Rect(0, 0, 512, 256), 10)
        self.ball = Ball(pg.Vector2(256, 128), pg.Vector2(-5, -5), pg.Rect(0, 0, 10, 10), bl_img, pg.Rect(0, 0, 512, 256))
        self.players_group = pg.sprite.Group(self.player, self.bot)
        self.balls_group = pg.sprite.Group(self.ball)

    def draw(self):
        screen = pg.Surface((512, 256))
        self.players_group.draw(screen)
        self.balls_group.draw(screen)
        return screen

    def update(self):
        self.players_group.update()
        self.balls_group.update()

        # bot control
        if self.bot.hit_box.centery > self.ball.hit_box.centery:
            self.bot.control(1)
        if self.bot.hit_box.centery < self.ball.hit_box.centery:
            self.bot.control(2)

    def handle_input(self, k_id: int):
        with switch(k_id):
            # noinspection PyCallingNonCallable
            if case(pg.K_w):
                self.player.control(1)
            # noinspection PyCallingNonCallable
            if case(pg.K_s):
                self.player.control(2)


class Menu(Scene):

    def __init__(self, app):
        super(Menu, self).__init__(app)

        def click():
            self.app.scene = self.app.game
#       self.start_button = Button(self.app.screen, (100, 100), ["start game"], SysFont, action=click)


class Settings(Scene):
    pass
