from typing import Union, List, Tuple, Callable, Optional

import pygame as p
from pygame.font import FontType, get_default_font, SysFont
from pygame.math import Vector2
from pygame.sprite import Sprite

from assets.images.sprite_sheet import load_image

COLOR = Union[p.Color, Tuple[int, int, int], Tuple[int, int, int, int]]



class Button:

    def __init__(self, screen: p.Surface = None,
                 position: Union[Vector2, Tuple[int, float]] = (0, 0),
                 texts: Optional[List[str]] = None, texts_font: Optional[List[FontType]] = None,
                 texts_color: Optional[List[COLOR]] = None, texts_bg_color: Optional[List[COLOR]] = None,
                 imgs: Optional[List[Union[str, p.Surface, Sprite]]] = None, render: bool = False,
                 action: Callable = None, swapping_back: bool = False):
        self.swapping_back = swapping_back
        if texts is not None:
            self.click_range = range(len(texts))
        elif imgs is not None:
            self.click_range = range(len(imgs))
        self.swap = 0
        self.position = Vector2(position)
        if texts is not None:
            if texts_font is None:
                texts_font = SysFont(get_default_font(), 20)
            if texts_color is None:
                texts_color = p.color.Color(255, 255, 255)
            for i in range(self.click_range.stop):
                text_r = [texts_font[i].render(texts[i], True, texts_color),
                          texts_font[i].render(texts[i], True, texts_color)]
                size = [text_r[i].get_size(), text_r[i].get_size()]
                self.display = [p.Surface(size[i]), p.Surface(size[i])]
            if texts_bg_color is not None:
                for i in range(self.click_range.stop):
                    self.display[i].fill(texts_bg_color[i])
            for i in range(self.click_range.stop):
                # noinspection PyUnboundLocalVariable
                self.display[i].blit(text_r[0], (0, 0))
            self.rect = []
            for i in range(self.click_range.stop):
                # noinspection PyUnboundLocalVariable
                self.rect.append(p.Rect(self.position.x, self.position.y, size[i][0], size[i][1]))
        elif imgs is not None:
            if isinstance(imgs[0], str):
                for i in range(self.click_range.stop):
                    self.display[i] = load_image(imgs[i])
            elif isinstance(imgs[0], Sprite):
                for i in range(self.click_range.stop):
                    self.display[i] = imgs[i].image
            elif isinstance(imgs[0], p.Surface):
                for i in range(self.click_range.stop):
                    self.display[i] = imgs[1]
            else:
                raise ValueError
            self.rect = []
            for i in range(self.click_range.stop):
                self.rect.append(imgs[i].rect)
        else:
            raise ValueError
        if render and screen is not None:
            self.render()
        if action is not None:
            self.click = action
        self.screen = screen

    def render(self):
        self.screen.blit(self.display[self.swap], (self.position.x, self.position.y))

    def click(self):
        """
        to overwrite
        :return:
        :rtype:
        """
        if self.swapping_back:
            self.swap += self.click_range.step
            if self.swap > self.click_range.stop:
                self.swap -= self.click_range.stop
        else:
            if self.swap + self.click_range.step <= self.click_range.stop:
                self.swap += self.click_range.step

    def check_click(self, cursor_pos):
        cursor_pos = list(cursor_pos)
        cursor_pos[0] -= self.position.x
        cursor_pos[1] -= self.position.y
        if cursor_pos[0] in range(self.rect[self.swap].height) and cursor_pos[1] in range(self.rect[self.swap].width):
            self.click()
