import pygame as pg

class Botones():
    def __init__(self,x,y,image_path,scale):
        self.image = pg.image.load(image_path)  # Carga la imagen desde el archivo
        width = self.image.get_width()
        height = self.image.get_height()
        self.image = pg.transform.scale(self.image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.click = False

    def update(self):
        accion = False
        pos = pg.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and self.click == False:
                self.click = True
                accion = True
        if pg.mouse.get_pressed()[0] == 0:
            self.click = 0
        return accion


    def draw(self, screen):
        screen.blit(self.image, self.rect)