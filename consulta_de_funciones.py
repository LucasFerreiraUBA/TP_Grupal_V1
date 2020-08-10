
def leer_comentario(archivo):
    """
        [Autor: Julian Uño]
        [Ayuda: Lee por linea del archivo recibido, y devuelve el registro
        sin salto de linea y divido por ',' en tres campos , si no devuelve vacio, solo
        separa tres campos]
    """
    
    linea = archivo.readline()
    if linea:
        devolver = linea.rstrip('\n').split(',', 2)
    else:
        devolver = "","",""
        
    return devolver
    
def leer_codigo(archivo):
    """
        [Autor: Julian Uño]
        [Ayuda: Lee por linea del archivo recibido, y devuelve el registro
        sin salto de linea y divido por ',' si no devuelve vacio. solo
        separa dos campos]
    """
   
    linea = archivo.readline()
    if linea:
        retornar = linea.rstrip('\n').split(',', 1)
    else:
        retornar = ""," "
        
    return retornar

def mostrar_tabla(lista):
    """
        [Autor: Julian Uño]
        [Ayuda:  Recibe un nombre de funcion y una
        tupla de listas donde se encuentra, va
        generando una tabla con las funciones de los archivos fuentes]
    """
    
    pos_nombre = 0
    
    while pos_nombre < len(lista):
        
        for nombre in range(0, 4):
            
            if pos_nombre < len(lista) and lista[pos_nombre]:
                
                print('{0:^25}'.format(lista[pos_nombre]), end = '\t\t')
                pos_nombre += 1
            
        print("\n")
    
def listar_comentarios(archivo_comentarios):
    """
        [Autor: Julian Uño]
        [Ayuda: Recibe el archivo comentarios.csv y devuelve una tupla
        con las lineas de comentarios de todas las funciones]
    """
    
    lista_nombres = []
    lista_autor = []
    lista_info_ayuda = []
    ar_comentarios = open(archivo_comentarios, "r")
    nombre_funcion, autor, resto_linea = leer_comentario(ar_comentarios)
    info_ayuda = resto_linea[:resto_linea.find(']')+1]
    
    while nombre_funcion:

                lista_nombres.append(nombre_funcion)
                lista_autor.append(autor)
                lista_info_ayuda.append(info_ayuda)
                nombre_funcion, autor,resto_linea = leer_comentario(ar_comentarios)
                info_ayuda = resto_linea[:resto_linea.find(']')+1]
        
    ar_comentarios.close()
     
    return lista_nombres, lista_autor, lista_info_ayuda

def listar_lineas_codigo(archivo_fuente_unico):
    """
        [Autor: Julian Uño]
        [Ayuda: Recibe el archivo fuente_unico.csv y
        lista las lineas de codigo en sublistas]
    """
    
    ar_cod = open(archivo_fuente_unico, 'r')
    
    lista_nombres2 = []
    lista_parametro = []
    lista_modulo = []
    lista_instrucciones = []
    nombre_f, resto = leer_codigo(ar_cod)
    parametro, resto = resto.split('),', 1)
    modulo, resto = resto.split(',', 1)
    parametro += ')'
    instrucciones = resto
    
    while nombre_f:
        
        lista_nombres2.append(nombre_f)
        lista_parametro.append(parametro)
        lista_modulo.append(modulo)
        lista_instrucciones.append(instrucciones)
        nombre_f, resto = leer_codigo(ar_cod)
        
        if nombre_f:
            parametro, resto = resto.split('),', 1)
            parametro += ')'
            modulo, resto = resto.split(',', 1)
            instrucciones = resto
    
    ar_cod.close()
    #devuelve una tupla de las listas
    return lista_nombres2, lista_parametro, lista_modulo, lista_instrucciones
    

def ingresar_funcion():
    """
        [Autor: Julian Uño]
        [Ayuda: Solicita el ingreso del nombre de la función
        y el caracter especial]
    """
    
    return input("Función: ")

def seleccionar_solo_nombre(nombre_con_caracter, caracter):
    """
        [Autor: Julian Uño]
        [Ayuda: recibe el nombre de la funcion con el caracter especial que lee de la entrada y
        el caracter especial para cortar la cadena nombre_caracter, con esto
        devuelve solo el nombre de la funcion, lo uso en los dos primeros if, elif de describir
        funciones]
    """
    
    nombre_funcion = nombre_con_caracter[0: nombre_con_caracter.find(caracter)]
    
    return nombre_funcion
    
def describir_funciones():
    """
        [Autor: Julian Uño]
        [Ayuda: Analiza lo que ingresa el usuario, y
        de acuerdo al caracter especial va a impirmir comentarios, instrucciones, informacion
        relativo a una funcion en particular o varias en funcion de lo ingresado]
    """
    
    print("Funciones".center(120, "-"))
    
    tupla_comentarios = listar_comentarios('comentarios.csv')
    tupla_codigos_funciones = listar_lineas_codigo('fuente_unico.csv')
    l_nombres_funciones = tupla_comentarios[0] #lista con los nombres de las funciones extraida de la tupla de comentarios
    
    mostrar_tabla(l_nombres_funciones)
    nombre_con_caracter = ingresar_funcion()
    
    while nombre_con_caracter:
         
        if '?' in nombre_con_caracter and seleccionar_solo_nombre(nombre_con_caracter, '?') in l_nombres_funciones:
            # el indice cero es la posicion de los nombres de las funciones
            nombre_funcion = seleccionar_solo_nombre(nombre_con_caracter, '?')
            
            posicion = l_nombres_funciones.index(nombre_funcion)
                #posicion: variable dependiendo del nombre de la funcion para determinar
                #la posicion en las listas de parametros y modulos, comentarios
            
            descripcion = tupla_comentarios[2][posicion][1:-1]
            autor = tupla_comentarios[1][posicion][1:-1]
            parametro = tupla_codigos_funciones[1][posicion]
            modulo_funcion = tupla_codigos_funciones[2][posicion]
                
            print('-'.center(120, '-'))
            
            print(descripcion)
            print('-'.center(120, '-'))
            
            print(autor)
            print('-'.center(120, '-'))
            
            print('parametro/s: ',parametro)
            print('-'.center(120, '-'))
            
            print('modulo: ', modulo_funcion)
            print('-'.center(120, '-'))
            
            print('='.center(120, '='))
            
            nombre_con_caracter = ingresar_funcion()
            
        elif '#' in nombre_con_caracter and seleccionar_solo_nombre(nombre_con_caracter, '#') in l_nombres_funciones:
                
                nombre_funcion = seleccionar_solo_nombre(nombre_con_caracter, '#')
                posicion = l_nombres_funciones.index(nombre_funcion)
            
                autor = tupla_comentarios[1][posicion][1:-1]
                #autor: guarda de la tupla de listas, en la lista de autores, la posicion del
                #nombre de la funcion y lo rebana sacandole los corchetes
                parametro = tupla_codigos_funciones[1][posicion]
                modulo_funcion = tupla_codigos_funciones[2][posicion]
                instruccion = tupla_codigos_funciones[3][posicion]
                descripcion = tupla_comentarios[2][posicion][1:-1]
                #descripcion: guarda de la tupla de listas, en la lista de ayudas, la posicion del
                #nombre de la funcion y lo rebana sacandole los corchetes
            
                print('def ' + nombre_funcion + parametro)
                print('"\"\"')
                print(autor)
                print(descripcion)
                print('"\"\"')
            
                print('Instrucciones de esta función: ')
                print(instruccion)
                
                #separador de funcion y funcion con '='
                print('='.center(120, '='))
            
                nombre_con_caracter = ingresar_funcion()
            
        elif "?todo" == nombre_con_caracter:
            
            posicion = 0
            
            for nombre in l_nombres_funciones:# es donde se encuentra la lista de nombres de funciones
                
                print("nombre de la funcion: ", nombre)
                print('-'.center(120, '-'))
                print("descripcion: {}".format(tupla_comentarios[2][posicion]))
                print('-'.center(120, '-'))
                print("autor: {}".format(tupla_comentarios[1][posicion]))
                print('-'.center(120, '-'))

                print("parametros: {}".format(tupla_codigos_funciones[1][posicion]))
                print('-'.center(120, '-'))

                print("modulo: {}".format(tupla_codigos_funciones[2][posicion]))
                print('='.center(120, '='))
                
                posicion += 1
                
            nombre_con_caracter = ingresar_funcion()
                    
        elif "#todo" == nombre_con_caracter:
            
            posicion = 0
            
            for nombre in tupla_comentarios[0]:
                
                print('def ' + nombre + tupla_codigos_funciones[1][posicion])
                
                print('"\"\"')
                print(tupla_comentarios[1][posicion])
                print(tupla_comentarios[2][posicion])
                print('"\"\"')
            
                print('Instrucciones de esta Función: ')

                print(tupla_codigos_funciones[3][posicion])
                print('-'.center(120, '-'))
                print('='.center(120, '='))
                posicion += 1
                
            nombre_con_caracter = ingresar_funcion()
                
        elif "imprimir ?todo" == nombre_con_caracter:
            #genera un archivo con la informacion de todas las funciones
            
            with open('ayuda_funciones.txt', 'w') as ayuda:
                
                subindice = 0
                
                for nombre in l_nombres_funciones:
                    
                    ayuda.write('Nombre Función: ' + nombre + '\n')
                    if len(tupla_comentarios[2][subindice][1:-1]) < 80:
                        ayuda.write(tupla_comentarios[2][subindice][1:-1]+ '\n')    #escribe la ayuda
                    else:
                        ayuda.write(tupla_comentarios[2][subindice][1:-1][:81]+ '\n')
                        ayuda.write(tupla_comentarios[2][subindice][1:-1][81:]+ '\n')
                        
                    ayuda.write(tupla_comentarios[1][subindice][1:-1] + '\n')    #escribe el autor
                    ayuda.write('Parametros: ' + tupla_codigos_funciones[1][subindice] + '\n')
                    ayuda.write('Modulo: ' + tupla_codigos_funciones[2][subindice] + '\n')
                    ayuda.write('\n')
                    subindice += 1
                    
            nombre_con_caracter = ingresar_funcion()
            
        else:
            
            print("Ocurrio un error al ingresar datos, intente de nuevo.")
            nombre_con_caracter = ingresar_funcion()
            
