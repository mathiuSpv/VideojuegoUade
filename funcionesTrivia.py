import random

BLOQUE_MALO_REVELADO = 6
BLOQUE_FINAL = 3


def sacarMas(lista_lineas: list) -> list:
    """Recibe una lista de lineas y devuelve una lista con los indices de las lineas que contienen un +."""
    mases = []
    for lugar, i in enumerate(lista_lineas):
        if i == "+\n":
            mases.append(lugar)
    return mases


def encontrarBloque(mapa: dict, BLOQUE: int):
    """Esta funcion se encarga de encontrar la posicion del jugador"""
    listaLlaves = list(mapa.keys())
    listaEncontrados = [llave for llave in listaLlaves if mapa[llave] == BLOQUE]
    random.shuffle(listaEncontrados)
    return listaEncontrados[0]

def generarPersonajes(ruta: str) -> dict:
    """Recibe una ruta de archivo y devuelve un diccionario con los personajes."""
    try:
        with open(ruta, "r") as archivo:
            lineas = archivo.readlines()
            personajes = {}
            mases = sacarMas(lineas)
            for lugar, i in enumerate(mases):
                if lugar == len(mases) - 1:
                    personajes[lineas[i +
                                      1].rstrip("\n")] = "".join(lineas[i+2:])
                else:
                    personajes[lineas[i+1].rstrip("\n")
                               ] = "".join(lineas[i+2:mases[lugar+1]])
            return personajes
    except FileNotFoundError:
        print("No se encontro el archivo, el juego puede no funcionar correctamente.")


def crearBanco(ruta: str) -> list:
    """Recibe una ruta de archivo y devuelve una lista con las preguntas del archivo de texto."""
    try:
        with open(ruta, "r") as archivo:
            lineas = archivo.readlines()
            preguntas = []
            letras = ["a", "b", "c", "d"]
            for linea in lineas:
                preguntaActual = {}
                linea_actual = linea.split(";")
                preguntaActual["pregunta"] = linea_actual[0]
                preguntaActual["respuestas"] = dict(
                    zip(letras, linea_actual[1:5]))
                preguntaActual["correcta"] = linea_actual[5].rstrip()
                preguntas.append(preguntaActual)
            return preguntas
    except FileNotFoundError:
        print("No se encontro el archivo, el juego puede no funcionar correctamente.")


def hacerPregunta(banco_preguntas: list) -> tuple:
    """Recibe un diccionario con las preguntas, hace una pregunta, pide la respuesta del usuario y retorna una tupla si la respuesta del usuario es correcta junto con la pregunta para su posterior eliminacion."""
    preguntaActual = random.choice(banco_preguntas)
    print(preguntaActual["pregunta"])
    respuestas = preguntaActual["respuestas"]
    for key, value in respuestas.items():
        print(f"{key}) {value.rstrip()}")
    respuestaUsuario = input("Ingrese una letra: ")
    while respuestaUsuario not in list(respuestas.keys()):
        respuestaUsuario = input("Ingrese una letra valida: ")
    return (respuestaUsuario.lower() == preguntaActual["correcta"], preguntaActual)


def aparicionMalo(arteMalvados: dict, bancoPreguntas: list) -> bool:
    """Recibe un diccionario con los personajes malvados y un diccionario con las preguntas, hace una pregunta, pide la respuesta del usuario y retorna una tupla si la respuesta del usuario es correcta junto con la pregunta para su posterior eliminacion."""
    try:
        print(arteMalvados[random.choice(list(arteMalvados.keys()))])
        print(
            "Has caido en mi trampa aventurero, responde mi pregunta si quieres vivir.🐱‍🐉")
        retornos = hacerPregunta(bancoPreguntas)
        bancoPreguntas.remove(retornos[1])
        return retornos[0]
    except AttributeError:
        print("No se cargaron personajes o hubo un error en el archivo.")


def aparicionBueno(arteBuenos: dict, bancoPreguntas: list) -> bool:
    """Recibe un diccionario con los personajes buenos y un diccionario con las preguntas, hace una pregunta, pide la respuesta del usuario y retorna una tupla si la respuesta del usuario es correcta junto con la pregunta para su posterior eliminacion."""
    try:
        print(arteBuenos[random.choice(list(arteBuenos.keys()))])
        print("Oh un aventurero, responde mi pregunta si quieres ganar una recompensa.😉")
        retornos = hacerPregunta(bancoPreguntas)
        bancoPreguntas.remove(retornos[1])
        return retornos[0]
    except AttributeError:
        print("No se cargaron personajes o hubo un error en el archivo.")


def encuentroMalo(personajesMalos: dict, bancoPreguntas: list,puntos: int,vidas:int,estadoJuego):
    if aparicionMalo(personajesMalos, bancoPreguntas):
        print("Tu respuesta es correcta ganas 20 puntos.")
        puntos += 20
    else:
        print("Respuesta incorrecta pierdes una vida")
        vidas -= 1
        if vidas == 0:
            estadoJuego = False
    return (puntos,vidas,estadoJuego)

def encuentroBueno(personajesBuenos: dict, bancoPreguntas: list,mapaActual,puntos: int,vidas:int,mapaJugador: dict):
    if aparicionBueno(personajesBuenos, bancoPreguntas):
        print("Tu respuesta es correcta ganas un comodin.")
        vidas,puntos,mapaJugador = unComodin(vidas,puntos,mapaJugador,mapaActual)
    else:
        print("Respuesta incorrecta, no ganas nada.")
    return puntos,vidas,mapaJugador


def unComodin(vidas: int, puntos: int, mapaVisible: dict, mapaBase) -> tuple:
    """Recibe las vidas y los puntos del jugador y devuelve las vidas y los puntos del jugador con un comodin."""
    try:
        elegirComodin = True
        while elegirComodin:
            chance = random.randint(1, 12)
            if 1 <= chance <= 1:
                puntos += 30
                print("Has ganado 30 puntos")
                elegirComodin = False
            elif 2 <= chance <= 5:
                enemigo = encontrarBloque(mapaBase, 5)
                if mapaVisible[enemigo] == BLOQUE_MALO_REVELADO:
                    pass
                else:
                    mapaVisible[enemigo] = BLOQUE_MALO_REVELADO
                    mapaBase[enemigo] = BLOQUE_MALO_REVELADO
                    print("Muestra la posicion de un malvado")
                    elegirComodin = False
            elif 6 <= chance <= 9:
                print("Has ganado 80 puntos")
                puntos += 80
                elegirComodin = False
            elif 10 <= chance <= 11 and (BLOQUE_FINAL not in list(mapaVisible.values())):
                salida = encontrarBloque(mapaBase, BLOQUE_FINAL)
                mapaVisible[salida] = BLOQUE_FINAL
                print("Muestra la posicion de la salida")
                elegirComodin = False
            elif chance == 12:
                vidas += 1
                print("Has ganado una vida")
                elegirComodin = False
            else:
                continue
            return vidas, puntos, mapaVisible

    except IndexError:
        print("Ya no quedan mas enemigos por revelar")

def encuentroFinal(tesoros: dict):
    print(tesoros[random.choice(list(tesoros.keys()))])


def main():
    bancoPreguntas = crearBanco("assets/preguntas.txt")
    print(hacerPregunta(bancoPreguntas))


if __name__ == "__main__":
    main()
