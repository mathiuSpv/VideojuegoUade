#CONSTANTES
MOVIMIENTOS = 'wasd'
MOV_ARRIBA = 'w'
MOV_ABAJO = 's'
MOV_IZQUIERDA = 'a'
MOV_DERECHA = 'd'
SUBIR = 1
BAJAR = -1
IZQUIERDA = -1
DERECHA = 1

LIMITE_DERECHO_MAPA=26
LIMITE_IZQUIERDO_MAPA=0
LIMITE_SUPERIOR_MAPA=64
LIMITE_INFERIOR_MAPA=91

def encontrarJugador(sala: dict):
    new_ke_lis = list(sala.keys())
    new_val = list(sala.values())
    new_pos = new_val.index(3)
    return new_ke_lis[new_pos]

def verificarMovimientoHorizontal(sala:dict,letraJugador:str, numeroJugador:str):
    esMovimientoRealizable = False
    if int(numeroJugador) >= LIMITE_DERECHO_MAPA or int(numeroJugador) <= LIMITE_IZQUIERDO_MAPA:
        print("El jugador se va del area")
    elif sala[letraJugador + str(numeroJugador)] == 1:
        print("El jugador golpea una pared")
    else:
        esMovimientoRealizable = True
    return esMovimientoRealizable

def verificarMovimientoVertical(sala:dict,jugadorPos:str,nuevaLetra:str):
    esMovimientoRealizable = False
    if not (LIMITE_SUPERIOR_MAPA < ord(nuevaLetra) < LIMITE_INFERIOR_MAPA):
        print("El jugador se va del area")
    elif sala[nuevaLetra + jugadorPos[1:3]] == 1:
        print("El jugador golpea una pared")
    else:
        esMovimientoRealizable = True
    return esMovimientoRealizable

def movimientoHorizontal(sala:dict,jugadorPos:str,letraJugador:str,numeroJugador:str,sentido:int):
    numeroJugador = int(numeroJugador) + sentido
    if len(str(numeroJugador)) == 1:
        numeroJugador = "0" + str(numeroJugador)   
    if verificarMovimientoHorizontal(sala,letraJugador, numeroJugador) == True:
        temporal = sala[letraJugador + str(numeroJugador)]
        sala[letraJugador + str(numeroJugador)] = 3
        sala[jugadorPos] = 0
        return temporal  

def movimientoVertical(sala:dict,jugadorPos:str,letraJugador:str,sentido:int):
    nuevaLetra = chr(ord(letraJugador) + sentido)
    if verificarMovimientoVertical(sala,jugadorPos,nuevaLetra) == True:
        temporal = sala[nuevaLetra + jugadorPos[1:3]]
        sala[nuevaLetra + jugadorPos[1:3]] = 3
        sala[jugadorPos] = 0
        return temporal

def elegirMovimiento():
    eleccion=input("Ingrese un movimiento con WASD(w arriba, A izquierda,D Derecha y S abajo): ")
    eleccion = eleccion.lower()
    while eleccion not in MOVIMIENTOS or len(eleccion) != 1:
        eleccion = input("Ingrese un movimiento valido: ")
        eleccion = eleccion.lower()
    return eleccion

def ejecutarMovimeno(sala:dict, jugadorPos:str, letraJugador:str, eleccion:int):
    if eleccion == MOV_ARRIBA:
        return movimientoVertical(sala,jugadorPos,letraJugador,BAJAR)
    elif eleccion == MOV_ABAJO:
        return movimientoVertical(sala,jugadorPos,letraJugador,SUBIR)
    elif eleccion == MOV_IZQUIERDA:
        numeroJugador = jugadorPos[1:]
        return movimientoHorizontal(sala,jugadorPos,letraJugador,numeroJugador,IZQUIERDA)
    elif eleccion == MOV_DERECHA:
        numeroJugador = jugadorPos[1:]
        return movimientoHorizontal(sala,jugadorPos,letraJugador,numeroJugador,DERECHA)

def realizarJugada(sala: dict):   
    eleccion = elegirMovimiento()
    jugadorPos = encontrarJugador(sala)
    letraJugador = jugadorPos[0]
    ejecutarMovimeno(sala,jugadorPos,letraJugador,eleccion)
