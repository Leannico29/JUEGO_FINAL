import pygame as pg
import random
from models.constantes import *
from defs_auxiliares import *
from models.player.player import Player
from models.bullet.Bullet import Bullet
from models.enemy.enemy import Enemy
from models.fruit.fruta import Fruta
from models.plataformas.piso import plataforma
from models.trampas.trampas import Trampas
from dataloader import *


#def stage_1():
screen = pg.display.set_mode((ANCHO_VENTANA, LARGO_VENTANA))
pg.init()
pg.display.set_caption("Let's destroy Missigno")
back_img = pg.image.load('models\\backgrounds\\fondo.jpeg') 
back_img =  pg.transform.scale(back_img,(ANCHO_VENTANA, LARGO_VENTANA))
shoots_flag = True
clock = pg.time.Clock()
font = pg.font.Font(None, 37)
game = True
puntos = 0


try:
    player = Player(70, 525, frame_rate = 100, speed_walk = 50, speed_run = 75, gravity = 20, jump = 70, vida = 100)
except Exception as ex:
    print(f"No fue posible crear al personaje: {ex}")

try:
    enemy = Enemy(200, 75, frame_rate=120, speed_walk=20)
except Exception as ex:
    print(f"No fue posible crear al enemigo: {ex}")



surfaces = pg.sprite.Group()
enemy_group = pg.sprite.Group()
enemy_group.add(enemy)
sound_bullet = pg.mixer.Sound('music\sonido disparo.mp3')

##############################################################################
piso = plataforma(0, LARGO_VENTANA - 70, ANCHO_VENTANA, LARGO_VENTANA)
plataform_1 = plataforma(0, 455, 75, 75)
plataform_2 = plataforma(200, 255, 400, 50)
plataform_3 = plataforma(75, 455, 75, 75)
plataform_4 = plataforma(525,455,75,75)
plataform_5 = plataforma(525,380,75,75)
plataform_6 = plataforma(525,305,75,75)
plataformas = [
    piso, plataform_1, plataform_2, 
    plataform_3,plataform_4,plataform_5,
    plataform_6
    ]
###############################################################################
frutas = pg.sprite.Group()
fruta = Fruta(590, 450, 50,50)
frutas.add(fruta)
################################################################################
trampas = pg.sprite.Group()
trampa_uno = Trampas(0,425,30,30)
trampa_dos = Trampas(30,425,30,30)
trampa_tres = Trampas(230,225,30,30)
trampa_cuatro = Trampas(260,225,30,30)
trampa_cinco = Trampas(290,225,30,30)
trampas.add(trampa_uno,trampa_dos,trampa_tres,trampa_cuatro,trampa_cinco)

######################
cooler_disparo = 0
cooler_disparo_enemigo = 0
cooler_colision = 0
cooler_daño_al_enemigo = 0
cooler_mov_enem = 50
cooler_reaparicion = 0
contador_toques = 0
contador_enemigos = 1
######################
color = None
##############################
vida_inicial = 100
vida = 100
enemigo_puede_disparar = False
##############################

#############################
clock = pg.time.Clock()
tiempo_transcurrido = 0
points = 0
font = pg.font.Font(None, 37)
texto_uno = 'Game over'
texto_dos = 'Ganaste!!'
##############################

pg.mixer.init()


##############################

while game:


    lista_eventos = pg.event.get()
    lista_teclas_presionadas = pg.key.get_pressed()
    for event in lista_eventos:
        match event.type:
            case pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    player.jump()
            case pg.QUIT:
                print('Adios')
                game = False
                
    if lista_teclas_presionadas[pg.K_RIGHT] and not lista_teclas_presionadas[pg.K_LEFT]:
        player.walk('Right')
    if lista_teclas_presionadas[pg.K_LEFT] and not lista_teclas_presionadas[pg.K_RIGHT]:
        player.walk('Left')
    if lista_teclas_presionadas[pg.K_RIGHT] and lista_teclas_presionadas[pg.K_LSHIFT] and not lista_teclas_presionadas[pg.K_LEFT]:
        player.run('Right')
    if lista_teclas_presionadas[pg.K_LEFT] and lista_teclas_presionadas[pg.K_LSHIFT] and not lista_teclas_presionadas[pg.K_RIGHT]:
        player.run('Left')
    if not lista_teclas_presionadas[pg.K_RIGHT] and not lista_teclas_presionadas[pg.K_LEFT]:
        player.stay()
    if lista_teclas_presionadas[pg.K_q] and cooler_disparo == 0 and player._Player__is_alive:
        player.shoot()
        sound_bullet.play()  
        cooler_disparo += 45

    if cooler_disparo > 0:
        cooler_disparo = resta(cooler_disparo,1)
    if cooler_disparo_enemigo > 0:
        cooler_daño_al_enemigo = coolers(cooler_daño_al_enemigo,1,False)
    if cooler_daño_al_enemigo > 0:
        cooler_daño_al_enemigo = resta(cooler_daño_al_enemigo,1)

    delta_ms = clock.tick(FPS)
    
    ############################################
    for plataforma in plataformas:
            plataforma.draw(screen)
    
    #############################################
    if cooler_daño_al_enemigo == 0:
        for bullet in player.bullet_group:
            hit_enemies = pg.sprite.spritecollide(bullet, enemy_group, True)
            for enemy_hit in hit_enemies:
                enemy_hit.kill()
                points = suma(points, 1000)
                cooler_daño_al_enemigo = coolers(cooler_daño_al_enemigo, 400, True)       
                cooler_reaparicion =  coolers(cooler_reaparicion, 250, True)
                print('murio')


    if enemy._enemy_is_alive and cooler_reaparicion >=1:
        cooler_reaparicion = resta(cooler_reaparicion, 1)

    if cooler_reaparicion == 0 and not enemy._enemy_is_alive:
        if contador_enemigos >= 5:
            enemy = Enemy(200, 0, frame_rate=120, speed_walk=20)
            contador_enemigos = suma(contador_enemigos, 1)
            enemy_group.add(enemy)
        
    ##############################################
    
    if pg.sprite.spritecollideany(player, trampas):
        
        if player._Player__is_alive and cooler_colision == 0:
            contador_toques = suma(contador_toques,1)
            player.hitted()
            cooler_colision = coolers(cooler_colision,90,True)
            print('TE TOCO')

            
            if cooler_colision > 0:
                cooler_colision = resta(cooler_colision,1)

            if contador_toques >= 1 or contador_toques == 0:

                for trampa in trampas:
                    if trampa.rect.colliderect(player.rect):
                        daño_recibido = trampa._Trampas__daño

                player.decrease_life(daño_recibido)

                if player.get_vida() <= 0:
                    player.kill()

                if player.get_vida() > 25 and player.get_vida() < 100:
                    color_vida = amarillo
                elif player.get_vida() == 25 or player.get_vida() == 0:
                    color_vida = rojo
                else:
                    color_vida = verde 
    
    if pg.sprite.spritecollideany(player, enemy_group):

        if player._Player__is_alive and cooler_colision == 0:
            contador_toques = suma(contador_toques,1)
            player.hitted()
            cooler_colision = coolers(cooler_colision,90,True)
            print('TE TOCO')
            
            daño_recibido = enemy.get_daño()
            player.decrease_life(daño_recibido)
            
            if player.get_vida() <= 0:
                player.kill()

            if cooler_colision > 0:
                cooler_colision = resta(cooler_colision,1)

            if contador_toques >= 0:

                if player.get_vida() > 25 and player.get_vida() < 100:
                    color_vida = amarillo
                elif player.get_vida() == 25 or player.get_vida() == 0:
                    color_vida = rojo
                else:
                    color_vida = verde 


    if pg.sprite.spritecollideany(player, frutas):
        player.gain_vida(100)
        vida = player.get_vida()
        points = suma(points,500) 
        print("Vida después de ganar:", player.get_vida())
        print("Puntos después de ganar:", points)
    vida = player.get_vida()
    texto_vida = font.render(f'Vida: {vida}',True,color_vida)



    if cooler_colision > 0:
        cooler_colision = resta(cooler_colision,1)
    if cooler_mov_enem >= 1:
        cooler_mov_enem = resta(cooler_mov_enem,1)

    ###############################################

    if player._Player__is_alive and enemy._enemy_is_alive:
        tiempo_segundos = tiempo_transcurrido // 1000
        minutos = tiempo_segundos // 60
        segundos = tiempo_segundos % 60
        
        color = set_color(minutos,segundos)
            
        if color == rojo:
            Player.kill()

    #############################################################

    if enemigo_puede_disparar and enemy._enemy_is_alive:
        if random.randint(1,23)%2 == 0 and cooler_disparo_enemigo == 0:
            sound_bullet.play()  
            cooler_disparo_enemigo = coolers(cooler_disparo_enemigo,250,True)
            enemy.shoot()
        
    
    #############################################################

    tiempo_texto = font.render(f'{minutos:02}:{segundos:02}', True, color)
    puntos = font.render(f'{points}', True, (255,155,0))
    texto_perdiste = font.render(f'{texto_uno}',True,(rojo))
    texto_ganaste = font.render(f'{texto_dos}',True,(verde))
    #############################################################
    
    if player._Player__is_alive:
        player.draw(screen)
        player.update(delta_ms, plataformas)
        player.handle_ground_collision(plataformas)
        player.handle_collisions(plataformas)
        player.bullet_group.update(delta_ms, surfaces)
        player.bullet_group.draw(screen)
        frutas.update(player)
        
    else:
        screen.blit(texto_perdiste,(((ANCHO_VENTANA/2)-80),(LARGO_VENTANA/2)))
        
        
    if points == 4500:
        screen.blit(texto_ganaste,(((ANCHO_VENTANA/2)-80),(LARGO_VENTANA/2)))
        
    #############################################################
    
    if enemy._enemy_is_alive and player._Player__is_alive:
        enemy.draw(screen)
        enemy.handle_collisions(plataformas)                           
        enemy.handle_ground_collision(plataformas)
        enemy.bullet_group.update(delta_ms, surfaces)
        enemy.bullet_group.draw(screen)
        enemy_group.update(delta_ms,plataformas)
    if not enemy._enemy_is_alive:
        enemy_group.remove(enemy)

    
    enemy.update(delta_ms, plataformas)
    trampas.update(player)
    trampas.draw(screen)
    #############################################################
    fruta.animate()
    frutas.draw(screen)  
    
    pg.display.update()

    
    
    screen.blit(back_img, back_img.get_rect())
    screen.blit(tiempo_texto, (((ANCHO_VENTANA/2)-30) ,5))
    screen.blit(puntos, (5,5))
    screen.blit(texto_vida,(675,5))
    tiempo_transcurrido += delta_ms
pg.quit()