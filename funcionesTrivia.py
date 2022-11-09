import random


def sacarMas(lista_lineas: list):
    mases = []
    for lugar, i in enumerate(lista_lineas):
        if i == "+\n":
            mases.append(lugar)
    return mases


def generarPersonajes(ruta=r"assets/personajes.txt"):
    with open(ruta, "r") as archivo:
        lineas = archivo.readlines()
        personajes = {}
        mases = sacarMas(lineas)
        for lugar, i in enumerate(mases):
            if lugar == len(mases) - 1:
                personajes[lineas[i+1].rstrip("\n")] = "".join(lineas[i+2:])
            else:
                personajes[lineas[i+1].rstrip("\n")
                           ] = "".join(lineas[i+2:mases[lugar+1]])
        return personajes


def crearBanco(ruta="assets/ideas.txt"):
    with open(ruta, "r") as archivo:
        lineas = archivo.readlines()
        mases = sacarMas(lineas)
        bancoPreguntas = []
        for i in mases:
            preguntaActual = {}
            preguntaActual["pregunta"] = lineas[i+1].rstrip()
            letras = ["a", "b", "c", "d"]
            preguntaActual["respuestas"] = dict(zip(letras, lineas[i+2:i+6]))
            preguntaActual["correcta"] = lineas[i+6].rstrip()
            bancoPreguntas.append(preguntaActual)
        return bancoPreguntas


def hacerPregunta(banco_preguntas: list):
    preguntaActual = random.choice(banco_preguntas)
    print(preguntaActual["pregunta"])
    respuestas = preguntaActual["respuestas"]
    for key, value in respuestas.items():
        print(f"{key}){value.rstrip()}")
    respuestaUsuario = input("Ingrese una letra: ")
    return respuestaUsuario.lower() == preguntaActual["correcta"]
