# Datos de prueba:
#####################################################################################################################################
# generador_de_lista_de_funciones() => listaOG, proviene de módulo3
listaOG = ['main', 'ingresar_datos', 'solicitar_valor', 'validar_valor', 'calcular_resultado', 'solicitar_rango', 'imprimir_informe']

# generador_de_lista_de_llamadas(listaOG) => listaLL
listaLL = [
    ['ingresar_datos', 'calcular_resultado', 'solicitar_rango', 'imprimir_informe'],
    ['solicitar_valor', 'solicitar_valor'],
    ['validar_valor'],
    [],
    [],
    ['solicitar_valor'],
    []
]

# contador_de_invocaciones(listaOG, listaLL) => dixTOT, proviene de módulo3
dixTOT = {
    'main': [0,1,0,0,1,1,1],
    'ingresar_datos': [0,0,2,0,0,0,0],
    'solicitar_valor': [0,0,0,1,0,0,0],
    'validar_valor': [0,0,0,0,0,0,0],
    'calcular_resultado': [0,0,0,0,0,0,0],
    'solicitar_rango': [0,0,1,0,0,0,0],
    'imprimir_informe': [0,0,0,0,0,0,0]
}

# contador_de_llamadas(listaOG, dixTOT) => dixRec, proviene de módulo3
dixRec = {
    'main': ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    'ingresar_datos': ['X', 'O', 'O', 'O', 'O', 'O', 'O'],
    'solicitar_valor': ['O', 'X', 'O', 'O', 'O', 'X', 'O'],
    'validar_valor': ['O', 'O', 'X', 'O', 'O', 'O', 'O'],
    'calcular_resultado': ['X', 'O', 'O', 'O', 'O', 'O', 'O'],
    'solicitar_rango': ['X', 'O', 'O', 'O', 'O', 'O', 'O'],
    'imprimir_informe': ['X', 'O', 'O', 'O', 'O', 'O', 'O']
}
#####################################################################################################################################

# tengo que generar:
#####################################################################################################################################
dixDependencias = {
    'main': [0, 4, ['ingresar_datos', 'calcular_resultado', 'solicitar_rango', 'imprimir_informe']],
    'ingresar_datos': [1, 2, ['solicitar_valor', 'solicitar_valor']],
    'solicitar_valor': [2, 1, ['validar_valor']],
    'validar_valor': [1, 0, []],
    'calcular_resultado': [1, 0, []],
    'solicitar_rango': [1, 1, ['solicitar_valor']],
    'imprimir_informe': [1, 0, []]
}
#####################################################################################################################################
# función para calcular canti lineas por función: TPG_parte_5 -> módulo, 

POS_CAMPO_CANTI_INVOCACIS = 1
POS_CAMPO_CANTI_LLAMADAS = 0
POS_CAMPO_LISTA_INVOCACIS = 2

'''
Función incompleta...
def generar_dependencias(listaLL, dixRec):
    for funcion, listaLlamadas in dixRec.items():
        cantiLlamadas = 0
        for Llamada in listaLlamadas:
            if (llamada == 'X'):
                cantiLlamadas += 1        
    return dixDependencias
'''    
    
def generar_arbol_dependencias(dixDependencias):
    listaNodosIniciales=[]
    
    # identificar nodos primarios
    for funcion, listaDependencias in dixDependencias.items():
        if (listaDependencias[POS_CAMPO_CANTI_LLAMADAS] == 0):
            listaNodosIniciales.append(funcion)
    
    # recorre el bosque
    for nodoInicial in listaNodosIniciales:
            # recorre un arbol
            msjNodoInicial = nodoInicial + '(la cantidad de lineas es tanto)'
            print(msjNodoInicial, end = '')
            listaInvocacis = dixDependencias[nodoInicial][POS_CAMPO_LISTA_INVOCACIS]
            desplazamientoNodo = ' '*len(msjNodoInicial)
            
            # corta el arbol para pasar a otro
            for funcionInvocada in listaInvocacis:
                imprimir_arbol_dependencias(desplazamientoNodo, funcionInvocada, dixDependencias)
    pass

def imprimir_arbol_dependencias(desplazamientoNodo, funcionInvocada, dixDependencias):
    #ORIGINAL me imprimo
    msjNodo = ' --> ' + funcionInvocada + '(la cantidad de lineas es tanto)'
    print(msjNodo, end = '')
    #desplazamientoNodoTotal = desplazamientoNodo 
    #desplazamientoNodoTotal += ' '*len(msjNodo)
        
    # caso base: si tengo hijos me llamo otra vez
    listaInvocacis = dixDependencias[funcionInvocada][POS_CAMPO_LISTA_INVOCACIS]
    if (len(listaInvocacis) == 0):
        print('\n')
        print(' '*62, end = '')
        #print(desplazamientoNodoTotal, end = '')
        #print(len(desplazamientoNodoTotal), end = '')
        return
    
    for funci in listaInvocacis:
        imprimir_arbol_dependencias(desplazamientoNodo, funci, dixDependencias)
    
generar_arbol_dependencias(dixDependencias)