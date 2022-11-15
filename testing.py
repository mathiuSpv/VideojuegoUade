import random
def encontrarBloque(mapa: dict, BLOQUE: int):
    """Esta funcion se encarga de encontrar la posicion del jugador"""
    listaLlaves = list(mapa.keys())
    listaEncontrados = [
        llave for llave in listaLlaves if mapa[llave] == BLOQUE]
    random.shuffle(listaEncontrados)
    return listaEncontrados[0]

def abrirMapa(archivo):
    """Abre un archivo y devuelve un diccionario que representa un mapa"""
    diccionario = {}
    with open(archivo, "r") as f:
        for linea in f.readlines():
            key, value = linea.rstrip().split("=")
            diccionario[key] = int(value)
    return diccionario



mapa = abrirMapa("mapaGuardado.txt")

print(encontrarBloque(mapa,4))