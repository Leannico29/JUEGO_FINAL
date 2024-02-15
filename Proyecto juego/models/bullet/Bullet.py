import pygame as pg
from models.auxiliar import SurfaceManager as sf
from models.constantes import ANCHO_VENTANA

class Bullet(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direction):
        super().__init__()
        self.direction = direction
        self.bullet_images = sf.get_surface_from_spritesheet('models\\bullet\\bullet.png', 1, 1)
        self.image = self.bullet_images[0].copy()
        self.rect = self.image.get_rect(midtop=(pos_x, pos_y))
        self.speed = 10  

    def do_shoot(self, surfaces):
        if self.direction == 'True':
            self.rect.x += self.speed
            if self.rect.x >= ANCHO_VENTANA or self.check_collision(surfaces):
                self.kill()
        elif self.direction == 'False':
            self.rect.x -= self.speed
            if self.rect.x <= 0 or self.check_collision(surfaces):
                self.kill()

    def check_collision(self, surfaces):
        return pg.sprite.spritecollideany(self, surfaces)

    def update(self, delta_ms, surfaces):
        self.do_shoot(surfaces)
        self.animate()

    def animate(self):
        self.image = self.bullet_images[0].copy()