def imprimirDos(lista):
    return f"{lista[0]} -> {lista[1]}"


def leerRanking(ruta):
    try:
        """Abre el archivo de texto donde se encuentran los nombres y puntajes de los jugadores y lo ordena de manera descendiente según el puntaje"""
        archivo = open(ruta, mode="r")
        lista = []
        for a in archivo.readlines():
            lineaActual = (a.rstrip()).split(";")
            lineaActual[1] = int(lineaActual[1])
            lista.append(lineaActual)

        miniFun = lambda lista1: lista1[1]
        lista.sort(key=miniFun, reverse=True)

        print("Ranking top jugadores")
        posicion = 0
        for i in range(0, 5):
            if posicion <= len(lista)-1:
                print(f"Puesto numero {i+1}: {imprimirDos(lista[i])}")
        posicion += 1
    except FileNotFoundError:
        """En caso de que no se pueda abrir el archivo o halla error en el ranking"""
        print("No se encontro el archivo, el juego puede no funcionar correctamente.")
    except IndexError:
        print("Hubo un error en el ranking, puede no funcionar correctamente.")



def main():
    leerRanking(r"assets\ranking.txt")


if __name__ == "__main__":
    main()