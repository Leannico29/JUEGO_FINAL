import pygame as pg
from models.botones.botones import Botones
from stage_1_ import *
from models.constantes import *
from defs_auxiliares import *
from models.player.player import Player
from models.bullet.Bullet import Bullet
from models.enemy.enemy import Enemy
from models.fruit.fruta import Fruta
from models.plataformas.piso import Plataforma
from models.trampas.trampas import Trampas

screen = pg.display.set_mode((ANCHO_VENTANA, LARGO_VENTANA))
pg.init()
pg.display.set_caption("Menu Principal")
back_img = pg.image.load('models\\backgrounds\Pink.png') 
back_img =  pg.transform.scale(back_img,(ANCHO_VENTANA, LARGO_VENTANA))
menu = True

boton_start = Botones((ANCHO_VENTANA * 0.2),(LARGO_VENTANA // 2),'models\\botones\start.png',0.3)
boton_stop = Botones((ANCHO_VENTANA * 0.6),(LARGO_VENTANA // 2),'models\\botones\stop.png',0.3)

while menu:


    lista_eventos = pg.event.get()
    for event in lista_eventos:
        match event.type:
            case pg.QUIT:
                print('Adios')
                menu = False

    screen.blit(back_img, back_img.get_rect())  
    if boton_start.update():
        stage_uno()
        menu = False

    if boton_stop.update():
        menu = False

    
    boton_start.draw(screen)       
    boton_stop.draw(screen)        
    pg.display.update()

pg.quit()