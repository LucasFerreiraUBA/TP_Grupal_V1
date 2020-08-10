def extraer_nombres(archivo):
    """[Autor: Javier Acho]
       [Ayuda: Devuelve una secuencia de dos elementos, el primero es una secuencia
        que contiene los nombres de función que se encuentran en el primer campo
        y el segundo elemento es una secuencia con los nombres de autor del ultimo
        campo en el archivo csv que recibe.]
    """

    nombres_funciones = []
    nombres_autores = []

    for registro in archivo:

        linea = registro.rstrip("\n")
        nom_funcion, resto = linea.split(",", 1)
        nombres_funciones.append(nom_funcion)

        resto, nom_autor = resto.rsplit(",", 1)
        nombres_autores.append(nom_autor)

    archivo.seek(0)   # vuelvo el cursor o puntero al inicio del archivo

    return nombres_funciones, nombres_autores

def buscar_longitudes_max(arch_info):
    """[Autor: Javier Acho]
       [Ayuda: Devuelve una secuencia de dos números enteros, que corresponden
        a las longitudes máximas de las cadenas que se encuentran en el primer
        y último campo de cada registro del archivo csv que recibe.]
    """

    nom_funciones, nom_autores = extraer_nombres(arch_info)
    long_max_funcion = max(map(len, nom_funciones))
    long_max_autor = max(map(len, nom_autores))
    return long_max_funcion, long_max_autor

def mostrar_tabla_funciones(arch_datos_funciones):
    """[Autor: Javier Acho]
       [Ayuda: Muestra por pantalla una tabla con información de cada función
        que se encuentra dentro del archivo csv. El archivo debe estar abierto
        en modo lectura.]
    """

    long_max_funcion, long_max_autor = buscar_longitudes_max(arch_datos_funciones)
    for linea in arch_datos_funciones:
        c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13 = \
        linea.rstrip("\n").split(",")

        c1 = c1.ljust(long_max_funcion)
        c13 = c13.ljust(long_max_autor)
        cadena = c1 + " | {0:^10s} | {1:^6s} | {2:^12s}".format(c2, c3, c4) +\
                 " | {0:^7s} | {1:^7s} | {2:^3s} | {3:^5s}".format(c5, c6, c7, c8) +\
                 " | {0:^5s} | {1:^4s} | {2:^6s} | {3:^5}".format(c9, c10, c11, c12) +\
                 " | " + c13

        print(cadena)
        print("-" * len(cadena))
