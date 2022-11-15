import random

ASCIILETRA= 65

"""UTILIZAR PARA EL MAPA GENERADOR"""
INVISIBLE= -1
MURALLA= 0
VACIO= 1
PERSONAJE= 2
SALIDA= 3
ALIADOS= 4
ENEMIGOS= 5

CANTSPAWN= random.randint(12,14)

#PILA FUNCIONES
def _initBloque():
    bloque= list()
    return bloque

def _agregarBloque(bloque: list, dato: str):
    bloque.append(dato)

def _datoBloque(bloque: list):
    """Cambios a la forma normal de la Pila, esta una vez lees el dato lo remueves"""
    dato= bloque[-1]
    bloque.pop()
    return dato

def _longitudBloque(bloque: list):
    return len(bloque)
############################

def genMapa(filas= 18, columnas= 32):
    """Funcion que permite crear la room del juego, usa un diccionario como un mapa y su Key es 'Key[0:1]' su fila y 'Key[1:3]' su columna respectiva"""
    filas= (filas if filas==18 else 18) + ASCIILETRA
    columnas= (columnas if columnas==32 else 32)
    MAPA= dict()
    _crearMapa(MAPA, filas, columnas, MURALLA)
    _generadores(MAPA, filas, columnas)
    return MAPA    

def _crearMapa(mapa: dict, filas: int, columnas: int, rellenar: int):
    """Crea las filas y columnas respectivas con un ID para cada bloque y un valor"""
    numId= 1; letraId= ASCIILETRA
    while letraId <= filas:
        ID= chr(letraId)+(str(numId) if numId>9 else f"0{numId}")
        mapa[ID]= rellenar
        numId+=1
        if numId > columnas:
            letraId+=1; numId= 1

def _generadores(mapa: dict, filas: int, columnas: int):
    """Funcion que acopla todos los generados necesarios para la creacion del mapa"""
    bloquesVacios= set()
    bloquesInflexion= _initBloque()
    _genEntradas(mapa, bloquesInflexion, filas, columnas)
    
    bloqueEntrada= _datoBloque(bloquesInflexion)
    
    _genPuntosInflexion(bloquesInflexion, filas, columnas)
    _genRandom(bloquesVacios, bloqueEntrada, bloquesInflexion)
    
    bloquesEliminar = set()
    for bloque in bloquesVacios:
        borrar= _limpiarBloqueAlrededor(bloque,bloquesVacios,8,False)
        if borrar:
            bloquesEliminar.add(bloque)
    
    bloquesDisponibles= bloquesVacios - bloquesEliminar

    bloquesEvento= dict()
    _genEventos(bloquesDisponibles, bloquesEvento)
    _genCompleto(mapa, bloquesDisponibles, bloquesEvento)
        
def _genEntradas(mapa: dict, puntosInflexion: list, filas: int, columnas: int):
    """Genera una entrada y una salida en el dict"""
    entradaFila= chr(random.randint(66,filas-1)) #EMPEZAR DE B COMO ACCSI HASTA LA PENULTIMA LETRA COMO ACCSI
    salidaFila= chr(random.randint(66,filas-1))
    entradaId= entradaFila+'01'
    primerSlotEntrada= entradaFila+'02'
    salidaId= salidaFila+f"{columnas}"
    primerSlotSalida= salidaFila+f"{columnas-1}"
    mapa[entradaId]= PERSONAJE; mapa[primerSlotEntrada]= VACIO
    mapa[salidaId]= SALIDA; mapa[primerSlotSalida]= VACIO
    _agregarBloque(puntosInflexion, primerSlotSalida)
    _agregarBloque(puntosInflexion, primerSlotEntrada)
    
def _genPuntosInflexion(puntosInflexion: list, filas: int, columnas: int):
    """Puntos que permiten conectar el mapa de forma aleatoria y con un punto final"""
    cuadrante= 1
    vecesHecho= 1
    while vecesHecho < CANTSPAWN:
        seleccion= _genPunto(filas, columnas, cuadrante)
        while seleccion in puntosInflexion:
            seleccion= _genPunto(filas, columnas, cuadrante)
        _agregarBloque(puntosInflexion, seleccion)
        vecesHecho+= 1
        if vecesHecho == CANTSPAWN//2:
            cuadrante= 0

def _genPunto(filas: int, columnas: int, cuadrante: int):
    """Genera puntos de inflexion por 2 cuadrantes de forma vertical"""
    sumValor= 15* cuadrante
    maxValor= ((columnas+1)//2)+sumValor
    seleccionFila= chr(random.randint(66, filas-1))
    seleccionColumna= str(random.randint(2+sumValor, maxValor))
    seleccionColumna= ('0' if len(seleccionColumna) == 1 else '')+ seleccionColumna
    return seleccionFila+ seleccionColumna

def _genRandom(bloquesVacios: set, entrada: str, puntosInflexion: list):
    """Ciclo recursivo que permite crear el mapa hasta llegar a la salida"""
    if puntosInflexion:
        llegada= _datoBloque(puntosInflexion)
        _genCamino(bloquesVacios, entrada, llegada)
        longitudPuntos= _longitudBloque(puntosInflexion)
        if (longitudPuntos*2)== CANTSPAWN:
            entrada2= random.choice(list(bloquesVacios))
            llegada2= _datoBloque(puntosInflexion)
            _genCamino(bloquesVacios, entrada2, llegada2)
        _genRandom(bloquesVacios, llegada, puntosInflexion)

def _genCamino(bloquesVacios, direccionInicio: str, direccionLlegada: str):
    """Establece los parametros para generar una distancia"""
    longitudFila, longitudColumna= _calcularCamino(direccionInicio, direccionLlegada)
    fila, columna= direccionInicio[0:1], direccionInicio[1:3]
    _genBloques(bloquesVacios, fila, columna, longitudFila, longitudColumna)

def _calcularCamino(direccionInicio: str, direccionLlegada: str):
    """Calcula la distancia ± respecto a donde se encuentra un punto con el otro"""
    filaInicio,columnaInicio= direccionInicio[0:1], direccionInicio[1:3]
    filaFinal,columnaFinal= direccionLlegada[0:1], direccionLlegada[1:3]
    longitudFila= (ord(filaFinal)- ord(filaInicio))
    longitudColumna= (int(columnaFinal)- int(columnaInicio))
    return longitudFila,longitudColumna
        
def _genBloques(bloquesVacios: set, fila: int, columna: int, distanciaFila: int, distanciaColumna: int):
    """Genera de movimientos tanto de forma horizontal y vertical siempre acercandose al punto que debe conectar"""
    movFila, movColumna = (1 if distanciaFila > 0 else -
                           1), (1 if distanciaColumna > 0 else -1)
    mov = random.choice(["fila", "columna"])
    while distanciaFila != 0 or distanciaColumna != 0:
        if mov == "fila" and distanciaFila != 0:
            if distanciaFila < 5 and distanciaFila > -5:
                vecesMov = distanciaFila
            else:
                vecesMov = random.randint(1, 4)*movFila
            for i in range(0, vecesMov+movFila, movFila):
                _fila = chr(ord(fila)+i)
                bloquesVacios.add(_fila + columna)
            fila = _fila
            distanciaFila += -1*vecesMov
        elif mov == "columna" and distanciaColumna != 0:
            if distanciaColumna < 5 and distanciaColumna > -5:
                vecesMov = distanciaColumna
            else:
                vecesMov = random.randint(1, 4)*movColumna
            for j in range(0, vecesMov+movColumna, movColumna):
                _columna = (str(int(columna)+j) if int(columna) +
                            j > 9 else '0' + str(int(columna)+j))
                bloquesVacios.add(fila + _columna)
            columna = _columna
            distanciaColumna += -1*vecesMov
        mov = random.choice(["fila", "columna"])
    
def _genEventos(bloquesDisponibles: set, bloquesEventos: dict):
    """Genera eventos"""
    bloquesDisponibles= list(bloquesDisponibles)
    cantEnemigos= random.randint(9,12)
    cantAliados= random.randint(2,3)
    numEvento= 0
    while numEvento != cantEnemigos:
        if numEvento >= cantAliados:
            eventoNegativo= random.choice(bloquesDisponibles)
            eventoRenovar= _limpiarBloqueAlrededor(eventoNegativo, set(bloquesEventos), 1, True)
            while eventoRenovar:
                eventoNegativo= random.choice(bloquesDisponibles)
                eventoRenovar= _limpiarBloqueAlrededor(eventoNegativo, set(bloquesEventos), 1, True)
            bloquesEventos[eventoNegativo]= ENEMIGOS
            
        else:
            eventoNegativo= random.choice(bloquesDisponibles)
            eventoRenovar= _limpiarBloqueAlrededor(eventoNegativo, set(bloquesEventos), 1, True)
            while eventoRenovar:
                eventoNegativo= random.choice(bloquesDisponibles)
                eventoRenovar= _limpiarBloqueAlrededor(eventoNegativo, set(bloquesEventos), 1, True)
            bloquesEventos[eventoNegativo]= ENEMIGOS
            
            eventoPositivo= random.choice(bloquesDisponibles)
            eventoRenovar= _limpiarBloqueAlrededor(eventoPositivo, set(bloquesEventos), 1, True)
            while eventoRenovar:
                eventoPositivo= random.choice(bloquesDisponibles)
                eventoRenovar= _limpiarBloqueAlrededor(eventoPositivo, set(bloquesEventos), 1, True)
            bloquesEventos[eventoPositivo]= ALIADOS  
        numEvento+=1
    
def _limpiarBloqueAlrededor(bloque: str, removerCasos: set, cantMaximaCaso: int, revisarMismo: bool):
    """Busca los arrededores para compararlo con algunos casos que se especifiquen en los parametros"""
    quitar= False; maxIguales= 0; bloquesColumna= -1
    filaBase,columnaBase= ord(bloque[0:1]), int(bloque[1:])
    while bloquesColumna != 2:
        """El 2 es debido a su posicion maxima que recorre siendo X Y su posicion  y las demas sus alrededores
            x-1 y-1 | x-1 y | x-1 y+1
             x  y-1 |  X Y  |  x  y+1
            x+1 y-1 | x+1 y | x+1 y+1   """
        try:
            cont= 1 if bloquesColumna!= 0 or revisarMismo else 2
            columnaTest= columnaBase+ bloquesColumna
            columnaTest= ('0' if columnaTest < 10 else '')+ str(columnaTest)
            for movFila in range(-1,2,cont):
                filaTest= chr(filaBase+ movFila)
                puntoTest= filaTest+columnaTest
                if puntoTest in removerCasos:
                    maxIguales+=1
                    if maxIguales == cantMaximaCaso:
                        quitar= True
                        raise KeyError
            bloquesColumna+= 1
        except KeyError:
            break
    return quitar

def _genCompleto(mapa: dict ,bloques: set, bloquesEventos: dict):
    for cord in bloques:
        mapa[cord]= VACIO
    for cord,valor in bloquesEventos.items():
        mapa[cord]= valor

def genMapaInvisible():
    """Genera mapa que ve el jugador"""
    mapaSuplente= dict()
    filas= ASCIILETRA+18
    columnas= 32
    _crearMapa(mapaSuplente, filas, columnas, INVISIBLE)
    return mapaSuplente

def reconocerEntorno(mapa: dict, mapaSuplente: dict, posPersonaje: str):
    """Aydua a sincronizar lo que ve el jugador con lo que hay en el mapa y en el mapa Invisible"""
    posFila, posColumna= ord(posPersonaje[0:1]), int(posPersonaje[1:])
    verColumna= -1
    while verColumna != 2:
        columnaId= posColumna+ verColumna
        columnaId= ('0' if columnaId < 10 else '')+ str(columnaId)
        for movFila in range(-1,2):
            filaId= chr(posFila+movFila)
            reconocerPunto= filaId+columnaId
            try:
                mapaSuplente[reconocerPunto]= mapa[reconocerPunto]
            except KeyError:
                pass
        verColumna+= 1

def imprimirMapa(mapa: dict):
    colores = {-1: "  ", 0: "⬜", 1: "⬛", 2: "👨",
           3: "🟩", 4: "⬛", 5: "⬛"}
    for i in mapa.keys():
        print(colores[mapa[i]], end= '')
        if i[1:3] == '32':
            print()
        
        
    

def main():
    mapa= genMapa()
    mapaInvisible= genMapaInvisible()
    
    imprimirMapa(mapa)

if __name__ == "__main__":
    main()