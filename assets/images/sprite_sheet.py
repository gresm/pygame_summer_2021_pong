from typing import Dict, Tuple
import json
import pygame as pg
import os


class SpriteSheet:
    def __init__(self, source: pg.Surface, info: Dict[str, Tuple[int, int, int, int]]):
        self.source = source
        self.info = info
        self.images = {}
        self.generate()

    def generate(self):
        for image in self.info:
            self.images[image] = self.source.subsurface(pg.Rect(self.images[image]))

    def get(self, name: str):
        return self.images[name]


def load_sprite_sheet(sheet: str, info: str):
    return SpriteSheet(load_image(sheet), json.load(open(info)))


def load_image(name: str):
    return pg.image.load(os.path.abspath("") + "/asserts/graphics/" + name)
