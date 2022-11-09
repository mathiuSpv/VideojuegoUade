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
        print(lineas)
        preguntas = []
        letras = ["a","b","c","d"]
        for linea in lineas:
            preguntaActual = {}
            linea_actual = linea.split(";")
            preguntaActual["pregunta"] = linea_actual[0]
            preguntaActual["respuestas"] = dict(zip(letras,linea_actual[1:5]))
            preguntaActual["correcta"] = linea_actual[5]
            preguntas.append(preguntaActual)
        return preguntas
            

            


def hacerPregunta(banco_preguntas: list):
    preguntaActual = random.choice(banco_preguntas)
    print(preguntaActual["pregunta"])
    respuestas = preguntaActual["respuestas"]
    for key, value in respuestas.items():
        print(f"{key}){value.rstrip()}")
    respuestaUsuario = input("Ingrese una letra: ")
    while respuestaUsuario not in list(respuestas.keys()):
        respuestaUsuario = input("Ingrese una letra valida: ")
    return (respuestaUsuario.lower() == preguntaActual["correcta"], preguntaActual)


def encuentroMalo(arteMalvados:dict,bancoPreguntas:list):
    print(arteMalvados[random.choice(list(arteMalvados.keys()))])
    print("Has caido en mi trampa aventurero, responde mi pregunta si quieres vivir.🐱‍🐉")
    retornos = hacerPregunta(bancoPreguntas)
    bancoPreguntas.remove(retornos[1])
    return retornos[0]

def encuentroBueno(arteBuenos:dict,bancoPreguntas:list):
    print(arteBuenos[random.choice(list(arteBuenos.keys()))])
    print("Oh un aventurero, responde mi pregunta si quieres ganar una recompensa.😉")

def main():
    bancoPreguntas = crearBanco("assets/preguntas.txt")
    print(len(bancoPreguntas))
    personajesMalos = generarPersonajes("assets/personajesMalos.txt")
    encuentroMalo(personajesMalos,bancoPreguntas)
    print(len(bancoPreguntas))



main()