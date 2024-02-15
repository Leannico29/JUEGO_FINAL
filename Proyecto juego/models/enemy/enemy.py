from models.auxiliar import SurfaceManager as sf
import pygame as pg
from models.constantes import ANCHO_VENTANA, DEBUG, LARGO_VENTANA
from models.bullet.Bullet import Bullet
import random

class Enemy(pg.sprite.Sprite):
    def __init__(self, coord_x, coord_y, frame_rate=100, speed_walk=6, gravity=30, life=100):
        super().__init__()
        self.__iddle_r = sf.get_surface_from_spritesheet('models/enemy/enemy.png', 1, 1)
        self.__iddle_l = sf.get_surface_from_spritesheet('models/enemy/enemy.png', 1, 1, flip=True)
        self.__walk_r = sf.get_surface_from_spritesheet('models/enemy/enemy.png', 1, 1)
        self.__walk_l = sf.get_surface_from_spritesheet('models/enemy/enemy.png', 1, 1, flip=True)

        self.__life = life
        self.__direction_change_counter = 0
        self.__direction_change_delay = 3 
        self.__move_x = 0
        self.__move_y = 0
        self.__gravity = gravity
        self.__speed_walk = speed_walk
        self.__frame_rate = frame_rate
        self.__enemy_move_time = 0
        self.__enemy_animation_time = 0
        self.__is_jumping = False
        self.__is_falling = False
        self._enemy_is_alive = True
        self.__initial_frame = 0
        self.__actual_animation = self.__iddle_r
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.__rect = self.__actual_img_animation.get_rect(topleft=(coord_x, coord_y))
        self.rect = self.__rect
        self.__is_looking_right = True
        ##############################################
        self.bullet_group = pg.sprite.Group()
        self.__rect = self.__actual_img_animation.get_rect(topleft = (coord_x, coord_y))
        self.rect = self.__rect
        self.__daño = 25
        #######################################

    def __set_x_animations_preset(self, move_x, animation_list: list[pg.surface.Surface], look_r: bool):
        self.__move_x = move_x
        self.__actual_animation = animation_list
        self.__is_looking_right = look_r

    def walk(self, direction: str = 'Right'):
        match direction:
            case 'Right':
                look_right = True
                self.__set_x_animations_preset(self.__speed_walk, self.__walk_r, look_r=look_right)
            case 'Left':
                look_right = False
                self.__set_x_animations_preset(-self.__speed_walk, self.__walk_l, look_r=look_right)

    def stay(self):
        if self.__actual_animation != self.__iddle_l and self.__actual_animation != self.__iddle_r:
            self.__actual_animation = self.__iddle_r if self.__is_looking_right else self.__iddle_l
            self.__initial_frame = 0
            self.__move_x = 0

    def do_movement(self, delta_ms, plataformas):
        self.__enemy_move_time += delta_ms
        if self.__enemy_move_time >= self.__frame_rate:
            self.__enemy_move_time = 0

            if self.__direction_change_counter > 0:
                self.__direction_change_counter -= 1 

            if random.randint(1,233)%2 == 0 and self.__direction_change_counter == 0 :
                self.__direction_change_counter = 30

                direction = random.choice(['Right', 'Left'])

                if direction == 'Right':
                    self.__set_x_animations_preset(self.__speed_walk, self.__walk_r, look_r=True)
                else:
                    self.__set_x_animations_preset(-self.__speed_walk, self.__walk_l, look_r=False)

            # Movimiento horizontal
            self.__rect.x += self.__set_borders_limits()
            
            # Movimiento vertical
            self.__rect.y += self.__gravity

            # Manejo de colisiones con las plataformas
            self.handle_ground_collision(plataformas)
            self.handle_wall_collision(plataformas)

    def handle_collisions(self, plataformas):
        for platform in plataformas:
            if self.__rect.colliderect(platform.rect_colision_superior):
                # Verificar la dirección del movimiento y ajustarla
                if self.__move_x > 0:
                    # Si se mueve hacia la derecha, cambia la dirección a la izquierda
                    self.__move_x = -self.__speed_walk
                    self.__is_looking_right = False
                elif self.__move_x < 0:
                    # Si se mueve hacia la izquierda, cambia la dirección a la derecha
                    self.__move_x = self.__speed_walk
                    self.__is_looking_right = True

    def handle_wall_collision(self, plataformas):
        for platform in plataformas:
            if self.__rect.colliderect(platform.rect_colision_izquierda) and self.__move_x < 0:
                # Si choca contra el lado izquierdo de la plataforma mientras se mueve hacia la izquierda
                self.__move_x *= -1  # Cambia la dirección
                self.__is_looking_right = True  # Mira hacia la derecha
            elif self.__rect.colliderect(platform.rect_colision_derecha) and self.__move_x > 0:
                # Si choca contra el lado derecho de la plataforma mientras se mueve hacia la derecha
                self.__move_x *= -1  # Cambia la dirección
                self.__is_looking_right = False  # Mira hacia la izquierda

    def handle_ground_collision(self, platforms):
        on_ground = False

        for platform in platforms:
            if self.__rect.colliderect(platform.rect_colision_superior):
                self.__rect.y = platform.rect.y - self.__rect.height
                self.__is_jumping = False
                self.__is_falling = False
                self.__move_y = 0
                on_ground = True
                break

        if not on_ground:
            if not self.__is_jumping:
                self.__is_falling = True

        if self.__is_falling:

            self.__rect.y += self.__move_y

            for platform in platforms:
                if self.__rect.colliderect(platform.rect_colision_superior):
                    self.__rect.y = platform.rect.y - self.__rect.height
                    self.__is_jumping = False
                    self.__is_falling = False
                    self.__move_y = 0
                    break

            if not any(self.__rect.colliderect(platform.rect_colision_superior) for platform in platforms):
                self.__is_jumping = False
                self.__is_falling = True

            if self.__rect.y >= LARGO_VENTANA - self.__rect.height:
                self.__rect.y = LARGO_VENTANA - self.__rect.height
                self.__is_falling = False
                self.__move_y = 0
            elif self.__rect.y < 0:
                self.__rect.y = 0 
                self.__is_falling = False
                self.__move_y = 0
            else:
                self.__move_y += self.__gravity

    def __set_borders_limits(self):
        pixels_move = 0
        if self.__move_x > 0:
            pixels_move = self.__move_x if self.__rect.x < ANCHO_VENTANA - self.__actual_img_animation.get_width() else 0
        elif self.__move_x < 0:
            pixels_move = self.__move_x if self.__rect.x > 0 else 0
        return pixels_move

    def do_movement(self, delta_ms, plataformas):
        self.__enemy_move_time += delta_ms
        if self.__enemy_move_time >= self.__frame_rate:
            self.__enemy_move_time = 0

            if self.__direction_change_counter > 0:
                self.__direction_change_counter -= 1 

            if random.randint(1,233)%2 == 0 and self.__direction_change_counter == 0 :
                self.__direction_change_counter = 30

                direction = random.choice(['Right', 'Left'])

                if direction == 'Right':
                    self.__set_x_animations_preset(self.__speed_walk, self.__walk_r, look_r=True)
                else:
                    self.__set_x_animations_preset(-self.__speed_walk, self.__walk_l, look_r=False)

            self.__rect.x += self.__set_borders_limits()
            
            self.__rect.y += self.__gravity
            self.handle_ground_collision(plataformas)
            
            if self.__rect.x < 0:
                self.__rect.x = 0
            elif self.__rect.x > ANCHO_VENTANA:
                self.__rect.x = ANCHO_VENTANA

    def do_animation(self, delta_ms):
        self.__enemy_animation_time += delta_ms
        try:
            if self.__enemy_animation_time >= self.__frame_rate:
                self.__enemy_animation_time = 0
                if self.__initial_frame < (len(self.__actual_animation) - 1):
                    self.__initial_frame += 1
                else:
                    self.__initial_frame = 0
        except IndexError:
            print("Error: self.__initial_frame is out of range for self.__actual_animation")

    def kill(self):
        self._enemy_is_alive = False
        
    def shoot(self):
        print('DISPARO EL ENEMIGO')
        bullet_direction = 'True' if self.__is_looking_right else 'False'
        bullet = self.create_bullet(bullet_direction)
        self.bullet_group.add(bullet)
    
    def get_daño(self):
        return self.__daño
    
    def get_life(self):
        return self.__life
    
    def decrease_life(self,amount):
        self.__life -= amount

    def revive(self):
        self._enemy_is_alive = True
        self.__life = 100

    def create_bullet(self, direction):
        return Bullet(self.__rect.x, self.__rect.top, direction)
    
    def set_cero_life(self):
        self.__life = 0
        

    def update(self, delta_ms, plataformas):
        self.do_movement(delta_ms, plataformas)
        self.do_animation(delta_ms)
        self.handle_ground_collision(plataformas)

    def draw(self, screen: pg.surface.Surface):
        if DEBUG:
            pg.draw.rect(screen, 'red', self.__rect)
        if self.__initial_frame < len(self.__actual_animation):
            self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
            screen.blit(self.__actual_img_animation, self.__rect)
        else:
            print(f"Error: self.__initial_frame ({self.__initial_frame}) is out of range for self.__actual_animation")