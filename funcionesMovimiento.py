#Constantes


LIMITE_DERECHO = 32
LIMITE_IZQUIERDO = 1
LIMITE_SUPERIOR = 91
LIMITE_INFERIOR = 64
PARED = 0
JUGADOR = 2
BLOQUE_CAMINABLE = 1
DERECHA = 1
IZQUIERDA= -1
ARRIBA= -1
ABAJO= 1


def encontrarJugador(sala: dict):
    """Esta funcion se encarga de encontrar la posicion del jugador"""
    listaLlaves = list(sala.keys())
    listaValores = list(sala.values())
    posicionenLista = listaValores.index(JUGADOR)
    return listaLlaves[posicionenLista]


def movimientoHorizontal(sala: dict, jugadorPos: str, letraJugador: str, numeroJugador: str, sentido: int):
    """Esta funcion se encarga de mover al jugador en el eje horizontal"""
    try:
        numeroJugador = int(numeroJugador) + sentido
        if len(str(numeroJugador)) == 1: #Arregla las columnas de 01 a 09
            numeroJugador = "0" + str(numeroJugador)
            
        if  LIMITE_IZQUIERDO > int(numeroJugador)+1 > LIMITE_DERECHO:
            print("El jugador se va del area")
        elif sala[letraJugador + str(numeroJugador)] == PARED:
            print("El jugador golpea una pared")
        else:
            temporal = sala[letraJugador + str(numeroJugador)]
            sala[letraJugador + str(numeroJugador)] = JUGADOR
            sala[jugadorPos] = BLOQUE_CAMINABLE
            return temporal
    except KeyError:
        print("El jugador se va del area")


def movimientoVertical(sala: dict, jugadorPos: str, letraJugador: str, sentido: int):
    """Esta funcion se encarga de mover al jugador en el eje vertical"""
    nuevaLetra = chr(ord(letraJugador) + sentido)
    if not (LIMITE_INFERIOR < ord(nuevaLetra) < LIMITE_SUPERIOR):
        print("El jugador se va del area")
    elif sala[nuevaLetra + jugadorPos[1:]] == PARED:
        print("El jugador golpea una pared")
    else:
        temporal = sala[nuevaLetra + jugadorPos[1:3]]
        sala[nuevaLetra + jugadorPos[1:]] = JUGADOR
        sala[jugadorPos] = BLOQUE_CAMINABLE
        return temporal


def hacerMovimiento(sala: dict):
    """Esta funcion se encarga de hacer el movimiento del jugador"""
    eleccion = input(
        "Ingrese un movimiento con WASD(w arriba, A izquierda,D Derecha y S abajo): ")
    while eleccion not in "wasd" or len(eleccion) != 1:
        eleccion = input("Ingrese un movimiento valido: ")

    jugadorPos = encontrarJugador(sala)
    letraJugador = jugadorPos[0]

    if eleccion == "w":
        return movimientoVertical(sala, jugadorPos, letraJugador, ARRIBA)
    elif eleccion == "s":
        return movimientoVertical(sala, jugadorPos, letraJugador, ABAJO)
    elif eleccion == "a":
        numeroJugador = jugadorPos[1:]
        return movimientoHorizontal(sala, jugadorPos, letraJugador, numeroJugador, IZQUIERDA)
    elif eleccion == "d":
        numeroJugador = jugadorPos[1:]
        return movimientoHorizontal(sala, jugadorPos, letraJugador, numeroJugador, DERECHA)
