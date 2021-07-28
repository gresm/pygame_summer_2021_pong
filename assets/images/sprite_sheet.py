from typing import Dict, Tuple
import json
import pygame as pg
import os


class SpriteSheet:
    def __init__(self, source: pg.Surface, info: Dict[str, Tuple[int, int, int, int]], scale: float = 1):
        self.source = source
        self.info = info
        self.images = dict()
        self.scale = scale
        self.generate()

    def generate(self):
        for image in self.info:
            self.images[image] = self.get_subsurface(image)

    def get(self, name: str):
        return self.images[name]

    def get_subsurface(self, name: str) -> pg.Surface:
        cords = self.info[name]
        if self.scale == 1:
            return self.source.subsurface(pg.Rect(cords))
        raw_image = self.source.subsurface(pg.Rect(cords))
        return pg.transform.scale(raw_image, (int(raw_image.get_width() * self.scale),
                                              int(raw_image.get_height() * self.scale)))


def load_sprite_sheet(sheet: str, info: str, scale: float = 1):
    return SpriteSheet(load_image(sheet), json.load(open(get_path(info))), scale)


def load_image(name: str):
    return pg.image.load(get_path(name)).convert_alpha()


def get_path(name: str):
    return os.path.join(os.path.abspath(""), "assets", "images", name)
