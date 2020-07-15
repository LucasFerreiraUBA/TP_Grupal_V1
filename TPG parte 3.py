import os

def contador_de_invocaciones(listaOG): 
    """
    [Autor: Lucas M. Diana]
    Genera un diccionario con la cantidad de referencias
    que realiza cada funcion.
    
    """
      
    dixTOT = {}
    contPosLL = 0
    for func in listaOG:
        dixTOT[func] = []     
        contPosS = 0
        sublis = []
        for fc2 in listaOG:
            sublis.append(0)      
            sublis[contPosS] = 0            
            for call in listaLL[contPosLL]:
                if fc2 == call:                    
                    sublis[contPosS] += 1
            contPosS += 1
        contPosLL += 1        
        dixTOT[func] = sublis
    return dixTOT

def contador_de_llamadas(listaOG, listaLL): 
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
    return dixRec


def generador_de_lista_de_funciones():
    """
    [Autor: Lucas M. Diana]
    Genera una lista con todas las funciones que existen
    dentro de fuente_unico.csv
    
    """

    fuente_unico =  open('fuente_unico.csv','r')
    listaFuncP = []
    listaOG = []
    for i in fuente_unico:
        if i.startswith("def "):
            listaFuncP.append(i.replace('def ',''))
    for j in listaFuncP:
        paren = j.find('(')
        funcion = j[:paren]
        listaOG.append(funcion)
    fuente_unico.close()
    return listaOG

def generador_de_listas_de_llamadas():
    """
    [Autor: Lucas M. Diana]
    Genera una lista para cada funcion con todas las llamadas
    que existen dentro. Estas se incorporan a una lista de listas.
    
    """
    fuente_unico =  open('fuente_unico.csv','r')
    listaFParcial = []
    listaLL = []
    for a in fuente_unico:
        if a.startswith("def ") and listaFParcial != []:
            sublistaLL = procesar_listaFP(listaFParcial)
            listaLL.append(sublistaLL)
            listaFParcial = []
            listaFParcial.append(a)
        else:
            listaFParcial.append(a)
    
##  Para la ultima, podria resolverse con eof
    
    sublistaLL = procesar_listaFP(listaFParcial)
    listaLL.append(sublistaLL)
    
    return listaLL

def procesar_listaFP(listaFParcial):
    """
    [Autor: Lucas M. Diana]
    Filtra la lista con cada linea de codigo de una funcion
    y devuelve una lista que contiene solo las llamadas de la funcion
    
    """
    sublistaLL = []
    for b in listaFParcial:
        llamada = None
        if b.endswith(')'):
            paren = b.find('(')
            if '= ' in b:
                igual = b.find('= ') + 2
            elif '=' in b:
                igual = b.find('=') + 1
            else:
                igual = 0
            llamada = b[igual:paren]
            if llamada in listaOG:
                sublistaLL.append(llamada)
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
    linea.append('|\t{0:{1}} ').format('Funcion/es', longitud)
    contador = 0
    for funcion in listaOG:
        linea.append('| {} ').format(contador)
        contador += 1
    linea.append('|\n')
    analizador = open(analizador.txt, 'w+')
    analizador.write(linea)

##  Genera el separador de renglones"""
    
    separador = ''
    for i in len(linea):
        separador.append('-')
    separador.append('\n')
    
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
        analizador.write(linea)
    analizador.write(separador)
    analizador.close()

def printer():
    """
    [Autor: Lucas M. Diana]
    Imprime los contenidos del archivo "analizador.txt" en la pantalla.
    
    """
    if os.isfile(os.getcwd()\\analizador.txt):
        print('analizador.txt existe, leyendo...')
        os.system('cls')
        analizador = open(analizador.txt, 'r')
    else:
        print('analizador.txt no existe, creando...')
        txt_maker()
        print('analizador.txt creado, leyendo...')
        os.system('cls')
        analizador = open(analizador.txt, 'r')
    for i in analizador:
        linea = ''
        linea.append(i)
        if linea.endswith('\n'):
            print(linea)
    analizador.close()

"""
Ejecucion del modulo

listaOG = generador_de_lista_de_funciones()
listaLL = generador_de_listas_de_llamadas() 
dixTOT = contador_de_invocaciones(listaOG)
dixRec = contador_de_llamadas(listaOG, listaLL)
txt_maker(listaOG, dixTOT, dixRec)
printer()


Falta un metodo para volver al programa principal
Chequear si es mejor dejar que las funciones se invoquen entre si
O ejecutar el modulo en su totalidad.
Renombrar todas las variables para hacer mas legible el codigo.
Ver si es posible reducir la cantidad de 'for's y/o crear una funcion
que pueda resolver los casos de 'for' anidados
"""
