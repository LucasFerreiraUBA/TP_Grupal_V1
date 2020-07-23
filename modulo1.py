
def leer_programas():
    """
    [Autor: Lucas Ferreira]
    [Ayuda: lee programas.txt, crea un diccionario y lo retorna]
    """
    programa_num = 0
    diccionario_salida = {}
    with open('programas.txt', encoding='utf-8') as p:
        renglon = None
        while renglon != '':
            renglon = p.readline()
            if renglon != '':
                #agrega al diccionario, usando de llave "programa_numeroDePrograma" e igualandolo a la direccion del programa
                diccionario_salida['programa' +str(programa_num)] = renglon.strip('\n')
            programa_num += 1
    return diccionario_salida

#recibe el diccionario de direcciones
def manejar_contenido(direcciones):
    """
    [Autor: Lucas Ferreira]
    [Ayuda: Lee el diccionario de direcciones, abre cada archivo, consigue el nombre de cada modulo y retorna una tupla con cada funcion ordenada]
    """
    lista_final = []
    #bucle que va abriendo cada direccion guardada
    for D in direcciones:
        with open(direcciones[D], encoding='utf-8') as p:
            programa = p.read().split('\n')
        nombre_modulo = direcciones[D].split('\\')[-1]
        for funcion in ordenar_contenido(programa,nombre_modulo):
            lista_final.append(funcion)
    lista_final = insercion(lista_final)
    return tuple(lista_final)

def insercion(lista):
    """
    [Autor: Lucas Ferreira]
    [Ayuda: ordena las listas por metodo de insercion, al inicio de cada lista está el nombre de la funcion, así quedan ordenadas alfabeticamente]

    """
    n = len(lista)
    for i in range(1,n):
        elemento = lista[i]
        max_local = i-1
        while max_local >= 0 and elemento < lista[max_local]:
            lista[max_local+1] = lista[max_local]
            max_local -= 1
        lista[max_local+1] = elemento
    #no se por que el ultimo elemento queda duplicado :C
    return lista[:n-1]
    
#recibe el texto de un modulo
#retorna una lista de sublistas, cada sublista es unafuncion

def ordenar_contenido(programa,nombre_mod):
    """
    [Autor: Lucas Ferreira]
    [Ayuda: ordena todo lo escrito en un modulo, separandolo en sublistas que corresponden a funciones, cada sublista está organizada para que sea facil encontrar
    toda la informacion vital para posteriormente generar los archivos csv. Adicionalmente convierte a las listas que ya no serán manipuladas en tuplas]
    
    """
    #lista de todo lo presente en el modulo
    lista_mod = []
    comentarios = []
    codigo = []
    es_comentario = False
    for linea in programa:
        linea = linea.strip()
        #ignora las lineas vacías e imports
        if linea == '' or 'import ' in linea:
            continue
        #si son comentarios multilinea, agrega la linea a la lista de comentarios
        #y cambia "es_comentario" a True o False, para luego el resto de las lineas reconocerlas como comentario o no
        if '\"\"\"' in linea:
            if es_comentario and linea.count('\"\"\"') == 1:
                es_comentario = False
            elif linea.count('\"\"\"') == 1:
                es_comentario = True
            comentarios.append(linea)
        elif es_comentario:
            if '[autor:' in linea.lower():
                comentarios.insert(0,linea)
            else:
                comentarios.append(linea)
        elif linea[0] == '#':
            if comentarios != []:
                comentarios.append(linea)
        # reconoce si está creando una funcion y genera la sublista correspondiente ademas de almacenar el codigo y comentarios guardados, en la funcion anterior si la hay
        elif linea.split()[0] == 'def':
            #nombre es una lista de nombre_funcion/parametros
            nombre = linea.split('def ')[1].split('(')
            if len(lista_mod) > 0:
                lista_mod[-1].append(tuple(codigo))
                codigo = []
                try:
                    if '[autor:' not in comentarios[0].lower():
                        comentarios.insert(0,'[Autor: ausente]')
                except IndexError:
                    comentarios.append('[Autor: ausente]')
                lista_mod[-1].append(tuple(comentarios))
                comentarios = []
            lista_mod.append([nombre[0],'('+nombre[1].strip(':'), nombre_mod])
        else:
            codigo.append(linea)
    #revisa si hay un autor, si no lo hay, agrega ausente en el espacio correspondiente
    if len(comentarios) == 0:
        comentarios.append('[Autor: ausente]')
    elif '[autor:' not in comentarios[0].lower():
        comentarios.insert(0,'[Autor: ausente]')
    lista_mod[-1].append(tuple(codigo))
    lista_mod[-1].append(tuple(comentarios))
    return lista_mod


def generar_csv(tupla):
    """
    [Autor: Lucas Ferreira]
    [Ayuda: lee las sublistas que corresponden a las funciones y extraen la información para separarla en dos archivos csv]

    """
    #las 2 cadenas de texto que serán guardadas como csv al final de la funcion
    fuente_unico = ''
    comentarios = ''
    for funcion in tupla:
        fuente_unico += funcion[0] + ';' 
        comentarios += funcion[0] + ';'
        fuente_unico += funcion[1] + ';'
        comentarios +=  funcion[4][0] + ';'
        fuente_unico += funcion[2].strip('.py') + ';'
        #agrega todo el codigo al final de fuente_unico, separando cada linea por una coma
        for linea in funcion[3]:
            fuente_unico += linea + ';'
                                                #lo hace desde la primera posicion para excluir al autor en los comentarios
        comentario_separado = separar_comentario(funcion[4][1:])
        try:
            comentarios += comentario_separado[0] +';'
        except TypeError:
            comentarios+=';'
        try:
            comentarios += comentario_separado[1] + ';'
        except TypeError:
            comentarios += ';'
        fuente_unico += '\n'
        comentarios += '\n'
    return (fuente_unico,comentarios)

def separar_comentario(comentarios):
    """
    [Autor: Lucas Ferreira]
    [Ayuda: lee la lista de comentarios de cada funcion y separa los comentarios importantes de ayuda, de el resto de los comentarios]

    """
    es_importante = False
    comentario_importante = ''
    comentario_normal = ''
    for linea in comentarios:
        if '[Ayuda' in linea:
            if ']' not in linea:
                es_importante = True
            comentario_importante += linea
        elif es_importante == False:
            comentario_normal += linea + ';'
        elif es_importante:
            if ']' in linea:
                es_importante = False
            comentario_importante += linea
    return(comentario_importante,comentario_normal)
