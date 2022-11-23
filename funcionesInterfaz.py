from generarMapa import imprimirMapa
import random

def imprimirVidas(vidas): return print("Vidas: " + "❤ " * vidas)
def imprimirPuntos(puntos): return print("Puntos: " + str(puntos))


def imprimirMapa(mapa: dict):
    colores = {-1: "  ", 0: "⬜", 1: "⬛", 2: "👨",
               3: "🟩", 4: "🟨", 5: "⬛", 6: "🟥"}
    for i in mapa.keys():
        print(colores[mapa[i]], end='')
        if i[1:3] == '32':
            print()

def imprimirInterfaz(mapaActual: list, puntos: int, vidas: int):
    """Imprime el mapa, las vidas y los puntos"""
    imprimirMapa(mapaActual)
    imprimirVidas(vidas)
    imprimirPuntos(puntos)


def respuestaSiNo(pregunta):
    """Pregunta al usuario si o no y devuelve True o False"""
    respuesta = input(pregunta + " (s/n): ")
    while respuesta.lower() not in ["s", "n"]:
        respuesta = input("Ingrese una opcion valida: ")
    return respuesta == "s"


def guardarMapa(diccionario, archivo):
    """Guarda el mapa en un archivo"""
    with open(archivo, "w") as f:
        for key, value in diccionario.items():
            f.write(f"{key}={value}\n")


def abrirMapa(archivo):
    """Abre un archivo y devuelve un diccionario que representa un mapa"""
    diccionario = {}
    with open(archivo, "r") as f:
        for linea in f.readlines():
            key, value = linea.rstrip().split("=")
            diccionario[key] = int(value)
    return diccionario


def guardarValores(puntos, vidas,mapaActual,archivoMapa, archivoPuntosVidas,mapaJugador,archivoMapaJugador):
    """Guarda los valores de puntos, vidas y el mapa en un archivo"""
    diccionario = {"puntos": puntos, "vidas": vidas}
    guardarMapa(mapaActual, archivoMapa)
    guardarMapa(diccionario, archivoPuntosVidas)
    guardarMapa(mapaJugador, archivoMapaJugador)


def recuperarPartida(archivoMapa, archivoPuntosVidas,archivoMapaJugador):
    """Recupera los valores de puntos, vidas y el mapa de un archivo"""
    mapaActual = abrirMapa(archivoMapa)
    estadisticas = abrirMapa(archivoPuntosVidas)
    puntos = int(estadisticas["puntos"])
    vidas = int(estadisticas["vidas"])
    mapaJugador = abrirMapa(archivoMapaJugador)
    return mapaActual, puntos, vidas,mapaJugador


def elegirSistema():
    """Pregunta al usuario si quiere jugar con Windows o Linux"""
    opcion = input(
        "Ingrese su sistema operativo (A para Windows o B para Linux): ")
    while opcion.lower() not in ["a", "b"]:
        opcion = input("Ingrese una opcion valida: ")
    if opcion.lower() == "a":
        return "cls"
    else:
        return "clear"


def jugarNivelSiguiente():
    """Pregunta al usuario si quiere jugar el nivel siguiente"""
    print("Quieres jugar al siguiente nivel? (s/n)")
    respuesta = input()
    while respuesta.lower() not in ["s", "n"]:
        print("Quieres jugar al nivel siguiente? (s/n)")
        respuesta = input()
    return respuesta == "s"
