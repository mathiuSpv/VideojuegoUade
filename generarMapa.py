import random

"""Valores int de cada evento"""
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
    filas= (filas if filas==18 else 18) + 65
    columnas= (columnas if columnas==32 else 32)
    SALA= dict()
    _crearSala(SALA, filas, columnas)
    _generadores(SALA, filas, columnas)
    return SALA    

def _crearSala(sala: dict, filas: int, columnas: int):
    numId= 1; letraId= 65
    while letraId <= filas:
        ID= chr(letraId)+(str(numId) if numId>9 else f"0{numId}")
        sala[ID]= MURALLA
        numId+=1
        if numId > columnas:
            letraId+=1; numId= 1

def _generadores(sala: dict, filas: int, columnas: int):
    bloquesVacios= set()
    bloquesInflexion= _initBloque()
    _genEntradas(sala, bloquesInflexion, filas, columnas)
    
    bloqueEntrada= _datoBloque(bloquesInflexion)
    
    _genPuntosInflexion(bloquesInflexion, bloqueEntrada, filas, columnas)
    _genRandom(bloquesVacios, bloqueEntrada, bloquesInflexion)
    
    bloquesEliminar = set()
    for bloque in bloquesVacios:
        borrar= _limpiarBloqueAlrededor(bloque,bloquesVacios,8,False)
        if borrar:
            bloquesEliminar.add(bloque)
    
    bloquesDisponibles= bloquesVacios - bloquesEliminar

    bloquesEvento= dict()
    _genEventos(bloquesDisponibles, bloquesEvento)
    
    for cord in bloquesDisponibles:
        sala[cord]= VACIO
    for cord,valor in bloquesEvento.items():
        sala[cord]= valor
        

def _genEntradas(sala: dict, puntosInflexion: list, filas: int, columnas: int):
    entradaFila= chr(random.randint(66,filas-1)) #EMPEZAR DE B COMO ACCSI HASTA LA PENULTIMA LETRA COMO ACCSI
    salidaFila= chr(random.randint(66,filas-1))
    entradaId= entradaFila+'01'
    primerSlotEntrada= entradaFila+'02'
    salidaId= salidaFila+f"{columnas}"
    primerSlotSalida= salidaFila+f"{columnas-1}"
    sala[entradaId]= PERSONAJE; sala[primerSlotEntrada]= VACIO
    sala[salidaId]= SALIDA; sala[primerSlotSalida]= VACIO
    _agregarBloque(puntosInflexion, primerSlotSalida)
    _agregarBloque(puntosInflexion, primerSlotEntrada)
    
def _genPuntosInflexion(puntosInflexion: list, entrada: str, filas: int, columnas: int):
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

def _genPunto(filas: int, columnas: int, cuadrante):
    sumValor= 15* cuadrante
    maxValor= ((columnas+1)//2)+sumValor
    seleccionFila= chr(random.randint(66, filas-1))
    seleccionColumna= str(random.randint(2+sumValor, maxValor))
    seleccionColumna= ('0' if len(seleccionColumna) == 1 else '')+ seleccionColumna
    return seleccionFila+ seleccionColumna

def _genRandom(bloquesVacios: set, entrada: str, puntosInflexion: list):
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
    longitudFila, longitudColumna= _calcularCamino(direccionInicio, direccionLlegada)
    fila, columna= direccionInicio[0:1], direccionInicio[1:3]
    _genBloques(bloquesVacios, fila, columna, longitudFila, longitudColumna)

def _calcularCamino(direccionInicio: str, direccionLlegada: str):
    filaInicio,columnaInicio= direccionInicio[0:1], direccionInicio[1:3]
    filaFinal,columnaFinal= direccionLlegada[0:1], direccionLlegada[1:3]
    longitudFila= (ord(filaFinal)- ord(filaInicio))
    longitudColumna= (int(columnaFinal)- int(columnaInicio))
    return longitudFila,longitudColumna
        
def _genBloques(bloquesVacios: set, fila: int, columna: int, longitudFila: int, longitudColumna: int):
    movFila, movColumna= (1 if longitudFila> 0 else -1),(1 if longitudColumna> 0 else -1)
    mov= random.choice(["fila","columna"])
    while longitudFila != 0 or longitudColumna !=  0:
        if mov== "fila" and longitudFila != 0:
            if longitudFila < 5 and longitudFila > -5:
                vecesMov= longitudFila
            else:
                vecesMov= random.randint(1,4)*movFila
            for i in range(0,vecesMov+movFila,movFila):
                _fila= chr(ord(fila)+i)
                bloquesVacios.add(_fila+ columna)
            fila= _fila; longitudFila+= -1*vecesMov
        elif mov == "columna" and longitudColumna != 0:
            if longitudColumna < 5 and longitudColumna > -5:
                vecesMov= longitudColumna
            else:
                vecesMov= random.randint(1,4)*movColumna
            for j in range(0,vecesMov+movColumna,movColumna):
                _columna= (str(int(columna)+j) if int(columna)+j>9 else '0'+ str(int(columna)+j))
                bloquesVacios.add(fila+ _columna)
            columna= _columna; longitudColumna+= -1*vecesMov
        mov= random.choice(["fila","columna"])
    
def _genEventos(bloquesDisponibles: set, bloquesEventos: dict):
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
    quitar= False; maxIguales= 0; bloquesColumna= -1
    filaBase,columnaBase= ord(bloque[0:1]), int(bloque[1:])
    while bloquesColumna != 2:
        try:
            cont= 1 if bloquesColumna!= 0 or revisarMismo else 2
            columnaTest= columnaBase+ bloquesColumna
            columnaTest= ('0' if columnaTest < 10 else '')+ str(columnaTest)
            for mov in range(-1,2,cont):
                filaTest= chr(filaBase+ mov)
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
            
        
        
    

def main():
    sala= genMapa()
    
    for i in sala.keys():
        print(i, end= '  ')
        if i[1:3] == '32':
            print('')
    print('\n')

    colores = {0: "⬜", 1: "⬛", 2: "👨",
           3: "🟩", 4: "🟨", 5: "🟥"}
    for i in sala.keys():
        print(colores[sala[i]], end= '')
        if i[1:3] == '32':
            print()
    pass

if __name__ == "__main__":
    main()