debug = True

# Inicializamos class de tweens (ya traia ganas de porfin usar classes, me da igual que sea un proyecto de primer semestre I fucking love OOP and metatables)
class Tween:
    
    def __init__(self, inicio : float | int, final : float | int, duracion : int, al_completar=None):
        """
        Class [Tween] Crea un nuevo tween (interpolacion numerica) con numeros dados

         Parametros
         - inicio -> El valor inicial que habra previo a la interpolacion.
         - final -> El valor final que habra despues de aplicar la interpolacion completamente.
         - duracion -> La cantidad de tiempo (en milisegundos) que tardara la interpolacion en realizarse.
         - al_completar -> Una funcion cualquiera que queramos reproducir al momento que termine la interpolacion.
         
        """
            
        self.inicio = inicio
        self.final = final
        self.duracion = duracion # En milisegundos, osea 1 segundo se expresaria como 1000
        self.al_completar = al_completar

        self.running = False
        self.tiempo_inicial = 0
        self.umbral = 0
        self.valor = inicio

        print(f"Inicializado con inicio {inicio}, final {final}, y duracion {duracion}.") if debug is True else None
    
    def lerp_ease_in_out(self) -> float:
        """
        Funcion tipo easing que aplicara un efecto smooth al valor numerico.
        Va de la mano junto a reproducir()

        Retorna:
            - Un float suavizado
        """

        return self.umbral * self.umbral if self.umbral < 0.5 else (1 - ((-2 * self.umbral) + 2)**3 ) / 2
        

    def empezar(self, tiempo : int):
        self.tiempo_inicial = tiempo
        self.running = True
    
    def reproducir(self, tiempo_actual : int) -> float: # tiempo_actual es el tiempo que nos arroja pygame.time.get_ticks()
        """
        Funcion principal de la clase, aplica una interpolacion numerica suave a cualquier tipo de numero, la interpolacion ocurre entre ticks.

        Parametros:
            - tiempo_actual -> Un int que se dara cada frame mediante pygame.time.get_ticks()
        
        Retorna:
            - El valor 

        """
        if not self.running:
            return self.value

        # Calculo del tiempo transcurrido normalizado (0.0 a 1.0)
        delta = (tiempo_actual - self.tiempo_inicial) / self.duracion
        self.umbral = min(delta, 1.0)
        
        # Aplicamos el easing 
        t_smooth = self.lerp_ease_in_out()
        
        # Interpolamos el valor final
        self.valor = self.inicio + (self.final - self.inicio) * t_smooth

        print(f"Reproduciendo... {self.valor} valor actual.") if debug is True else None

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

        self.lista_de_tweens = [tween for tween in self.lista_de_tweens if tween.running]