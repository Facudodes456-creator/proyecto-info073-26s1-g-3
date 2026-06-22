import os
import random

import pygame

# Estados del juego
ESTADO_INICIO = "inicio"
ESTADO_INSTRUCCIONES = "instrucciones"
ESTADO_JUGANDO = "jugando"
ESTADO_DERROTA = "derrota"
ESTADO_VICTORIA = "victoria"

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
MANZANAS_OBJETIVO = 5

#Variables misc
piso = 0
monstruos_current = 0
manzanas_current = 0
manzanas_max = 2

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
            "MANZANAS_OBJETIVO" : 8,
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
            "MANZANAS_OBJETIVO" : 11,
        },
        "Placeholder_Futuro" : {} #Por si tenemos que agregar algo mas
    },

}

#Diccionario que contiene la informacion de nuestro personaje
STATS = {
    "Vida" : 3,
    "Vida_Actual" : 3,
    "Velocidad" : 200, # Esta variable hace alucion a el  retraso entre cada movimiento
    "Vidas_Adicionales" : 0, # Al consumir 4 puntos disponibles en mejorar esta metrica, se obtendra una resurreccion
    "Puntos_disponibles" : 0, # Aqui guardaremos los puntos disponibles, se conseguiran 4 puntos cada piso completado, y 0.5 puntos por cada monstruo derrotado en el piso (No cuentan los monstruos derrotados si no pasas el piso)
    "Armadura" : 1, # Cada punto de armadura es 1 punto de defensa que protege al jugador de 1 solo hit por cada punto de armadura, por ejemplo si tienes 2 de armadura y 4 de vida, y tocas a 3 monstruos, tu vida restante sera de 3, 2 golpes habran sido tankeados por la armadura
    "Armadura_Current" : 1,
    "Pasos_Max" : 75
}

# Variable global para pasos restantes, y pasos realizados
restantes = STATS["Pasos_Max"]
pasos = 0

# Tamaño del tablero
# Si se cambian estas constantes, se debe modificar la definición
# del tablero que se encuentra en función reiniciar().
FILAS = 15
COLUMNAS = 15

ACHO_VENTANA = 1040
ALTO_VENTANA = 800

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
            
        
        STATS["Vida"] += (puntos_inputeados // 2)
        msj = f"Exito. Tus puntos de vida ahora son {STATS['Vida']}."
    elif id_stat == "Velocidad":
        if puntos_inputeados % 2 != 0 and puntos_inputeados > 1:
            puntos_inputeados -= 1
        elif puntos_inputeados < 1:
           return "Error, no tienes puntos suficientes."
        
        STATS["Velocidad"] = max(75, STATS["Velocidad"] - (puntos_inputeados * 10))
        msj =  f"Exito. Tu velocidad se reducio a {STATS['Velocidad']} milisegundos."
    elif id_stat == "Vidas_Adicionales":
        if puntos_inputeados < 4:
            return "Error, no tienes puntos suficientes."
        else:
            puntos_inputeados = 4

            STATS["Vidas_Adicionales"] += 1
            msj =  f"Exito. Ahora tienes {STATS['Vidas_Adicionales']} vidas adicionales."
    elif id_stat == "Pasos_Max":

        STATS["Pasos_Max"] += (puntos_inputeados * 5)
        msj =  f"Exito. Ahora tus pasos maximos son {STATS['Pasos_Max']} pasos."
    
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

def spawn_objects(tablero, id_elem):
    global monstruos_current
    global piso
    global pisos_datos

    if id_elem == MANZANA:
        if manzanas_current < manzanas_max:
            aparecer_aleatorio(tablero, id_elem)
    elif id_elem == MONSTRUO:
        if monstruos_current < pisos_datos[piso]["Datos"]["MONSTRUOS_MAX"]:
            aparecer_aleatorio(tablero, id_elem)




def refrescar_tablero(screen, tablero, img_jugador):
    global piso
    global pisos_datos

    screen.fill("gray30")
    
    wall = pygame.image.load(pisos_datos[piso]["Texturas"]["Pared"]).convert()
    apple = pygame.image.load(pisos_datos[piso]["Texturas"]["Manzana"]).convert_alpha()
    floor = pygame.image.load(pisos_datos[piso]["Texturas"]["Piso"]).convert()
    monster = pygame.image.load(pisos_datos[piso]["Texturas"]["Monstruo"]).convert()

    alto_elem = screen.get_height() / FILAS
    ancho_elem = screen.get_width() / COLUMNAS

    pos_y = 0
    for i in range(FILAS):
        pos_x = 0
        for j in range(COLUMNAS):

            # Dibujamos la base que es el suelo en todos los tiles
            if tablero[i][j] in (SUELO, JUGADOR, MANZANA, MONSTRUO):
                screen.blit(floor, [pos_x, pos_y])

            # Aqui dibujamos cada elemento correspondiente encima de el
            if tablero[i][j] == OBSTACULO:
                screen.blit(wall, [pos_x, pos_y])
            elif tablero[i][j] == JUGADOR:
                screen.blit(img_jugador, [pos_x + 2, pos_y + 2])
            elif tablero[i][j] == MANZANA:
                screen.blit(apple, [pos_x, pos_y])
            elif tablero[i][j] == MONSTRUO:
                screen.blit(monster, [pos_x, pos_y])

            pos_x += ancho_elem
        pos_y += alto_elem

    pygame.display.flip()


def cambiar_direccion(keys, direccion_actual):
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
        return (0, -1)

    # Tecla S
    if keys[pygame.K_s]:
        # En este caso avanzará a través de las filas del tablero.
        return (0, 1)

    # Tecla A
    if keys[pygame.K_a]:
        # Retrocede por las columnas del tablero.
        return (-1, 0)

    # Tecla D
    if keys[pygame.K_d]:
        # Avanza por las columnas del tablero.
        return (1, 0)

    # Si no se presiona ninguna de las teclas anteriores, la dirección
    # será la misma que la anterior.
    return direccion_actual


def avanzar(tablero, pos_jugador, direccion,manzanas_comidas):
    """
    Avanza el jugador un paso en la dirección dada.

    Parámetros:
        - tablero: El tablero con sus posiciones actuales.
        - pos_jugador: Tupla con la posición actual (índice con
            estructura (columna, fila)) del jugador en el tablero.
        - direccion: Tupla con la dirección en la que está avanzando actualmente el jugador.

    Retorna:
        - (resultado, nueva_pos_jugador): Retorna el resultado que se obtiene
            al avanzar (derrota, victoria o "ok" (no cambia de pantalla)) y la nueva posición del jugador.
    """

    # Obtenemos los componentes "x" e "y" de cada tupla recibida
    # con información de la dirección y posición del jugador.
    global restantes
    global pasos
    global STATS
    global pisos_datos
    global monstruos_current
    global manzanas_current

    dir_col, dir_fila = direccion
    ind_actual_col, ind_actual_fila = (
        pos_jugador  # Tupla (columna, fila) que representa los índices en el tablero.
    )

    # Aplicamos la dirección a la posición del jugador.
    ind_nueva_col = ind_actual_col + dir_col
    ind_nueva_fila = ind_actual_fila + dir_fila

    # Verificamos que no haya choque con el borde del tablero.
    if not (0 <= ind_nueva_col < COLUMNAS and 0 <= ind_nueva_fila < FILAS):
        return "derrota", pos_jugador,manzanas_comidas

    # Obtenemos el elemento que se encuentre en el tablero en la nueva posición del jugador.
    pos_elem = tablero[ind_nueva_fila][ind_nueva_col]

    if pos_elem == OBSTACULO:
        return "derrota", pos_jugador,manzanas_comidas
    elif pos_elem == MONSTRUO:
        if STATS["Armadura_Current"] > 0:
            STATS["Armadura_Current"] -= 1
        else:
            STATS["Vida_Actual"] -= 1

        monstruos_current = max(0, monstruos_current - 1)
        if STATS["Vida_Actual"] <= 0:
            return "derrota", pos_jugador,manzanas_comidas

    if pos_elem == MANZANA:
        manzanas_comidas += 1
        manzanas_current = max(0, manzanas_current - 1)
        # Agregamos 5 pasos a el jugador, procurando de no sobrepasar los 50 pasos maximos.
        pasos -= 6

        tablero[ind_actual_fila][ind_actual_col] = SUELO
        tablero[ind_nueva_fila][ind_nueva_col] = JUGADOR

        if manzanas_comidas >= pisos_datos[piso]["Datos"]["MANZANAS_OBJETIVO"]:
            return "victoria", (ind_nueva_col, ind_nueva_fila), manzanas_comidas

        return "ok", (ind_nueva_col, ind_nueva_fila), manzanas_comidas

    # Movimiento normal, si es que no encontramos manzana ni obstáculo.
    tablero[ind_actual_fila][ind_actual_col] = SUELO
    tablero[ind_nueva_fila][ind_nueva_col] = JUGADOR

    return "ok", (ind_nueva_col, ind_nueva_fila), manzanas_comidas


def reiniciar():
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
    tablero = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

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
    poblar_tablero(tablero)

    # Colocamos al jugador en una posición aleatoria.
    pos_jugador = aparecer_aleatorio(tablero, JUGADOR)

    return tablero, pos_jugador


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


def main():
    pygame.init()

    # Establecemos la resolución de la pantalla.
    screen = pygame.display.set_mode((800, 800))

    # Establecemos el título de la ventana.
    pygame.display.set_caption("Juego Básico")

    running = True

    global restantes
    global pasos
    global STATS
    global piso
    global monstruos_current

    estado = ESTADO_INICIO
    tablero = []
    pos_jugador = (0, 0)
    direccion = (0, 0)
    tiempo_ultimo_mov = 0
    manzanas_comidas = 0
    mostrar_pantalla(screen, PANTALLA_INICIO)
    img_arriba = pygame.image.load("data/imagenes/player/up.png").convert_alpha()
    img_abajo = pygame.image.load("data/imagenes/player/down.png").convert_alpha()
    img_izq = pygame.image.load("data/imagenes/player/left.png").convert_alpha()
    img_der = pygame.image.load("data/imagenes/player/right.png").convert_alpha()

    img_arriba = pygame.transform.scale(img_arriba, (53, 53))
    img_abajo = pygame.transform.scale(img_abajo, (53, 53))
    img_izq = pygame.transform.scale(img_izq, (53, 53))
    img_der = pygame.transform.scale(img_der, (53, 53))

    img_actual = img_abajo

    img_actual = img_abajo
    # Este es el bucle principal del juego, todo lo que sucede en el juego
    # está aquí.
    
    elapsed_time_monstruo = pygame.time.get_ticks()
    elapsed_time_manzana = pygame.time.get_ticks()
    while running:
        # Se analizan los eventos del bucle actual.
        for evento in pygame.event.get():
            # Si es que se quiere cerrar la ventana.
            if evento.type == pygame.QUIT:
                running = False

            # Si es que se presiona alguna tecla.
            if evento.type == pygame.KEYDOWN:
                if estado == ESTADO_INICIO:
                    if evento.key == pygame.K_SPACE:
                        piso = min(piso + 1, 3)
                        tablero, pos_jugador = reiniciar()
                        manzanas_comidas = 0
                        direccion = (0, 0)
                        img_actual = img_abajo
                        # Obtiene tiempo en milisegundos
                        tiempo_ultimo_mov = pygame.time.get_ticks()
                        elapsed_time_monstruo = pygame.time.get_ticks()
                        elapsed_time_manzana = pygame.time.get_ticks()
                        estado = ESTADO_JUGANDO
                        pygame.mixer.music.load(pisos_datos[piso]["Sonidos"]["Musica"])
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(-1)


                        refrescar_tablero(screen, tablero, img_actual)
                    elif evento.key == pygame.K_i:
                        estado = ESTADO_INSTRUCCIONES
                        mostrar_pantalla(screen, PANTALLA_INSTRUCCIONES)

                elif estado == ESTADO_INSTRUCCIONES:
                    estado = ESTADO_INICIO
                    mostrar_pantalla(screen, PANTALLA_INICIO)

                elif estado in (ESTADO_DERROTA, ESTADO_VICTORIA):
                    pygame.mixer.music.pause()
                    if evento.key == pygame.K_r:
                        if estado == ESTADO_VICTORIA:
                            piso = min(piso + 1, 3)
                        tablero, pos_jugador = reiniciar()
                        manzanas_comidas = 0
                        direccion = (0, 0)
                        img_actual = img_abajo
                        tiempo_ultimo_mov = pygame.time.get_ticks()
                        elapsed_time_monstruo = pygame.time.get_ticks()
                        elapsed_time_manzana = pygame.time.get_ticks()
                        estado = ESTADO_JUGANDO
                        pygame.mixer.music.unpause()
                        refrescar_tablero(screen, tablero, img_actual)

                    if evento.key == pygame.K_ESCAPE:
                        estado = ESTADO_INICIO
                        mostrar_pantalla(screen, PANTALLA_INICIO)

                elif estado == ESTADO_JUGANDO:              
                    direccion = cambiar_direccion(pygame.key.get_pressed(), direccion)

        if estado == ESTADO_JUGANDO:
            tiempo_actual = pygame.time.get_ticks()  # En milisegundos
            if (tiempo_actual - elapsed_time_monstruo) >= pisos_datos[piso]["Datos"]["SPAWN_RATE"]:
                spawn_objects(tablero, MONSTRUO)
                elapsed_time_monstruo = tiempo_actual
                refrescar_tablero(tablero)

            if (tiempo_actual - elapsed_time_manzana) >= pisos_datos[piso]["Datos"]["SPAWN_RATE_MANZANAS"]:
                spawn_objects(tablero, MANZANA)
                elapsed_time_manzana = tiempo_actual
                refrescar_tablero(tablero)

            # La variable STATS["Velocidad"] hace que si no han pasado esa cantidad de ticks,
            # entonces no se avanzará en el tablero.
            if direccion != (0, 0) and tiempo_actual - tiempo_ultimo_mov >= STATS["Velocidad"]:
                resultado, pos_jugador, manzanas_comidas = avanzar(tablero, pos_jugador, direccion, manzanas_comidas)

                if resultado == "derrota":
                    estado = ESTADO_DERROTA
                    restantes = STATS["Pasos_Max"]
                    pasos = 0
                    STATS["Vida_Actual"] = STATS["Vida"]
                    STATS["Armadura_Current"] = STATS["Armadura"]
                    mostrar_pantalla(screen, PANTALLA_DERROTA)
                elif resultado == "victoria":
                    estado = ESTADO_VICTORIA
                    restantes = STATS["Pasos_Max"]
                    pasos = 0
                    STATS["Vida_Actual"] = STATS["Vida"]
                    STATS["Armadura_Current"] = STATS["Armadura"]
                    mostrar_pantalla(screen, PANTALLA_VICTORIA)
                else:
                    tiempo_ultimo_mov = tiempo_actual
                    pasos += 1
                    restantes = STATS["Pasos_Max"] - pasos
                    pygame . display . set_caption ( f" Juego - Pasos restantes : {restantes}")
                    if pasos >= STATS["Pasos_Max"]:
                        estado = ESTADO_DERROTA
                        restantes = STATS["Pasos_Max"]
                        pasos = 0
                        STATS["Vida_Actual"] = STATS["Vida"]
                        STATS["Armadura_Current"] = STATS["Armadura"]
                        mostrar_pantalla(screen, PANTALLA_DERROTA)
                    else:
                        if direccion == (0, -1):
                          img_actual = img_arriba

                        elif direccion == (0, 1):
                          img_actual = img_abajo

                        elif direccion == (-1, 0):
                         img_actual = img_izq

                        elif direccion == (1, 0):
                         img_actual = img_der

                        refrescar_tablero(screen, tablero, img_actual)
                        
                
                

    pygame.quit()


if __name__ == "__main__":
    main()
#test personaje