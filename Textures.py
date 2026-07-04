import gc
import pygame 
debug = True

# Modulo para cargar y aplicar escala a cualquier textura usando un Class
class TextureLoader():
    def __init__(self, resolucion_base : list[int], resolucion_actual : list[int]):
        self.delta = max(1, 
                         min(resolucion_actual[0] // resolucion_base[0], 
                             resolucion_actual[1] // resolucion_base[1]))
        self.loaded = {} # Aqui almacenaremos nuestras texturas cargadas

    def limpiar_piso(self):
        self.loaded.clear()

        gc.collect()
        
        print("Memory cleaned") if debug else None

    def cargar_y_escalar(self, ruta : str):

        imagen = pygame.image.load(ruta).convert_alpha()
        escala = (imagen.get_width() * self.delta,
                  imagen.get_height() * self.delta)
        
        escalado = pygame.transform.scale(imagen, escala)
        self.loaded[ruta] = escalado

    def obtener(self, ruta : str):
        if ruta not in self.loaded:
            self.cargar_y_escalar(ruta)
        return self.loaded[ruta]