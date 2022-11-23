def ingresarUsuarios(puntaje):
    try:
        archivo = open("usuarios.txt", mode = "r")
    except IOError:
        print("no se puede crear el archivo")
    else:
        nombre = input("ingrese su nombre de usuario: ").lower()
        archivo = open("usuarios.txt", mode = "a")
        archivo.write(nombre + ";" + str(puntaje)+"\n")
        archivo.close()
ingresarUsuarios()
