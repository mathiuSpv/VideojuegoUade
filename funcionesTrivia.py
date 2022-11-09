import random


def sacarMas(lista_lineas: list) -> list:
    """Recibe una lista de lineas y devuelve una lista con los indices de las lineas que contienen un +."""
    mases = []
    for lugar, i in enumerate(lista_lineas):
        if i == "+\n":
            mases.append(lugar)
    return mases


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
        print("No se encontro el archivo")


def crearBanco(ruta: str) -> list:
    """Recibe una ruta de archivo y devuelve una lista con las preguntas del archivo de texto."""
    try:
        with open(ruta, "r") as archivo:
            lineas = archivo.readlines()
            print(lineas)
            preguntas = []
            letras = ["a", "b", "c", "d"]
            for linea in lineas:
                preguntaActual = {}
                linea_actual = linea.split(";")
                preguntaActual["pregunta"] = linea_actual[0]
                preguntaActual["respuestas"] = dict(
                    zip(letras, linea_actual[1:5]))
                preguntaActual["correcta"] = linea_actual[5]
                preguntas.append(preguntaActual)
            return preguntas
    except FileNotFoundError:
        print("No se encontro el archivo")


def hacerPregunta(banco_preguntas: list) -> tuple:
    """Recibe un diccionario con las preguntas, hace una pregunta, pide la respuesta del usuario y retorna una tupla si la respuesta del usuario es correcta junto con la pregunta para su posterior eliminacion."""
    preguntaActual = random.choice(banco_preguntas)
    print(preguntaActual["pregunta"])
    respuestas = preguntaActual["respuestas"]
    for key, value in respuestas.items():
        print(f"{key}){value.rstrip()}")
    respuestaUsuario = input("Ingrese una letra: ")
    while respuestaUsuario not in list(respuestas.keys()):
        respuestaUsuario = input("Ingrese una letra valida: ")
    return (respuestaUsuario.lower() == preguntaActual["correcta"], preguntaActual)


def encuentroMalo(arteMalvados: dict, bancoPreguntas: list) -> bool:
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


def encuentroBueno(arteBuenos: dict, bancoPreguntas: list) -> bool:
    """Recibe un diccionario con los personajes buenos y un diccionario con las preguntas, hace una pregunta, pide la respuesta del usuario y retorna una tupla si la respuesta del usuario es correcta junto con la pregunta para su posterior eliminacion."""
    try:
        print(arteBuenos[random.choice(list(arteBuenos.keys()))])
        print("Oh un aventurero, responde mi pregunta si quieres ganar una recompensa.😉")
        retornos = hacerPregunta(bancoPreguntas)
        bancoPreguntas.remove(retornos[1])
        return retornos[0]
    except AttributeError:
        print("No se cargaron personajes o hubo un error en el archivo.")


def main():
    bancoPreguntas = crearBanco("assets/preguntas.txt")
    personajesMalos = generarPersonajes("")
    personajesBuenos = generarPersonajes("assets/personajesBuenos.txt")
    tesorosObjetivos = generarPersonajes("assets/tesorosObjetivos.txt")
    encuentroMalo(personajesMalos, bancoPreguntas)
    encuentroBueno(personajesBuenos, bancoPreguntas)
    print(tesorosObjetivos["tesoro"])


main()
