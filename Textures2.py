import gc
import pygame

debug = True

def New_Texture_Handler(resolucion_base : list[int, int], resolucion_actual : list[int, int]) -> dict:
    return {
        "delta" : max(1, 
                         min(resolucion_actual[0] // resolucion_base[0], 
                             resolucion_actual[1] // resolucion_base[1])),
        "loaded" : {} # Aqui guardaremos las texturas cargadas en este handler, de esta forma [ruta de textura] : pygameImage
    }

def limpiar_piso(T_Handler : dict):
    T_Handler["loaded"].clear()

    gc.collect()

    print("Memory cleaned") if debug else None

def cargar_y_escalar(T_Handler : dict, ruta : str):

        imagen = pygame.image.load(ruta).convert_alpha()
        escala = (imagen.get_width() * T_Handler["delta"],
                  imagen.get_height() * T_Handler["delta"])

        escalado = pygame.transform.scale(imagen, escala)
        T_Handler["loaded"][ruta] = escalado

def obtener(T_Handler : dict, ruta : str):
        if ruta not in T_Handler["loaded"]:
            cargar_y_escalar(T_Handler, ruta)
        return T_Handler["loaded"][ruta]