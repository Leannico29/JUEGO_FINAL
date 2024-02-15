import pygame as pg
from models.auxiliar import SurfaceManager as sf

class Trampas(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.images = sf.get_surface_from_spritesheet('models\\trampas\\Idle.png', 1, 1)
        self.image = self.images[0].copy()
        self.image = pg.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.image_index = 0
        self.__daño = 25

    

    def update(self, player):
        if self.rect.colliderect(player.rect):
            return True

    def animate(self):
        self.image_index = (self.image_index + 1) % len(self.images)
        self.image = self.images[self.image_index].copy()
        self.image = pg.transform.scale(self.image, self.rect.size)