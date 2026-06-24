import math as math

# Inicializamos class de tweens (ya traia ganas de porfin usar classes, me da igual que sea un proyecto de primer semestre I fucking love OOP and metatables)
class Tween:
    def __init__(self, inicio : float | int, final : float | int, duracion : int, al_completar : callable | None):
        self.inicio = inicio
        self.final = final
        self.duracion = duracion # En milisegundos, osea 1 segundo se expresaria como 1000
        self.al_completar = al_completar

        self.running = False
        self.tiempo_inicial = 0
        self.umbral = 0
        self.valor = inicio
    
    def lerp_ease_in_out(self):
        return self.umbral * self.umbral if self.umbral < 0.5 else (1 - ((-2 * self.umbral) + 2)**3 ) / 2
        

    def empezar(self, tiempo : int):
        self.tiempo_inicial = tiempo
        self.running = True
    
    def reproducir(self, tiempo_actual : int): # tiempo_actual es el tiempo que nos arroja pygame.time.get_ticks()
        if not self.running:
            return self.value

        # Cálculo del tiempo transcurrido normalizado (0.0 a 1.0)
        delta = (tiempo_actual - self.tiempo_inicial) / self.duracion
        self.umbral = min(delta, 1.0)
        
        # Aplicamos el Easing (Ease-in-out-quad)
        t_smooth = self.lerp_ease_in_out()
        
        # Interpolamos el valor final
        self.valor = self.inicio + (self.final - self.inicio) * t_smooth
        
        if self.umbral >= 1.0:
            self.running = False
            if self.al_completar:
                self.al_completar()
            
        return self.valor
        

class Tweens:
    def __init__(self):
        self.lista_de_tweens = []
    
    def agregar(self, tween):
        self.lista_de_tweens.append(tween)
    
    def actualizar(self, tiempo_actual : int): # Recordemos que tiempo_actual es pygame.time.get_ticks()
        for tween in self.lista_de_tweens:
            tween.reproducir(tiempo_actual)

        self.lista_de_tweens = [tween for tween in self.lista_tweens if tween.running]