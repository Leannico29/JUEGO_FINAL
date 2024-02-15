import pygame as pg

class SurfaceManager:

    @staticmethod
    def get_surface_from_spritesheet(img_path: str, cols: int, rows: int, step = 1, flip: bool = False) -> list[pg.surface.Surface]:
        sprites_list = list()
        surface_img = pg.image.load(img_path)
        frame_width = int(surface_img.get_width()/cols)
        frame_height = int(surface_img.get_height()/rows)

        for row in range(rows):

            for column in range(0, cols, step):
                x_axis = column * frame_width
                y_axis = row * frame_height

                frame_surface = surface_img.subsurface(
                    x_axis, y_axis, frame_width, frame_height
                )

                if flip:
                    frame_surface = pg.transform.flip(frame_surface, True, False)
                sprites_list.append(frame_surface)
        return sprites_list


def quick_sort(list):
    if len(list) <= 1:
        return list
    else:
        pivot = list[0][1]
        menores = [(nombre, puntos) for nombre, puntos in list if puntos < pivot]
        iguales = [(nombre, puntos) for nombre, puntos in list if puntos == pivot]
        mayores = [(nombre, puntos) for nombre, puntos in list if puntos > pivot]
        return quick_sort(menores) + iguales + quick_sort(mayores)