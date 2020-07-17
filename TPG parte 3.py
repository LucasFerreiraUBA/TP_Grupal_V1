import os, time

def contador_de_invocaciones(listaOG, listaLL): 
    """
    [Autor: Lucas M. Diana]
    Genera un diccionario con la cantidad de referencias
    que realiza cada funcion.

    """

    dixTOT = {}
    posLL = 0
    for funcion in listaOG:
        dixTOT[funcion] = []     
        posSub = 0
        sublis = []
        for funcion2 in listaOG:
            sublis.append(0)      
            sublis[posSub] = 0            
            for call in listaLL[posLL]:
                if funcion2 == call:                    
                    sublis[posSub] += 1
            posSub += 1
        posLL += 1        
        dixTOT[funcion] = sublis
    del posLL, funcion, posSub, sublis, funcion2, call
    return dixTOT

def contador_de_llamadas(listaOG, dixTOT): 
    """
    [Autor: Lucas M. Diana]
    Genera un diccionario que marca donde es referenciada
    cada funcion.
    
    """
    
    dixRec = {}
    pos = 0
    for recive in listaOG:
        listaRec = []
        for envia in dixTOT:
            if dixTOT[envia][pos] > 0:
                listaRec.append('X')
            else:
                listaRec.append('O')
        dixRec[recive] = listaRec
        pos += 1
    del pos, recive, listaRec, envia
    return dixRec


def generador_de_lista_de_funciones():
    """
    [Autor: Lucas M. Diana]
    Genera una lista con todas las funciones que existen
    dentro de fuente_unico.csv
    
    """
    
    fuente_unico =  open('fuente_unico.csv','r')
    lista_de_funciones_parcial = []
    listaOG = []
    for valor in fuente_unico:
        if valor.startswith("def "):
            lista_de_funciones_parcial.append(valor.replace('def ',''))
    for proto_funcion in lista_de_funciones_parcial:
        paren = proto_funcion.find('(')
        funcion = proto_funcion[:paren]
        listaOG.append(funcion)
    fuente_unico.close()
    del lista_de_funciones_parcial, valor, proto_funcion, paren, funcion
    return listaOG

def generador_de_listas_de_llamadas():
    """
    [Autor: Lucas M. Diana]
    Genera una lista para cada funcion con todas las llamadas
    que existen dentro. Estas se incorporan a una lista de listas.
    
    """
    
    fuente_unico =  open('fuente_unico.csv','r')
    lista_de_funciones_parcial = []
    listaLL = []
    for valor in fuente_unico:
        if valor.startswith("def ") and lista_de_funciones_parcial != []:
            sublistaLL = procesar_listaFP(lista_de_funciones_parcial)
            listaLL.append(sublistaLL)
            lista_de_funciones_parcial = []
            lista_de_funciones_parcial.append(valor)
        elif valor is None:
            sublistaLL = procesar_listaFP(lista_de_funciones_parcial)
            listaLL.append(sublistaLL)
        else:
            lista_de_funciones_parcial.append(valor)
    fuente_unico.close()
    del lista_de_funciones_parcial, valor, sublistaLL
    return listaLL

def procesar_listaFP(lfp):
    """
    [Autor: Lucas M. Diana]
    Filtra la lista con cada linea de codigo de una funcion
    y devuelve una lista que contiene solo las llamadas de la funcion
    
    """
    
    sublistaLL = []
    for funcionLocal in lfp:
        llamada = None
        if funcionLocal.endswith(')'):
            paren = funcionLocal.find('(')
            if '= ' in funcionLocal:
                igual = funcionLocal.find('= ') + 2
            elif '=' in funcionLocal:
                igual = funcionLocal.find('=') + 1
            else:
                igual = 0
            llamada = funcionLocal[igual:paren]
            if llamada in listaOG:
                sublistaLL.append(llamada)
    del paren, igual, funcion, llamada, funcionLocal
    return sublistaLL

def txt_maker(listaOG, dixTOT, dixRec):
    """
    [Autor: Lucas M. Diana]
    Genera el archivo "analizador.txt"
    
    """

##  Genera la primera linea y a escribe en el txt
    
    linea = ''
    longitud = 0
    for funcion in listaOG:
        if len(funcion) > longitud:
            longitud = len(funcion)
    longitud += 1
    linea.append('|\t{0:{1}} ').format('Funcion/es', longitud)
    del longitud
    contador = 0
    for funcion in listaOG:
        linea.append('| {} ').format(contador)
        contador += 1
    linea.append('|\n')
    analizador = open(analizador.txt, 'w+')
    analizador.write(linea)

##  Genera el separador de renglones"""
    
    separador = ''
    for char in len(linea):
        separador.append('-')
    separador.append('\n')
    del char
    
##  Genera y suma el resto de las lineas
##  y los separadores de renglones que correspondan.
    
    for funcion in listaOG:
        analizador.write(separador)
        linea = ''
        linea.append('|\t{0:{1}}').format(funcion, longitud)
        contador = 0
        for funcion2 in listaOG:
            if dixTOT[funcion][contador] > 0 and dixRec[funcion][contador] == 'X':
                linea.append('|{0}/{1}').format(dixTOT[funcion][contador], dixRec[funcion][contador])
            elif dixTOT[funcion][contador] > 0:
                linea.append('| {} ').format(dixTOT[funcion][contador])
            elif dixRec[funcion][contador] == 'X':
                linea.append('| {} ').format(dixRec[funcion][contador])
            else:
                linea.append('|   ')
            contador += 1
        linea.append('|\n')
        analizador.write(linea)
    analizador.write(separador)
    analizador.close()
    del funcion, funcion2, linea, contador

def printer():
    """
    [Autor: Lucas M. Diana]
    Crea e imprime los contenidos del archivo "analizador.txt" en la pantalla.
    
    """
    
    if os.isfile(os.getcwd()\\analizador.txt):
        print('analizador.txt existe, leyendo...')
        time.sleep(2)
        os.system('cls')
        analizador = open(analizador.txt, 'r')
    else:
        print('analizador.txt no existe, creando...')
        listaOG = generador_de_lista_de_funciones()
        listaLL = generador_de_listas_de_llamadas()
        dixTOT = contador_de_invocaciones(listaOG, listaLL)
        dixRec = contador_de_llamadas(listaOG, dixTOT)
        txt_maker(listaOG, dixTOT, dixRec)
        del listaOG, listaLL, dixRec, dixTOT
        time.sleep(2)
        print('analizador.txt creado, leyendo...')
        time.sleep(2)
        os.system('cls')
        analizador = open(analizador.txt, 'r')
    print(analizador.read())
    analizador.close()

## Falta un metodo para volver al programa principal (de ser necesario)
## Solo usar printer() - hace todo lo demas
## Renombrar variables confusas (?) para hacer mas legible el codigo.
## Ver si es posible reducir la cantidad de 'for's (cada uno tiene su uso) T_T
## time.sleep(n) no hace nada durante n segundos
