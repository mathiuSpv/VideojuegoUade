from funcionesMovimiento import *
from funcionesTrivia import *
from funcionesInterfaz import *
from funcionesRanking import *
from generarMapa import genMapa,genMapaJugador,reconocerEntorno
import os
import time

VIDAS_INICIALES = 3
PUNTOS_INICIALES = 0
TIEMPO_A_DORMIR = 1
BLOQUE_MALO = 5
BLOQUE_BUENO = 4
BLOQUE_FINAL = 3


def main():
    print("Bienvenido a la aventura de los 100 pasos")

    sistemaOperativo = elegirSistema()
    borrarPantalla = lambda : os.system(sistemaOperativo) #noqa
    bancoPreguntas = crearBanco("assets/preguntas.txt")
    personajesMalos = generarPersonajes("assets/personajesMalos.txt")
    personajesBuenos = generarPersonajes("assets/personajesBuenos.txt")
    tesorosObjetivos = generarPersonajes("assets/tesorosObjetivos.txt")
    if respuestaSiNo("Desea cargar una partida guardada?"):
        mapaBase, puntos, vidas,mapaVisible = recuperarPartida(
            "mapaGuardado.txt", "estadisticasGuardadas.txt","mapaJugador.txt")
    else:    
        puntos, vidas, mapaBase,mapaVisible = PUNTOS_INICIALES, VIDAS_INICIALES, genMapa(),genMapaJugador()

    estadoJuego = True
    while estadoJuego:
        try:
            reconocerEntorno(mapaBase, mapaVisible, encontrarJugador(mapaBase))
            imprimirInterfaz(mapaVisible, puntos, vidas)
            bloque = hacerMovimiento(mapaBase)
            if bloque == BLOQUE_MALO:
                """Encuentro con un personaje malo"""
                borrarPantalla()
                puntos, vidas, estadoJuego = encuentroMalo(
                    personajesMalos, bancoPreguntas, puntos, vidas, estadoJuego)
                time.sleep(TIEMPO_A_DORMIR)

                if not estadoJuego:
                    print("Has perdido todas tus vidas.")
                    time.sleep(TIEMPO_A_DORMIR)
                    finalCorrecto = True

            elif bloque == BLOQUE_BUENO:
                """Encuentro con un personaje bueno"""
                borrarPantalla()
                puntos, vidas,mapaVisible= encuentroBueno(
                    personajesBuenos, bancoPreguntas,mapaBase, puntos, vidas,mapaVisible)
                time.sleep(TIEMPO_A_DORMIR)

            elif bloque == BLOQUE_FINAL:
                """Si caes en un tesoro, se termina el nivel"""
                borrarPantalla()
                encuentroFinal(tesorosObjetivos)
                puntos += 100
                print(f"Felicidades has ganado hasta ahora {puntos} puntos")
                if respuestaSiNo("Quieres seguir jugando?: "):
                    mapaNuevo = genMapa()
                    mapaBase = mapaNuevo
                    mapaVisible = genMapaJugador()
                else:
                    estadoJuego = False
                    finalCorrecto = True
            borrarPantalla()


        except KeyboardInterrupt:
            borrarPantalla()
            if respuestaSiNo("Has apretado Control + C, quieres salir?"):
                estadoJuego = False
                finalCorrecto = False
                if respuestaSiNo("Quieres sobreescribir el juego guardado?"):
                    guardarValores(puntos, vidas, mapaBase,"mapaGuardado.txt","estadisticasGuardadas.txt",mapaVisible,"mapaJugador.txt")
                    print("Juego guardado")
                    time.sleep(TIEMPO_A_DORMIR)
            else:
                continue

    if finalCorrecto:
        """Si el juego termina correctamente, se guarda el puntaje"""
        print("El juego ha finalizado")
        nombreJugador = input("Ingresa tu nombre: ")
        with open("ranking.txt", "a") as f:
            f.write(f"{nombreJugador};{puntos}\n")
        if respuestaSiNo("Quieres ver el ranking?"):
            leerRanking("ranking.txt")
        print("Gracias por jugar.")


if __name__ == "__main__":
    main()