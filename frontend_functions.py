import pygame
import math

def aplicar_gaussian_blur(screen, delta : int | float):
    ancho, alto = screen.get_size()

    reduccion = pygame.transform.smoothscale(screen, (int(ancho * delta), (alto * delta)))
    blur = pygame.transform.smoothscale(reduccion, (ancho, alto))

    screen.blit(blur, (0, 0))

def funcion_after_death(allowed : bool):
    allowed = not allowed