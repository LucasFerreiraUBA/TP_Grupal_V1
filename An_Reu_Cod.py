import os

def generador_de_lista_de_funciones():
    """
    [Autor: Lucas M. Diana]
    [Ayuda: Genera una lista con todas las funciones que existen
            dentro de fuente_unico.csv]
    """
    fuente_unico =  open('fuente_unico.csv','r')
    listaOG = []
    renglon = fuente_unico.readline().split(",")
    while renglon != None:
        funcion = renglon[0]
        if funcion != '':
            listaOG.append(funcion)
            renglon = fuente_unico.readline().split(",")
        else:
            renglon = None
    fuente_unico.close()
    del renglon, funcion
    listaOG = chequeo(listaOG)
    return listaOG

def chequeo(listaOG):
    """
    [Autor: Lucas M. Diana]
    [Ayuda: Se fija que no haya repetidas]
    """
    posicion = 0
    for funcion in listaOG:
        if listaOG[posicion] == listaOG[posicion - 1] and posicion > 0:
            listaOG.pop(posicion)
        if posicion < len(listaOG):
            posicion += 1
    return listaOG

def generador_de_listas_de_llamadas(listaOG):
    """
    [Autor: Lucas M. Diana]
    [Requisitos: listaOG - una lista que contenga el nombre
                           de todas las funciones.]
    [Ayuda: Genera una lista para cada funcion con todas las llamadas
            que existen dentro. Estas se incorporan a una lista de listas.]
    """
    fuente_unico =  open('fuente_unico.csv','r')
    listaLL = []
    renglon = fuente_unico.readline().split(",")
    while renglon != None:
        funcion = renglon[0]
        if funcion != '':
            sublistaLL = procesar_listaFP(renglon, listaOG)
            listaLL.append(sublistaLL)
            renglon = fuente_unico.readline().split(",")
        else:
            del funcion
            renglon = None
    fuente_unico.close()
    del renglon, sublistaLL
    return listaLL

def procesar_listaFP(lfp, listaOG):
    """
    [Autor: Lucas M. Diana]
    [Requisitos: listaOG - una lista que contenga el nombre
                           de todas las funciones.
                 lfp - una lista/tupla que contenga cada linea de una funcion
                       en cada campo.]
    [Ayuda: Filtra la lista con cada linea de codigo de una funcion
            y devuelve una lista que contiene solo las llamadas de la funcion]
    """
    sublistaLL = []
    for linea in lfp:
        llamada = None
        paren = None
        if linea is not lfp[0]:
            try:
                paren = linea.find('(')
                if '= ' in linea:
                    igual = linea.find('= ') + 2
                elif '=' in linea:
                    igual = linea.find('=') + 1
                else:
                    igual = 0
                llamada = linea[igual:paren]
            except:
                None
        if llamada in listaOG:
            sublistaLL.append(llamada)
    if paren != None:
        del paren, igual, llamada, linea
    else:
        del llamada, linea, paren
    return sublistaLL

def contador_de_invocaciones(listaOG, listaLL): 
    """
    [Autor: Lucas M. Diana]
    [Requisitos: listaOG - una lista que contenga el nombre
                           de todas las funciones.
                 listaLL - una lista de listas de llamadas.]
    [Ayuda: Genera un diccionario cuyas claves son las funciones del programa
            y el contenido de cada llave es una lista con la cantidad de
            llamadas realizadas por la funcion clave (cada campo refiere
            a una funcion).]
    """
    dixTOT = {}
    posLL = 0
    for funcion in listaOG:
        dixTOT[funcion] = []     
        posSub = 0
        sublis = []
        for funcion2 in listaOG:
            sublis.append(0)          
            for call in listaLL[posLL]:
                if funcion2 == call:                    
                    sublis[posSub] += 1
            posSub += 1
        posLL += 1        
        dixTOT[funcion] = sublis
    del posLL, funcion, posSub, sublis, funcion2, call
    return dixTOT

def contador_de_llamadas(dixTOT): 
    """
    [Autor: Lucas M. Diana]
    [Requisitos: listaOG - una lista que contenga el nombre
                           de todas las funciones.
                 dixTOT - un diccionario con la cantidad de referencias
                          que realiza cada funcion.]
    [Ayuda: Genera un diccionario cuyas claves son las funciones del programa
            y el contenido de cada llave es una lista con (O)s y (X)s,
            siendo las X cuando la funcion clave recive una llamada
            (cada campo refiere a una funcion).]
    """
    dixRec = {}
    posicionFuncion = 0
    for funcion in dixTOT:
        sublistaDeLlamadas = []
        for key in dixTOT:
            if dixTOT[key][posicionFuncion] > 0:
                sublistaDeLlamadas.append('X')
            else:
                sublistaDeLlamadas.append('O')
        posicionFuncion += 1
        dixRec[funcion] = sublistaDeLlamadas
    return dixRec

def txt_maker(listaOG, dixTOT, dixRec):
    """
    [Autor: Lucas M. Diana]
    [Requisitos: listaOG - una lista que contenga el nombre
                           de todas las funciones.
                 dixTOT - un diccionario con la cantidad de referencias
                          que realiza cada funcion.
                 dixRec - un diccionario con llamadas realizadas a cada funcion.]
    [Ayuda: Genera el archivo "analizador.txt" en el directorio actual,
            cuyos contenidos son los elementos de dixTOT y dixRec formateados
            para mas facil interpretacion por parte del usuario.
            Genera una fila y una columna para cada funcion, y muestra:
              - la cantidad de veces que la funcion llama a otra en su fila;
              - si recive una llamada en su columna (marcado con una X);
              - Deja un campo vacio en caso de no hacer ni recivir una llamada.]
    """
    linea = ''
    tab = 0
    longitud = 0
    for funcion in listaOG:
        if len(funcion) > longitud:
            longitud = len(funcion)
        tab += 1
    tab = len(str(tab))
    if len('Funcion/es') > longitud:
        longitud = len('Funcion/es')
    if len('Total de Invocaciones') > longitud:
        longitud = len('Total de Invocaciones')
    longitud += 1
    linea += ('|{0:{1}} {2:{3}}').format(' ', tab + 1,'Funcion/es', longitud)
    contador_columnas = 0
    for funcion in listaOG:
        linea += ('| {} ').format(contador_columnas)
        contador_columnas += 1
    del contador_columnas
    linea += ('|\n')
    separador = ''
    for char in linea:
        separador += ('-')
    del char
    separador += ('\n')
    analiz = open("{}\\analizador.txt".format(os.getcwd()), 'w+')
    analiz.write(separador)
    analiz.write(linea)
    escritor(analiz, listaOG, separador, tab, longitud, dixTOT, dixRec)
    linea = ''
    linea += ('|{0:{1}} {2:{3}}').format(' ', tab + 1,'Total de Invocaciones', longitud)
    contador = 0
    for funcion in listaOG:
        suma_tot = suma_inv(dixTOT, contador)
        linea += ('| {0:{1}} ').format(suma_tot, len(str(contador)))
        contador += 1
    linea += ('|\n')
    analiz.write(linea)
    analiz.write(separador)
    analiz.close()
    del linea, contador, longitud, tab, analiz

def escritor(analiz, listaOG, separador, tab, longitud, dixTOT, dixRec):
    """
    [Autor: Lucas M. Diana]
    [Ayuda: Para anotar en el txt]
    """
    n_funcion = 0
    for funcion in listaOG:
        analiz.write(separador)
        linea = ''
        linea += ('|{0:{1}}) {2:{3}}').format(n_funcion, tab, funcion, longitud)
        n_funcion += 1
        contador = 0
        for funcion2 in listaOG:
            if dixTOT[funcion][contador] > 0 and dixRec[funcion][contador] == 'X':
                linea += ('|{0:{1}}').format('{0}/{1}'.format(dixTOT[funcion][contador], dixRec[funcion][contador]), len(str(contador)))
            elif dixTOT[funcion][contador] > 0:
                linea += ('| {0:{1}} ').format(dixTOT[funcion][contador], len(str(contador)))
            elif dixRec[funcion][contador] == 'X':
                linea += ('| {0:{1}} ').format(dixRec[funcion][contador], len(str(contador)))
            else:
                linea += ('| {0:{1}} ').format('', len(str(contador)))
            contador += 1
        linea += ('|\n')
        analiz.write(linea)
    analiz.write(separador)
    del funcion, funcion2, contador, n_funcion
    return

def suma_inv(dixTOT, contador):
    """
    [Autor: Lucas M. Diana]
    [Requisitos: dixTOT - un diccionario con la cantidad de referencias
                          que realiza cada funcion.
                 contador - un contador usado para determinar
                            la funcion que se evalua.]
    [Ayuda: suma el total de llamadas recividas por una funcion.]
    """
    suma_total = 0
    for funcion in dixTOT:
        suma_total += dixTOT[funcion][contador]
    return suma_total

def reutilizacion_de_codigo():
    """
    [Autor: Lucas M. Diana]
    [Requisitos: Ninguno!]
    [Ayuda: Imprime los contenidos del archivo "analizador.txt" en la pantalla.
            En caso de no existir, crea el archivo txt y luego lo imprime.]
    """
    if os.path.isfile("{}\\analizador.txt".format(os.getcwd())):
        print('\analizador.txt existe, leyendo...\n')
        print()
        analizador = open("{}\\analizador.txt".format(os.getcwd()), 'r')
    else:
        print('\analizador.txt no existe, creando...\n')
        listaOG = generador_de_lista_de_funciones()
        listaLL = generador_de_listas_de_llamadas(listaOG)
        dixTOT = contador_de_invocaciones(listaOG, listaLL)
        dixRec = contador_de_llamadas(dixTOT)
        txt_maker(listaOG, dixTOT, dixRec)
        del listaOG, listaLL, dixRec, dixTOT
        print('analizador.txt creado, leyendo...\n')
        print()
        analizador = open("{}\\analizador.txt".format(os.getcwd()), 'r')
    print(analizador.read())
    analizador.close()
    input('Pulse ENTER para finalizar.')
