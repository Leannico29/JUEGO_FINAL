from models.auxiliar import SurfaceManager as sf
import pygame as pg
from models.constantes import ANCHO_VENTANA, DEBUG, LARGO_VENTANA
from models.bullet.Bullet import Bullet
from dataloader import *


class Player:
    def __init__(self, coord_x, coord_y, frame_rate = 100, speed_walk = 6, speed_run = 12, gravity = 20, jump = 70, vida = 100):
        self.__iddle_r = sf.get_surface_from_spritesheet('models\player\iddle\Idle.png',11 , 1)
        self.__iddle_l = sf.get_surface_from_spritesheet('models\player\iddle\Idle.png', 11, 1, flip=True)
        self.__walk_r = sf.get_surface_from_spritesheet('models\player\walk\walk.png', 12, 1)
        self.__walk_l = sf.get_surface_from_spritesheet('models\player\walk\walk.png', 12, 1, flip=True)
        self.__run_r = sf.get_surface_from_spritesheet('models\player\\run\Run.png', 6,1 )
        self.__run_l = sf.get_surface_from_spritesheet('models\player\\run\Run.png', 6, 1, flip=True)
        self.__jump_r = sf.get_surface_from_spritesheet('models\player\jump\Jump.png', 1, 1)
        self.__jump_l = sf.get_surface_from_spritesheet('models\player\jump\Jump.png', 1, 1, flip=True)
        self.__falling_r = sf.get_surface_from_spritesheet('models\player\\fall\Fall.png',7,1)
        self.__falling_r = sf.get_surface_from_spritesheet('models\player\\fall\Fall.png',7,1, flip=True)
        self.__hitted_r = sf.get_surface_from_spritesheet('models\player\hitted\Hit.png', 1, 1)
        self.__hitted_l = sf.get_surface_from_spritesheet('models\player\hitted\Hit.png', 1, 1, flip=True)
        self.__move_x = 0
        self.__move_y = 0
        self.__speed_walk = speed_walk
        self.__speed_run = speed_run
        self.__frame_rate = frame_rate
        self.__daño = 50
        self.__player_move_time = 0
        self.__player_animation_time = 0
        self.__gravity = gravity
        self.__jump = jump
        self.__vida = vida 
        self.__is_jumping = False
        self.__is_falling = False
        self._Player__is_alive = True
        self.__initial_frame = 0
        self.__actual_animation = self.__iddle_r
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.__rect = self.__actual_img_animation.get_rect()
        self.__is_looking_right = True
##############################################
        self.bullet_group = pg.sprite.Group()
        self.__rect = self.__actual_img_animation.get_rect(topleft = (coord_x, coord_y))
        self.rect = self.__rect
##############################################


    def __set_x_animations_preset(self, move_x, animation_list: list[pg.surface.Surface], look_r: bool):
        self.__move_x = move_x
        self.__actual_animation = animation_list
        self.__is_looking_right = look_r
        
    
    def __set_y_animations_preset(self, jumping):
        if jumping:
            self.__is_jumping = True
            self.__is_falling = False
            self.__initial_frame = 0
            self.__move_y = -self.__jump
        else:
            self.__is_jumping = False
            self.__is_falling = True
            self.__move_y = self.__gravity
    
    def walk(self, direction: str = 'Right'):
        match direction:
            case 'Right':
                look_right = True
                self.__set_x_animations_preset(self.__speed_walk, self.__walk_r, look_r=look_right)
            case 'Left':
                look_right = False
                self.__set_x_animations_preset(-self.__speed_walk, self.__walk_l, look_r=look_right)
    
    def run(self, direction: str = 'Right'):
        match direction:
            case 'Right':
                look_right = True
                self.__set_x_animations_preset(self.__speed_run, self.__run_r, look_r=look_right)
            case 'Left':
                look_right = False
                self.__set_x_animations_preset(-self.__speed_run, self.__run_l, look_r=look_right)
    
    def stay(self):
        if self.__actual_animation != self.__iddle_l and self.__actual_animation != self.__iddle_r:
            self.__actual_animation = self.__iddle_r if self.__is_looking_right else self.__iddle_l
            self.__initial_frame = 0
            self.__move_x = 0
            self.__move_y = 0
    
    def jump(self, jumping=True):
        self.__set_y_animations_preset(jumping)

    def hitted(self):
        if self._Player__is_alive:
            if not self.__is_jumping and not self.__is_falling:
                if self.__is_looking_right:
                    self.__set_x_animations_preset(0, self.__hitted_r, look_r=True)
                else:
                    self.__set_x_animations_preset(0, self.__hitted_l, look_r=False)
                self.__initial_frame = 0
                self.__move_x = 0
                self.__move_y = 0

    def handle_collisions(self, platforms):
        for platform in platforms:
            if self.__rect.colliderect(platform.rect_colision_superior):
                self.__rect.y = platform.rect.y - self.__rect.height
                self.__is_jumping = False
                self.__is_falling = False
                self.__move_y = 0
            elif self.__rect.colliderect(platform.rect_colision_inferior):
                self.__rect.y = platform.rect.y - self.__rect.height
                self.__is_jumping = False
                self.__is_falling = False
                self.__move_y = 0

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
            if self.__rect.y >= LARGO_VENTANA - 70:
                self.__rect.y = LARGO_VENTANA - 70
                self.__is_falling = False
                self.__move_y = 0
            else:
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

                if self.__rect.y < 0:
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


    def do_movement(self, delta_ms):
        self.__player_move_time += delta_ms
        if self.__player_move_time >= self.__frame_rate:
            self.__player_move_time = 0
            new_x = self.__rect.x + self.__set_borders_limits()

            if not self.__is_jumping and not self.__is_falling:
                new_y = self.__rect.y + self.__move_y
                self.__rect.y = min(max(new_y, 0), LARGO_VENTANA - self.__rect.height)  

            self.__rect.x = new_x

            if self.__is_jumping or self.__is_falling:
                self.__rect.y += self.__move_y

                if self.__rect.y >= LARGO_VENTANA - self.__rect.height:
                    self.__rect.y = LARGO_VENTANA - self.__rect.height
                    self.__is_jumping = False
                    self.__is_falling = False
                    self.__move_y = 0
                elif self.__rect.y < 0:
                    self.__rect.y = 0  
                    self.__is_jumping = False
                    self.__is_falling = False
                    self.__move_y = 0
                else:
                    self.__move_y += self.__gravity

    def do_animation(self, delta_ms):
        self.__player_animation_time += delta_ms
        try:
            if self.__player_animation_time >= self.__frame_rate:
                self.__player_animation_time = 0
                if self.__initial_frame < (len(self.__actual_animation) - 1):
                    self.__initial_frame += 1
                else:
                    self.__initial_frame = 0
                    if self.__is_jumping:
                        self.__is_jumping = False
                        self.__move_y = 0
        except IndexError:
            print("Error: self.__initial_frame is out of range for self.__actual_animation")

    def shoot(self):
        print('DISPARASTE')
        bullet_direction = 'True' if self.__is_looking_right else 'False'
        bullet = self.create_bullet(bullet_direction)
        self.bullet_group.add(bullet)
    
    def create_bullet(self, direction):
        return Bullet(self.__rect.x, self.__rect.top, direction)

    def get_daño(self):
        return self.__daño

    def get_vida(self):
        return self.__vida
    
    def gain_vida(self, amount):
        self.__vida = amount 

    def kill(self):
        self._Player__is_alive = False

    def decrease_life(self, amount):
        self.__vida -= amount

    def revive(self):
        self._Player__is_alive = True
        self.__vida = 100

    def update(self, delta_ms,plataformas):
        self.do_movement(delta_ms)
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