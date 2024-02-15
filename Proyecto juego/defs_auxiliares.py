from models.constantes import *

def coolers(cooler:int,valor:int,condicion:bool):
    cooler = cooler + valor if condicion else cooler - valor  
    return cooler 

def suma(a,b):
    suma = a + b
    return suma 

def resta(a,b):
    resta = a - b
    return resta

def set_cero(a):
    a = 0
    return a

def set_color(minutos,segundos):
    if segundos < 30 and minutos < 1:
            color = verde
    elif segundos >= 30:
        color = amarillo
    elif minutos >= 1:
        color = rojo 
    elif minutos >= 2 and segundos > 0:
        color = rojo 
    return color