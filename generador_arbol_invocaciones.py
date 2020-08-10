import An_Reu_Cod

def generar_dependencias():
    """
    [Autor: David DJ Sandoval]
    [Ayuda: Función para armar el diccionario de dependencias que se utilizará para recorrer el árbol de dependencias]
    """   
    listaOG = An_Reu_Cod.generador_de_lista_de_funciones()
    listaLL = An_Reu_Cod.generador_de_listas_de_llamadas(listaOG)
    dixTOT = An_Reu_Cod.contador_de_invocaciones(listaOG, listaLL)
    dixRec = An_Reu_Cod.contador_de_llamadas(listaOG, dixTOT)
    dixDependencis = {}
    i = 0
    for funcion, listaLlamadas in dixRec.items():
        # calculo la cantidad de llamadas por función
        cantiLlamadas = 0
        for llamada in listaLlamadas:
            if (llamada == 'X'):
                cantiLlamadas += 1
        dixDependencis[funcion] = [cantiLlamadas, listaLL[i]]
        i += 1
    
    return dixDependencis


POS_CAMPO_CANTI_LLAMADAS = 0
POS_CAMPO_LISTA_INVOCACIS = 1
def generar_arbol_dependencias():
    """
    [Autor: David DJ Sandoval]
    [Ayuda: Función para imprimir el arbol de dependencias]
    """
    # arma diccionario de dependencias
    dixDependencias = generar_dependencias()
    # identifica nodos primarios
    listaNodosPrimarios=[]
    for funcion, listaDependencias in dixDependencias.items():
        if (listaDependencias[POS_CAMPO_CANTI_LLAMADAS] == 0):
            listaNodosPrimarios.append(funcion)
    # recorre el bosque
    for funcionPrima in listaNodosPrimarios:
        # imprime el nodo primario del arbol
        msjNodoPrimario = funcionPrima + '(la cantidad de lineas es tanto)'
        print(msjNodoPrimario, end = '')
        # genera el desplazamiento a la derecha respectivo al nodo primario
        desplazamientoNodoPrima = ' '*len(msjNodoPrimario)
        # genera lista de nodos secundarios
        listaNodosSecundarios = dixDependencias[funcionPrima][POS_CAMPO_LISTA_INVOCACIS]
        # imprime cada nodo secundario con todos sus hijos respectivos (corta el nodo secundario del arbol para pasar a otro)
        for funcionSecu in listaNodosSecundarios:
            # imprime nodo secundario sin hijos
            if (len(dixDependencias[funcionSecu][POS_CAMPO_LISTA_INVOCACIS]) == 0):
                msjNodoSecu = '\r\n' + desplazamientoNodoPrima + ' --> ' + funcionSecu + '(la cantidad de lineas es tanto)'
                print('\r\n' + msjNodoSecu)
                print('\r\n' + desplazamientoNodoPrima, end = '')
            # imprime nodo secundario con hijos
            else:
                imprimir_arbol_dependencias(funcionSecu, dixDependencias, desplazamientoNodoPrima)
    return

def imprimir_arbol_dependencias(funcionInvocada, dixDependencias, desplazamientoNodoPrima):
    """
    [Autor: David DJ Sandoval]
    [Ayuda: Función para imprimir los nodos del árbol de dependencias hasta encontrar el nodo que no realice invocaciones a otras funciones]
    """
    # imprime la función invocada asociado al nodo respectivo
    msjNodo = ' --> ' + funcionInvocada + '(la cantidad de lineas es tanto)'
    print(msjNodo, end = '')
    # genera el desplazamiento a la derecha respectivo
    desplazamientoNodo = ' '*len(msjNodo)
    desplazamientoTotal = desplazamientoNodoPrima
    desplazamientoTotal += desplazamientoNodo
    # genera la lista de nodos hijos asociada la función invocada
    listaNodosHijos = dixDependencias[funcionInvocada][POS_CAMPO_LISTA_INVOCACIS]
    # si la lista de nodos hijos está vacía entonces se cortan los llamados recursivos (caso base)
    if (len(listaNodosHijos) == 0):
        print('\r\n' + desplazamientoTotal, end = '')
        return
    # si la lista de nodos hijos no está vacía entonces hago llamado recursivo pasándole cada nodo hijo
    for funcionHijo in listaNodosHijos:
        imprimir_arbol_dependencias(funcionHijo, dixDependencias, desplazamientoNodoPrima)
