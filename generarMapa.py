import random


DIFICULTAD= 1.2 #GENERAR ALGUN VALOR PARA AUMENTAR ESTO O QUE AUMENTE 0.3 CADA DIF

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
############################

def genMapa(filas= 18, columnas= 32):
    """Funcion que permite crear la room del juego, usa un diccionario como un mapa y su Key es 'Key[0:1]' su fila y 'Key[1:3]' su columna respectiva"""
    filas= (filas if filas==22 else 18) + 65
    columnas= (columnas if columnas==28 else 32)
    SALA= dict()
    BLOQUESVACIOS= set()
    _crearSala(SALA, filas, columnas)
    _generadores(SALA, BLOQUESVACIOS, filas, columnas)
    return SALA    

def _crearSala(sala: dict, filas: int, columnas: int):
    numId= 1; letraId= 65
    while letraId <= filas:
        ID= chr(letraId)+(str(numId) if numId>9 else f"0{numId}")
        sala[ID]= 0
        numId+=1
        if numId > columnas:
            letraId+=1; numId= 1

def _generadores(sala: dict, bloquesVacios: set, filas: int, columnas: int):
    bloquesCerrados= set()
    bloquesInflexion= _initBloque()
    _definirContorno(bloquesCerrados, filas, columnas)
    _genEntradas(sala, bloquesInflexion, filas, columnas)
    
    bloqueEntrada= _datoBloque(bloquesInflexion) # EN _genEntradas() UTLIZAMOS ESTA LISTA PARA EXTRAER COMO PRIMER DATO LA ENTRADA DE LA SALA
    
    _genPuntosInflexion(bloquesInflexion, bloqueEntrada, filas, columnas)
    _genRandom(bloquesVacios, bloqueEntrada, bloquesInflexion)
    
    for cord in bloquesVacios:
        sala[cord]= 1
    eventos= set()
    for i in range(9):
        i= random.choice(list(bloquesVacios))
        while i in eventos:
            i= random.choice(list(bloquesVacios))
        eventos.add(i)
        sala[i]= random.randint(4,5)

def _definirContorno(bloquesCerrados: set, filas: int, columnas: int):
    numId= 1; letraId= 65
    while letraId <= filas:
        bloquesCerrados.add(chr(letraId)+'01')
        bloquesCerrados.add(chr(letraId)+f'{columnas}')
        letraId+= 1
    while numId <= columnas:
        bloquesCerrados.add('A'+(str(numId) if numId>9 else f'0{numId}'))
        bloquesCerrados.add(chr(filas)+(str(numId) if numId>9 else f'0{numId}'))
        numId+= 1

def _genEntradas(sala: dict, puntosInflexion: list, filas: int, columnas: int):
    VACIO= 1; ENTRADAVALUE= 2; SALIDAVALUE= 3
    entradaFila= chr(random.randint(66,filas-1)) #EMPEZAR DE B COMO ACCSI HASTA LA PENULTIMA LETRA COMO ACCSI
    salidaFila= chr(random.randint(66,filas-1))
    entradaId= entradaFila+'01'
    primerSlotEntrada= entradaFila+'02'
    salidaId= salidaFila+f"{columnas}"
    primerSlotSalida= salidaFila+f"{columnas-1}"
    sala[entradaId]= ENTRADAVALUE; sala[primerSlotEntrada]= VACIO
    sala[salidaId]= SALIDAVALUE; sala[primerSlotSalida]= VACIO
    _agregarBloque(puntosInflexion, primerSlotSalida)
    _agregarBloque(puntosInflexion, primerSlotEntrada)
    
def _genPuntosInflexion(puntosInflexion: list, entrada: str, filas: int, columnas: int):
    cantMax= random.randint(12,14) #SE PUEDE MODIFICAR Y PODER AUMENTAR RESPECTO A LA DIFICULTAD
    cuadrante= 1
    vecesHecho= 1
    while vecesHecho < cantMax:
        seleccion= _genPunto(filas, columnas, cuadrante)
        while seleccion in puntosInflexion:
            seleccion= _genPunto(filas, columnas, cuadrante)
        _agregarBloque(puntosInflexion, seleccion)
        vecesHecho+= 1
        if vecesHecho == cantMax//2:
            cuadrante= 0
    print(puntosInflexion)

def _genPunto(filas, columnas, cuadrante):
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
    


def main():
    sala= genMapa()
    
    
    for i in sala.keys():
        print(i, end= '  ')
        if i[1:3] == '32':
            print('')
    print('\n')
    
    colores = {0: "⬛", 1: "⬜", 2: "👨",
           3: "🟥", 4: "🟩", 5: "🟨"}
    for i in sala.keys():
        print(colores[sala[i]], end= '')
        if i[1:3] == '32':
            print()
    pass

if __name__ == "__main__":
    main()