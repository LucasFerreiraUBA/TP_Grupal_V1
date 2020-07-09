def contador_de_invocaciones(listaOG, listaLL):
    """
    [Autor: Lucas M. Diana]
    Genera un diccionario con la cantidad de referencias que realiza cada funcion
    
    para testear su funcionamiento, use:

        listaLL = [['funcion2()', 'funcion3()', 'funcion2()'],
                   ['funcion3()', 'funcion4()', 'funcion1()'],
                   ['funcion1()', 'funcion2()'],
                   ['funcion2()']]

        listaOG = ['funcion1()', 'funcion2()', 'funcion3()', 'funcion4()']

        devolvio: (esta suelta)
        
        dixTOT = {'funcion1()': [0, 2, 1, 0],
                  'funcion2()': [1, 0, 1, 1],
                  'funcion3()': [1, 1, 0, 0],
                  'funcion4()': [0, 1, 0, 0]}    (es correcto!)
    """
    
##  SOLO LLAMAR AL CONTADOR DE INVOCACIONES SI EL DIX NO EXISTE!!  
##  listaLL = ["lista con todas las llamadas a otras funciones"]
##  listaOG = ["lista con todas las funciones"]

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
        devuelvo el diccionario"""
##  SOLO LLAMAR AL CONTADOR DE INVOCACIONES SI EL DIX NO EXISTE!!
    return dixTOT
