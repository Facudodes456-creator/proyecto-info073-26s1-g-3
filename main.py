import os
import random
import pygame
import gc
import frontend_functions

import tween_module as TweenHandler
from Textures import TextureLoader as TextureHandler
import frontend_functions

import Textures2 as TextureModule
import tween_module2 as TweenModule

# Estados del juego
ESTADO_INICIO = "inicio"
ESTADO_INSTRUCCIONES = "instrucciones"
ESTADO_JUGANDO = "jugando"
ESTADO_DERROTA = "derrota"
ESTADO_VICTORIA = "victoria"
ESTADO_STATS = "cambiando_stats"

# Rutas a la carpeta de imágenes de pantallas
DIR_PANTALLAS = os.path.join(os.path.dirname(__file__), "data", "pantallas")

# Se específica el nombre del archivo para cada imagen de pantalla.
# El formato de imagen utilizado puede ser PNG, JPG/JPEG, BMP, o GIF.
PANTALLA_INICIO = "pantalla_inicio.bmp"
PANTALLA_INSTRUCCIONES = "pantalla_instrucciones.bmp"
PANTALLA_VICTORIA = "pantalla_victoria.bmp"
PANTALLA_DERROTA = "pantalla_derrota.bmp"

# Códigos de cada elemento del tablero
SUELO = 0
OBSTACULO = 1
MONSTRUO = 4
JUGADOR = 2
MANZANA = 3

# Ancho y alto de la pantalla

ANCHO_VENTANA = 800
ALTO_VENTANA = 800

# Tamano del tablero
FILAS = 15
COLUMNAS = 15


#Variables misc
piso = 1
monstruos_current = 0
manzanas_current = 0
manzanas_max = 2

# Inicializamos gestor de texturas
T_Handler = TextureHandler([800, 800], [ANCHO_VENTANA, ALTO_VENTANA])
T_Handler = TextureModule.New_Texture_Handler([800, 800], [ANCHO_VENTANA, ALTO_VENTANA])



# Gestor de Tweens principal
gestor_tweens = TweenHandler.Tweens()

# Tweens inicializados
tween_botones_ui = TweenHandler.Tween(100, 300, 500)

#Diccionario que contiene informacion esencial de cada piso
pisos_datos = {
    1 : {
        "Texturas" : { #Aqui estan los paths de cada textura que usemos para los elementos de el piso, en este caso el piso 1
            "Monstruo" : "data/pisos/1/monstruo.png",
            "Piso" : "data/pisos/1/suelo.png",
            "Manzana" : "data/pisos/1/manzana.png",
            "Pared" : "data/pisos/1/pared.png"
        },
        "Sonidos" : { # Ubicacion de los sonidos que se usaran en el piso
            "Musica" : "data/pisos/1/test.mp3",
            "Hola" : "gamma dan is fucking hell istfg im never clearin that shit"
        },
        "Datos" : { #Aqui esta la logica del piso correspondiente
            "MONSTRUOS_MAX" : 2,
            "OBSTACULOS_MAX" : 2,
            "SPAWN_RATE" : 6000, # Cada 6000 ticks (O 6 segundos) aparecera un nuevo monstruo mientras aun no se haya llegado a la capacidad maxima de monstruos
            "SPAWN_RATE_MANZANAS" : 5000, # Lo mismo, cada 7 segundos aparecera una nueva manzana (Solo pueden haber un maximo de 2 manzanas en el tablero)
            "MANZANAS_OBJETIVO" : 4
        },
        "Placeholder_Futuro" : {} #Por si tenemos que agregar algo mas
    },
        2 : {
        "Texturas" : { #Aqui estan los paths de cada textura que usemos para los elementos de el piso, en este caso el piso 2
            "Monstruo" : "data/pisos/2/monstruo.png",
            "Piso" : "data/pisos/2/suelo.png",
            "Manzana" : "data/pisos/2/manzana.png",
            "Pared" : "data/pisos/2/pared.png"
        },
        "Sonidos" : {
            "Musica" : "data/pisos/2/test.mp3",
            "Hola" : "gamma dan is fucking hell istfg im never clearin that shit"
        },
        "Datos" : { #Aqui esta la logica del piso correspondiente
            "MONSTRUOS_MAX" : 4,
            "OBSTACULOS_MAX" : 4,
            "SPAWN_RATE" : 4000,
            "SPAWN_RATE_MANZANAS" : 6000,
            "MANZANAS_OBJETIVO" : 1,
        },
        "Placeholder_Futuro" : {} #Por si tenemos que agregar algo mas
    },
        3 : {
        "Texturas" : { #Aqui estan los paths de cada textura que usemos para los elementos de el piso, en este caso el piso 3
            "Monstruo" : "data/pisos/3/monstruo.png",
            "Piso" : "data/pisos/3/suelo.png",
            "Manzana" : "data/pisos/3/manzana.png",
            "Pared" : "data/pisos/3/pared.png"
        },
        "Sonidos" : {
            "Musica" : "data/pisos/3/test.mp3",
            "Hola" : "gamma dan is fucking hell istfg im never clearin that shit"
        },
        "Datos" : { #Aqui esta la logica del piso correspondiente
            "MONSTRUOS_MAX" : 10,
            "OBSTACULOS_MAX" : 10,
            "SPAWN_RATE" : 2000,
            "SPAWN_RATE_MANZANAS" : 8000,
            "MANZANAS_OBJETIVO" : 1,
        },
        "Placeholder_Futuro" : {} #Por si tenemos que agregar algo mas
    },

}


# ==================== CAMBIO DE TEXTURAS POR PISO ====================
# No precargamos todas las texturas al inicio.
# Cada vez que cambia el piso, limpiamos la caché del loader y cargamos
# las imágenes del piso actual. Así el nivel 3 usa su propio suelo.png y pared.png.

def aplicar_texturas_piso_actual(datos: dict):
    global piso

    datos["texturas"].clear()
    TextureModule.limpiar_piso(T_Handler)

    datos["texturas"] = {
        "Manzana": TextureModule.obtener(T_Handler, pisos_datos[piso]["Texturas"]["Manzana"]),
        "Pared": TextureModule.obtener(T_Handler, pisos_datos[piso]["Texturas"]["Pared"]),
        "Piso": TextureModule.obtener(T_Handler, pisos_datos[piso]["Texturas"]["Piso"]),
        "Monstruo": TextureModule.obtener(T_Handler, pisos_datos[piso]["Texturas"]["Monstruo"]),
    }

#Diccionario que contiene la informacion de nuestro personaje
STATS = {
    "Vida" : 3,
    "Vida_Actual" : 3,
    "Velocidad" : 200, # Esta variable hace alucion a el  retraso entre cada movimiento
    "Vidas_Adicionales" : 0, 
    "Vidas_Adicionales_Current" : 0, # Al consumir 4 puntos disponibles en mejorar esta metrica, se obtendra una resurreccion
    "Puntos_disponibles" : 0, # Aqui guardaremos los puntos disponibles, se conseguiran 4 puntos cada piso completado, y 0.5 puntos por cada monstruo derrotado en el piso (No cuentan los monstruos derrotados si no pasas el piso)
    "Armadura" : 1, # Cada punto de armadura es 1 punto de defensa que protege al jugador de 1 solo hit por cada punto de armadura, o consume 2 puntos para tankear el golpe de un obstaculo y lo destruye, o si te sales del mapa, consumes 2 puntos para evitar esto, y te quedas parado en el ultimo tile pisado, hasta que elijas una nueva direccion, por ejemplo si tienes 2 de armadura y 4 de vida, y tocas a 3 monstruos, tu vida restante sera de 3, 2 golpes habran sido tankeados por la armadura
    "Armadura_Current" : 4,
    "Pasos_Max" : 100
}

STATS_MAXIMUM_VALUES = {
    "Vida" : 8,
    "Velocidad" : 100,
    "Vidas_Adicionales" : 2,
    "Armadura" : 4
}

# Variable global para pasos restantes, y pasos realizados
restantes = STATS["Pasos_Max"]
pasos = 0


def aparecer_aleatorio(tablero, id_elem):
    
    global monstruos_current
    global manzanas_current
    global pisos_datos

    """
    Coloca un elemento en una casilla vacía aleatoria del tablero.

    Parámetros:
        - tablero: El tablero con sus posiciones actuales.
        - id_elem: El número identificador del elemento que queremos colocar.

    Retorna:
        - (columna, fila): Tupla que indica posición en la que se colocó el elemento.
    """

    # Debemos detectar los espacios vacíos, para ello recorremos
    # el tablero y almacenamos tuplas de (columna, fila) las posiciones
    # en las que un elemento "VACIO" (el número 0 en este caso) se encuentre.

    vacios = []

    # Forma vista en clases de recorrer el arreglo multidimensional.
    # Tanto fila como columna son números.
    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            # Obtenemos el elemento que se encuentra en esa fila y columna.
            elem_pos = tablero[fila][columna]

            if elem_pos == SUELO:
                # Al utilizar los paréntesis () dentro de la función, lo estaremos
                # añadiendo como una tupla con la estructura (columna, fila).
                vacios.append((columna, fila))

    # También se puede utilizar comprensión de listas para rellenar el arreglo
    # a la vez que lo recorremos:
    #
    # vacios = [
    #     (columna, fila)
    #     for fila in range(FILAS)
    #     for columna in range(COLUMNAS)
    #     if tablero[fila][columna] == VACIO
    # ]

    # Si no hay casillas vacías, retornamos un valor especial.
    if len(vacios) == 0:
        return -1, -1

    # Usando la función random.choice(lista) podremos obtener una tupla
    # aleatoria desde el arreglo "vacios" que definimos anteriormente.
    columna, fila = random.choice(vacios)

    # Finalmente, colocamos el elemento al poner su número en la casilla
    # del tablero correspondiente.
    
    if id_elem == MONSTRUO:
        monstruos_current = min(monstruos_current + 1, pisos_datos[piso]["Datos"]["MONSTRUOS_MAX"])
    elif id_elem == MANZANA:
        manzanas_current = min(manzanas_current + 1, manzanas_max)
    tablero[fila][columna] = id_elem

    return columna, fila

def pantalla_stats(): # Funcion donde mostraremos la pantalla de mejorar stats, luego de ganar cada partida
    return "クソクソクソクソクソ"

def cambiar_stats(id_stat : str, puntos_inputeados : int) -> str:
    global STATS
    
    if puntos_inputeados > STATS["Puntos_disponibles"]:
        return "Error, no tienes puntos suficientes."
    
    msj = ""
    if id_stat == "Vida": #Cada dos puntos disponibles obtienes 1 punto de vida
        if puntos_inputeados % 2 != 0 and puntos_inputeados > 1:
            puntos_inputeados -= 1
        elif puntos_inputeados < 1:
            return "Error, no tienes puntos suficientes."
            
        
        STATS["Vida"] = min(STATS["Vida"] + (puntos_inputeados // 2), STATS_MAXIMUM_VALUES["Vida"])
        msj = f"Exito. Tus puntos de vida ahora son {STATS['Vida']}."
    elif id_stat == "Velocidad":
        if puntos_inputeados % 2 != 0 and puntos_inputeados > 1:
            puntos_inputeados -= 1
        elif puntos_inputeados < 1:
           return "Error, no tienes puntos suficientes."
        
        STATS["Velocidad"] = max(100, STATS["Velocidad"] - (puntos_inputeados * 10))
        msj =  f"Exito. Tu velocidad se reducio a {STATS['Velocidad']} milisegundos."
    elif id_stat == "Vidas_Adicionales":
        if puntos_inputeados < 4:
            return "Error, no tienes puntos suficientes."
        else:
            puntos_inputeados = 4

            STATS["Vidas_Adicionales"] = min(STATS["Vidas_Adicionales"] + 1, STATS_MAXIMUM_VALUES["Vidas_Adicionales"])
            msj =  f"Exito. Ahora tienes {STATS['Vidas_Adicionales']} vidas adicionales."
    elif id_stat == "Pasos_Max":

        STATS["Pasos_Max"] += (puntos_inputeados * 5)
        msj =  f"Exito. Ahora tus pasos maximos son {STATS['Pasos_Max']} pasos."
    elif id_stat == "Armadura":
        if puntos_inputeados % 2 != 0 and puntos_inputeados > 1:
            puntos_inputeados -= 1
        elif puntos_inputeados < 1:
            return "Error, no tienes puntos suficientes."
        
        STATS["Armadura"] = min(STATS["Armadura"] + (puntos_inputeados // 2), STATS_MAXIMUM_VALUES["Armadura"])
        msj = f"Exito. Ahora tienes {STATS['Armadura']} de armadura adicional."

    STATS["Puntos_disponibles"] -= puntos_inputeados
    return msj

def poblar_tablero(tablero):
    global piso
    global pisos_datos
    global monstruos_current


    """
    Coloca un obstáculo y la manzana en el tablero.

    Parámetros:
        - tablero: El tablero con sus posiciones actuales.
    """
    obstaculos_max = pisos_datos[piso]["Datos"]["OBSTACULOS_MAX"]
    monstruos_max = pisos_datos[piso]["Datos"]["MONSTRUOS_MAX"]

    for i in range(obstaculos_max):
        aparecer_aleatorio(tablero, OBSTACULO)
    
    for i in range(monstruos_max):
        aparecer_aleatorio(tablero, MONSTRUO)
    
    for i in range(manzanas_max):
        aparecer_aleatorio(tablero, MANZANA)




def refrescar_tablero(datos : dict):

    datos["screen"].fill("gray30")
    
    alto_elem = datos["screen"].get_height() / FILAS
    ancho_elem = datos["screen"].get_width() / COLUMNAS

    pos_y = 0
    for i in range(FILAS):
        pos_x = 0  # <- Corregido: Alineado correctamente a 8 espacios
        for j in range(COLUMNAS):
            
            # Dibujamos suelo siempre para asegurar consistencia
            datos["screen"].blit(datos["texturas"]["Piso"], [pos_x, pos_y])

            # Ahora dibujamos el objeto correspondiente encima
            if datos["tablero"][i][j] == OBSTACULO:
                datos["screen"].blit(datos["texturas"]["Pared"], [pos_x, pos_y])
            elif datos["tablero"][i][j] == JUGADOR:
                datos["screen"].blit(datos["img_actual"], [pos_x + 2, pos_y + 2])
            elif datos["tablero"][i][j] == MANZANA:
                datos["screen"].blit(datos["texturas"]["Manzana"], [pos_x, pos_y])
            elif datos["tablero"][i][j] == MONSTRUO:
                datos["screen"].blit(datos["texturas"]["Monstruo"], [pos_x, pos_y])

            pos_x += ancho_elem
        
        # <- Corregido: Esto debe ejecutarse CADA VEZ que termina una fila (12 espacios)
        pos_y += alto_elem 
        
    # <- Corregido: El flip va al final de todo, fuera de los bucles (4 espacios)
    dibujar_barra(datos["screen"])
    pygame.display.flip()


def cambiar_direccion(keys, datos):
    """
    Cambia la dirección del jugador.

    Parámetros:
        - keys: Arreglo de teclas presionadas.
        - direccion_actual: La dirección en la que estaba avanzando justo antes de analizar
            si hubo un cambio de dirección.

    Retorna:
        - direccion_actual: La nueva dirección del jugador.
    """

    # Tecla W
    if keys[pygame.K_w]:
        # La tupla nos indica que horizontalmente (columnas) no hará nada (0) y
        # que verticalmente (filas) disminuirá el índice en el tablero (-1).
        datos["direccion"] =  (0, -1)

    # Tecla S
    elif keys[pygame.K_s]:
        # En este caso avanzará a través de las filas del tablero.
        datos["direccion"] =  (0, 1)

    # Tecla A
    elif keys[pygame.K_a]:
        # Retrocede por las columnas del tablero.
        datos["direccion"] =  (-1, 0)

    # Tecla D
    elif keys[pygame.K_d]:
        # Avanza por las columnas del tablero.
        datos["direccion"] =  (1, 0)

    # Si no se presiona ninguna de las teclas anteriores, la dirección
    # será la misma que la anterior.


def avanzar(datos: dict) -> str:
    """
    Avanza el jugador un paso en la dirección dada interactuando directamente
    con el estado centralizado en el diccionario de datos.

    Retorna:
        - resultado (str): "derrota", "victoria" o "ok"
    """
    global restantes
    global pasos
    global STATS
    global monstruos_current
    global manzanas_current

    dir_col, dir_fila = datos["direccion"]
    ind_actual_col, ind_actual_fila = datos["pos_jugador"]

    # Aplicamos la dirección a la posición del jugador
    ind_nueva_col = ind_actual_col + dir_col
    ind_nueva_fila = ind_actual_fila + dir_fila

    # Verificamos choque con el borde del tablero
    if not (0 <= ind_nueva_col < COLUMNAS and 0 <= ind_nueva_fila < FILAS):
        if STATS["Armadura_Current"] >= 2:
            datos["direccion"] = (0, 0)
            STATS["Armadura_Current"] = max(0, STATS["Armadura_Current"] - 2)
            datos["img_actual"] = datos["sprites"]["abajo"]
            return "ok"
        else:
            return "derrota"

    # Obtenemos el elemento en la nueva celda
    pos_elem = datos["tablero"][ind_nueva_fila][ind_nueva_col]

    if pos_elem == OBSTACULO:
        if STATS["Armadura_Current"] >= 2:
            STATS["Armadura_Current"] = max(0, STATS["Armadura_Current"] - 2)
            datos["pos_jugador"] = (ind_nueva_col, ind_nueva_fila)
            
            datos["tablero"][ind_actual_fila][ind_actual_col] = SUELO
            datos["tablero"][ind_nueva_fila][ind_nueva_col] = JUGADOR
            datos["pos_jugador"] = (ind_nueva_col, ind_nueva_fila)

            return "ok"
        else:
            return "derrota"
            
    elif pos_elem == MONSTRUO:
        if STATS["Armadura_Current"] > 0:
            STATS["Armadura_Current"] -= 1
        else:
            STATS["Vida_Actual"] -= 1

        datos["tablero"][ind_actual_fila][ind_actual_col] = SUELO
        datos["tablero"][ind_nueva_fila][ind_nueva_col] = JUGADOR
        monstruos_current = max(0, monstruos_current - 1)
        
        if STATS["Vida_Actual"] <= 0:
            return "derrota"

    elif pos_elem == MANZANA:
        datos["manzanas_comidas"] += 1
        manzanas_current = max(0, manzanas_current - 1)
        pasos -= 6  # Recompensa de pasos

        datos["tablero"][ind_actual_fila][ind_actual_col] = SUELO
        datos["tablero"][ind_nueva_fila][ind_nueva_col] = JUGADOR
        datos["pos_jugador"] = (ind_nueva_col, ind_nueva_fila)

        if datos["manzanas_comidas"] >= pisos_datos[piso]["Datos"]["MANZANAS_OBJETIVO"]:
            return "victoria"
        

    # Movimiento normal (SUELO o celdas vacías tras procesar monstruos sobrevivientes)
    datos["tablero"][ind_actual_fila][ind_actual_col] = SUELO
    datos["tablero"][ind_nueva_fila][ind_nueva_col] = JUGADOR
    datos["pos_jugador"] = (ind_nueva_col, ind_nueva_fila)
    
    return "ok"


def reiniciar(datos : dict):
    global monstruos_current
    global manzanas_current

    """
    Crea un nuevo tablero y estado para una nueva partida.

    Retorna:
        - (tablero, pos_jugador): Tablero nuevo y la nueva posición aleatoria del jugador.
            pos_jugador corresponda a una tupla (columna, fila) donde columna y fila son índices
            de matriz tablero.
    """

    # Si se modifica constante FILAS o COLUMNAS al inicio, también
    # se debe modificar este arreglo de tablero con los valores correspondientes.
    # Esto puede ser mejorado usando dos bucles "for" anidados o comprensión de listas.
    datos["tablero"] = [[0] * COLUMNAS for _ in range(FILAS)]

    # Usando dos bucles "for" anidados se haría de la siguiente manera:
    # tablero = []
    # for _ in range(FILAS):
    #     fila_tablero = []
    #
    #     for _ in range(COLUMNAS):
    #         fila_tablero.append(VACIO)
    #
    #     tablero.append(fila_tablero)
    # Otra manera usando comprensión de listas:
    # tablero = [[VACIO] * COLUMNAS for _ in range(FILAS)]
    # El _ en el "for" indica que no usamos la variable con la que iteramos.

    monstruos_current = 0
    manzanas_current = 0
    poblar_tablero(datos["tablero"])

    # Colocamos al jugador en una posición aleatoria.
    datos["pos_jugador"] = aparecer_aleatorio(datos["tablero"], JUGADOR)


def mostrar_pantalla(screen, nombre_archivo):
    """
    Carga una imagen y la muestra escalada a la ventana.

    Parámetros:
        - screen: La pantalla donde colocaremos la imagen.
        - nombre_archivo: El nombre del archivo de la imagen.
    """

    ruta = os.path.join(DIR_PANTALLAS, nombre_archivo)

    try:
        imagen = pygame.image.load(ruta)
        imagen = pygame.transform.scale(imagen, screen.get_size())

        # Dibujamos la imagen en la pantalla en la coordenada (0, 0).
        screen.blit(imagen, (0, 0))

        # Refrescamos pantalla.
        pygame.display.flip()
    except FileNotFoundError:
        # Fallback de seguridad en caso de que las imágenes no existan aún
        screen.fill("black")
        pygame.display.flip()
        print(f"Advertencia: No se encontró la imagen {ruta}")


# Hacemos una funcion auxiliar para evitar el "DRY" (Don't repeat yourself) en el while de main()
# Funcion auxiliar [1]
def reestablecer_stats():
    STATS["Vida_Actual"] = STATS["Vida"]
    STATS["Armadura_Current"] = STATS["Armadura"]
    STATS["Vidas_Adicionales_Current"] = STATS["Vidas_Adicionales"]

# Funcion auxiliar [2]
def reiniciar_estado_juego(datos : dict):
    reiniciar(datos)
    datos["manzanas_comidas"] = 0
    datos["direccion"] = (0, 0)
    datos["img_actual"] = datos["sprites"]["abajo"]
    datos["tiempo_ultimo_mov"] = pygame.time.get_ticks()
    datos["elapsed_time_monstruo"] = pygame.time.get_ticks()
    datos["elapsed_time_manzana"] = pygame.time.get_ticks()
    pygame.mixer.music.unpause()
    refrescar_tablero(datos)

# Funcion auxiliar [3]
def iniciar_estado_juego(datos : dict):
    reiniciar_estado_juego(datos) # Holy shit I love recursive stuff so much
    pygame.mixer.music.load(pisos_datos[piso]["Sonidos"]["Musica"])
    pygame.mixer.music.set_volume(0)
    pygame.mixer.music.play(-1)

# Funcion auxiliar [4] 寒いいいいいバカー～
def avanzar_personaje(datos : dict):
    global pasos
    global restantes

    datos["tiempo_ultimo_mov"] = datos["tiempo_actual"]
    pasos += 1
    restantes = STATS["Pasos_Max"] - pasos
    pygame.display.set_caption(f" Juego - Pasos restantes : {restantes}")
                        
    if pasos >= STATS["Pasos_Max"]:
        datos["estado"] = ESTADO_DERROTA
        restantes = STATS["Pasos_Max"]
        pasos = 0
        reestablecer_stats()
        mostrar_pantalla(datos["screen"], PANTALLA_DERROTA)
    else:
                            
        if datos["direccion"] == (0, -1): datos["img_actual"] = datos["sprites"]["arriba"]
        elif datos["direccion"] == (0, 1): datos["img_actual"] = datos["sprites"]["abajo"]
        elif datos["direccion"] == (-1, 0): datos["img_actual"] = datos["sprites"]["izquierda"]
        elif datos["direccion"] == (1, 0): datos["img_actual"] = datos["sprites"]["derecha"]

        refrescar_tablero(datos)

# Funcion auxiliar [5] made by y'all motherfucking ass Sebasutian Araya です　にっが
def spawn_objects(tablero, id_elem):

    if id_elem == MANZANA:
        if manzanas_current < manzanas_max:
            aparecer_aleatorio(tablero, id_elem)
    elif id_elem == MONSTRUO:
        if monstruos_current < pisos_datos[piso]["Datos"]["MONSTRUOS_MAX"]:
            aparecer_aleatorio(tablero, id_elem)

# Funcion auxiliar [6] made by your fucking ugly dogshit awesome dipshit ass author going by the motherfuckidy fucking ass name Sebastian Arrrrrrrrrrraya DESU
def actualizar_texturas_piso(datos: dict):
    # Antes se borraban y se volvían a cargar las texturas aquí.
    # Eso causaba el retraso y que se viera por un momento el nivel anterior.
    aplicar_texturas_piso_actual(datos)

def dibujar_barra(screen):

    fuente = pygame.font.SysFont("Arial", 22)

    #==================== VIDA ====================

    porcentaje_vida = STATS["Vida_Actual"] / STATS["Vida"]

    x = 20
    y = 20

    largo_barra = 180
    alto_barra = 18

    rect_fondo = pygame.Rect(x, y, largo_barra, alto_barra)

    rect_salud = pygame.Rect(
        x,
        y,
        largo_barra * porcentaje_vida,
        alto_barra
    )

    pygame.draw.rect(screen, "red", rect_fondo)
    pygame.draw.rect(screen, "lime", rect_salud)
    pygame.draw.rect(screen, "white", rect_fondo, 2)

    texto = fuente.render(
        f"Vida: {STATS['Vida_Actual']} / {STATS['Vida']}",
        True,
        "white"
    )

    screen.blit(texto, (215, 16))


    #==================== ARMADURA ====================

    porcentaje_armadura = min(STATS["Armadura_Current"] / STATS_MAXIMUM_VALUES["Armadura"], 1)

    y = 50

    rect_fondo = pygame.Rect(x, y, largo_barra, alto_barra)

    rect_armadura = pygame.Rect(
        x,
        y,
        largo_barra * porcentaje_armadura,
        alto_barra
    )

    pygame.draw.rect(screen, "gray25", rect_fondo)
    pygame.draw.rect(screen, "dodgerblue", rect_armadura)
    pygame.draw.rect(screen, "white", rect_fondo, 2)

    texto = fuente.render(
        f"Armadura: {STATS['Armadura_Current']} / {STATS['Armadura']}",
        True,
        "white"
    )

    screen.blit(texto, (215, 46))


    #==================== PASOS ====================

    texto = fuente.render(
        f"Pasos: {restantes}",
        True,
        "white"
    )

    screen.blit(texto, (20, 82))



def main():
    global restantes
    global pasos
    global STATS
    global piso
    global monstruos_current
    
    pygame.init()

    # Cargamos la pantalla previamente para que la funcion auxiliar pueda cargar los sprites de los jugadores
    screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))


    # En este diccionario estaran todos nuestros datos relevantes
    datos = {
        "pos_jugador" : (0, 0),
        "direccion" : (0, 0),
        "tiempo_ultimo_mov" : 0,
        "manzanas_comidas" : 0,
        "screen" : screen,
        "tablero" : [],
        "img_actual" : TextureModule.obtener(T_Handler, "data/imagenes/player/down.png"),
        "elapsed_time_monstruo" : pygame.time.get_ticks(),
        "elapsed_time_manzana" : pygame.time.get_ticks(),
        "tiempo_actual" : 0,
        "estado" : ESTADO_INICIO,
        # Aqui estaran los sprites, simplemente parseados por referencia
        "sprites": {
            "arriba": TextureModule.obtener(T_Handler, "data/imagenes/player/up.png"),
            "abajo": TextureModule.obtener(T_Handler, "data/imagenes/player/down.png"),
            "izquierda": TextureModule.obtener(T_Handler, "data/imagenes/player/left.png"),
            "derecha": TextureModule.obtener(T_Handler, "data/imagenes/player/right.png")
        },
        # Las texturas se cargan con aplicar_texturas_piso_actual(datos)
        "texturas" : {}
    }

    aplicar_texturas_piso_actual(datos)

    pygame.display.set_caption("Juego Básico")
    running = True

    mostrar_pantalla(datos["screen"], PANTALLA_INICIO)
    
    while running:
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False

            if evento.type == pygame.KEYDOWN:
                if datos["estado"] == ESTADO_INICIO:
                    if evento.key == pygame.K_SPACE:
                        iniciar_estado_juego(datos)
                        datos["estado"] = ESTADO_JUGANDO
                    
                    elif evento.key == pygame.K_i:
                        datos["estado"] = ESTADO_INSTRUCCIONES
                        mostrar_pantalla(datos["screen"], PANTALLA_INSTRUCCIONES)

                elif datos["estado"] == ESTADO_INSTRUCCIONES:
                    datos["estado"] = ESTADO_INICIO
                    mostrar_pantalla(datos["screen"], PANTALLA_INICIO)
                
                elif datos["estado"] == ESTADO_VICTORIA:
                    datos["direccion"] = (0, 0)
                    if evento.key == pygame.K_r:
                        datos["estado"] = ESTADO_STATS
                        pygame.mixer.music.pause()
                    elif evento.key == pygame.K_ESCAPE:
                        datos["estado"] = ESTADO_INICIO
                        mostrar_pantalla(datos["screen"], PANTALLA_INICIO)
                
                elif datos["estado"] == ESTADO_DERROTA:
                    
                    if evento.key == pygame.K_r:
                            reiniciar_estado_juego(datos)
                            datos["estado"] = ESTADO_JUGANDO
                    if evento.key == pygame.K_ESCAPE:
                        datos["estado"] = ESTADO_INICIO
                        mostrar_pantalla(datos["screen"], PANTALLA_INICIO)

                elif datos["estado"] == ESTADO_JUGANDO:              
                    cambiar_direccion(pygame.key.get_pressed(), datos)
                
                elif datos["estado"] == ESTADO_STATS:
                    if evento.key == pygame.K_r:
                        piso = min(piso + 1, 3)

                        # 1) Primero cambiamos las texturas al piso nuevo.
                        actualizar_texturas_piso(datos)

                        # 2) Luego cargamos la música del piso nuevo.
                        pygame.mixer.music.load(pisos_datos[piso]["Sonidos"]["Musica"])
                        pygame.mixer.music.set_volume(0)
                        pygame.mixer.music.play(-1)

                        # 3) Recién ahora reiniciamos y dibujamos el tablero.
                        # Así nunca se alcanza a ver el nivel anterior.
                        reiniciar_estado_juego(datos)
                        datos["estado"] = ESTADO_JUGANDO

                    elif evento.key == pygame.K_ESCAPE:
                        piso = min(piso + 1, 3)
                        actualizar_texturas_piso(datos)
                        datos["estado"] = ESTADO_INICIO
                        mostrar_pantalla(datos["screen"], PANTALLA_INICIO)

        if datos["estado"] == ESTADO_JUGANDO:
            factor_velocidad = STATS["Velocidad"] / 200.0

            spawnrate_ringos = pisos_datos[piso]["Datos"]["SPAWN_RATE_MANZANAS"] * factor_velocidad
            datos["tiempo_actual"] = pygame.time.get_ticks()

            if (datos["tiempo_actual"] - datos["elapsed_time_monstruo"]) >= pisos_datos[piso]["Datos"]["SPAWN_RATE"]:
                spawn_objects(datos["tablero"], MONSTRUO)
                datos["elapsed_time_monstruo"] = datos["tiempo_actual"]
                refrescar_tablero(datos)

            if (datos["tiempo_actual"] - datos["elapsed_time_manzana"]) >= spawnrate_ringos:
                spawn_objects(datos["tablero"], MANZANA)
                datos["elapsed_time_manzana"] = datos["tiempo_actual"]
                refrescar_tablero(datos)

            # Movimiento por ticks
            if datos["direccion"] != (0, 0) and datos["tiempo_actual"] - datos["tiempo_ultimo_mov"] >= STATS["Velocidad"]:
                resultado = avanzar(datos)

                if resultado == "derrota":
                    if STATS["Vidas_Adicionales_Current"] > 0:
                        STATS["Vidas_Adicionales_Current"] = max(0, STATS["Vidas_Adicionales_Current"] - 1)
                        STATS["Vida_Actual"] = min(STATS["Vida_Actual"] + 1, STATS["Vida"])

                        avanzar_personaje(datos)
                    else:
                        datos["estado"] = ESTADO_DERROTA
                        restantes = STATS["Pasos_Max"]
                        pasos = 0
                        reestablecer_stats()
                        mostrar_pantalla(datos["screen"], PANTALLA_DERROTA)
                        allowed_to_continue["allowed"] = False
                
                elif resultado == "victoria":
                    datos["estado"] = ESTADO_VICTORIA
                    restantes = STATS["Pasos_Max"]
                    pasos = 0
                    reestablecer_stats()
                    mostrar_pantalla(datos["screen"], PANTALLA_VICTORIA)
                
                else:
                    avanzar_personaje(datos)
                        
    pygame.quit()


if __name__ == "__main__":
    main()
#test personaje