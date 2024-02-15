import pygame as pg
from random import choice
from models.auxiliar import SurfaceManager as sf

class Fruta(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.__banana = sf.get_surface_from_spritesheet('models\\fruit\\Bananas.png', 17, 1)
        self.__apple = sf.get_surface_from_spritesheet('models\\fruit\\Apple.png', 17, 1)
        self.images = choice([self.__banana, self.__apple])
        self.image = self.images[0].copy()
        self.image = pg.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.image_index = 0

    def update(self, player):
        if self.rect.colliderect(player.rect):
            self.kill()

    def animate(self):
        self.image_index = (self.image_index + 1) % len(self.images)
        self.image = self.images[self.image_index].copy()
        self.image = pg.transform.scale(self.image, self.rect.size)
