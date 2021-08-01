import pygame as pg
import os


def get_song(song: str):
    return pg.mixer.Sound(get_path(song))


def get_path(name: str):
    return os.path.join(os.path.abspath(""), "assets", "sounds", name)
