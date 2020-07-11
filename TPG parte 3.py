def contador_de_invocaciones():
##  SOLO LLAMAR AL CONTADOR DE INVOCACIONES SI EL DIX NO EXISTE!!  
    
    """
    [Autor: Lucas M. Diana]
    Genera un diccionario con la cantidad de referencias
    que realiza cada funcion
    
    para testear su funcionamiento, use:

        listaLL = [['funcion2()', 'funcion3()', 'funcion2()'],
                   ['funcion3()', 'funcion4()', 'funcion1()'],
                   ['funcion1()', 'funcion2()'],
                   ['funcion4()']]

        listaOG = ['funcion1()', 'funcion2()', 'funcion3()', 'funcion4()']

    devolvio: (estan sueltos)
        
        dixTOT = {'funcion1()': [0, 2, 1, 0],        llama 2v a 2 y 1v a 3
                  'funcion2()': [1, 0, 1, 1],        llama 1v a 1, 3 y 4
                  'funcion3()': [1, 1, 0, 0],        llama 1v a 1 y 2
                  'funcion4()': [0, 0, 0, 1]}        llama 1v a 4
                  
        dixRec = {'funcion1()': ['O', 'X', 'X', 'O'],   llaman 2 y 3
                  'funcion2()': ['X', 'O', 'X', 'O'],   llaman 1 y 3
                  'funcion3()': ['X', 'X', 'O', 'O'],   llaman 1 y 2
                  'funcion4()': ['O', 'X', 'O', 'X']}   llaman 2 y 4
                                                      (es correcto!) """
    
    listaOG, listaLL = generador_de_lista_de_funciones()    
    dixTOT = {}
    contPosLL = 0
    """ contPosLL determina que sublista de listaLL se usa
        hay que generar una llave para cada funcion"""
    for func in listaOG:
        dixTOT[func] = []     
        contPosS = 0
        sublis = []
        """contPosS determina a que funcion(llamada) se refiere el valor
        hay que generar una sublista para cada llave en el dix
        (listaLL tiene las llamadas literales, no las cant)
        agarrar cada funcion y comparar con la sublista"""
        for fc2 in listaOG:
            sublis.append(0)
            """evaluo cada funcion(llamada)..."""            
            sublis[contPosS] = 0            
            for call in listaLL[contPosLL]:
                """... con cada llamada [si la funcion(llamada)
                        no se la llama, queda el valor en cero]"""
                if fc2 == call:                    
                    sublis[contPosS] += 1
            contPosS += 1
        """cuando termino de chequear las llamadas de la primer funcion,
            la sumo al diccionario y paso a la siguiente"""
        contPosLL += 1        
        dixTOT[func] = sublis
    """Una vez calculadas todas las llamadas del programa,
        devuelvo el diccionario

        ((Hasta aca chequeo llamadas realizadas))

        Ahora determino que funcion depende de cada una
        (llamadas recividas)"""

    dixRec = {}
    pos = 0
    for recive in listaOG:
        listaRec = []
        for envia in dixTOT:
            if dixTOT[envia][pos] > 0:
                listaRec.append('X')
            else:
                listaRec.append('0')
        dixRec[recive] = listaRec
        pos += 1

##  SOLO LLAMAR AL CONTADOR DE INVOCACIONES SI EL DIX NO EXISTE!!
    return dixTOT, dixRec

def generador_de_lista_de_funciones():
    """
    [Autor: Lucas M. Diana]
    Genera una lista con todas las funciones que existen dentro de fuente_unico.csv

    para testear su funcionamiento, use este mismo archivo guardado como .csv
    devolvio:
            
    listaOG = ['contador_de_invocaciones', 'generador_de_lista_de_funciones']

            [es correcto! (x ahora)]     """

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
    """Hasta aca genera la lista de funciones del programa
        Continuo con la lista de llamadas"""
    fuente_unico.close()
    fuente_unico =  open('fuente_unico.csv','r')
    listaFParcial = []
    listaLL = []
    for a in fuente_unico:
        if a.startswith("def ") and listaFParcial != []:
            sublistaLL = procesar_listaFP(listaFParcial)
            listaLL.append(sublistaLL)
            listaFParcial = []
            listaFParcial.append(a)
        elif a.startswith("def "):
            listaFParcial.append(a)
        else:
            listaFParcial.append(a)
    sublistaLL = procesar_listaFP(listaFParcial)
    listaLL.append(sublistaLL)
    return listaOG, listaLL

def procesar_listaFP(listaFParcial):
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
