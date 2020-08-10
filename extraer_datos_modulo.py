def buscar_funciones(arch_python):
    """[Autor: Javier Acho]
       [Ayuda: Devuelve una secuencia con los nombres de las funciones que se
        definen en el archivo que recibe.
        El archivo debe estar abierto en modo lectura.]
    """

    nombres_funciones = []

    for linea in arch_python:
        if linea.startswith("def "):
            nom_funcion = linea[4:linea.index("(")]
            nombres_funciones.append(nom_funcion)

    arch_python.seek(0)  # leí todo el archivo, vuelvo el cursor o puntero al inicio
    return nombres_funciones

def encontrar_declaracion_funcion(arch_python, nom_funcion):
    """[Autor: Javier Acho]
       [Ayuda: Devuelve una cadena que contiene la declaración de la función en
        el modulo python que recibe.
        El archivo debe estar abierto en modo lectura.]
    """

    linea = arch_python.readline()
    while f"def {nom_funcion}" not in linea:
        linea = arch_python.readline()
    return linea

def separar_parametros(linea_codigo):
    """[Autor: Javier Acho]
       [Ayuda: Recibe una cadena que contiene la firma de una función y devuelve
        una cadena con los parámetros formales de la misma, encerrados entre
        paréntesis.]
    """

    desde = linea_codigo.index("(")
    hasta = linea_codigo.index(")")
    return linea_codigo[desde:hasta+1]

def extraer_documentacion(linea_codigo, archivo):
    """[Autor: Javier Acho]
       [Ayuda: Devuelve una cadena que contiene la documentación de una función.
        La descripción se encuentra inmediatamente después de la firma de la
        función, encerrada entre comillas triples.]
    """

    descripcion = ""

    if "\"\"\"" in linea_codigo:
        texto = linea_codigo.replace("\n", " ")    # me va crear un espacio entre cada línea 
        descripcion += texto.replace("\"\"\"", "").lstrip()  # los espacios de la izquierda y las comillas triples no los necesito
        linea = archivo.readline()
        while "\"\"\"" not in linea:
            descripcion += linea.replace("\n", " ").lstrip()  # genero un espacio al fin de línea y quito los espacios de la izquierda
            linea = archivo.readline()
        descripcion += linea.replace("\"\"\"", "").strip()  # las comillas triples, los espacios de la izquierda y derecha no los necesito

    return descripcion

def separar_datos(documentacion):
    """[Autor: Javier Acho]
       [Ayuda: Devuelve una secuencia con los datos de Autor y Ayuda que se
        encuentran en la documentacion que recibe, desconociendo el orden de
        los mismos en la secuencia.]
    """

    cant = documentacion.count("[")
    if cant == 2:
        inicio = documentacion.index("[")
        fin = documentacion.index("]")
        dato_1 = documentacion[inicio:fin+1]

        inicio = documentacion.index("[", fin + 1)
        fin = documentacion.index("]", fin + 1)
        dato_2 = documentacion[inicio:fin+1]

    elif cant == 1:
        inicio = documentacion.index("[")
        fin = documentacion.index("]")
        dato_1 = documentacion[inicio:fin+1]
        dato_2 = ""
    else:
        dato_1 = '[Autor: ausente]'
        dato_2 = documentacion

    return dato_1, dato_2

def ordenar_autor_ayuda(dato1, dato2):
    """[Autor: Javier Acho]
       [Ayuda: Recibe dos cadenas que contienen los datos de autor y ayuda de
        una función, desconociendo el orden de los datos. Devuelve una secuencia
        de dos elementos donde el primero tendra la informacion del autor y el
        segundo la ayuda de una función.]
    """

    if dato2 == "":
        if "Autor" in dato1:
            autor = dato1
            ayuda = "[Ayuda: Ausente]"
        elif "Ayuda" in dato1:
            ayuda = dato1
            autor = "[Autor: Ausente]"
    else:
        if "Autor" in dato1 or "Ayuda" in dato2:
            autor = dato1
            ayuda = dato2
        elif "Ayuda" in dato1 or "Autor" in dato2:
            ayuda = dato1
            autor = dato2

    return autor, ayuda

def obtener_autor_ayuda(manual_funcion):
    """[Autor: Javier Acho]
       [Ayuda: Recibe la documentación de una función y devuelve una secuencia
        de dos elementos, donde el primero corresponde al autor y el segundo al
        manual de uso de la función.]
    """

    if manual_funcion:
        dato_1, dato_2 = separar_datos(manual_funcion)
        autor, manual = ordenar_autor_ayuda(dato_1, dato_2)
    else:
        autor = "[Autor: Ausente]"
        manual = "[Ayuda: Ausente]"

    return autor, manual

def extraer_datos_funcion(modulo_python, linea_actual):
    """[Autor: Javier Acho]
       [Ayuda: Devuelve una estructura de datos que contiene información de la
        función que recibe. La información se extrae del archivo que recibe, a
        partir de una línea del modulo python.
        El archivo debe estar abierto en modo lectura.]
    """

    datos_rutina = {}
    lineas_codigo = []
    lineas_comentarios = []

    param_formales = separar_parametros(linea_actual)
    linea_actual = modulo_python.readline()

    documentacion = extraer_documentacion(linea_actual, modulo_python)
    linea_actual = modulo_python.readline()

    while linea_actual and not linea_actual.startswith("def "):
        if ("#" in linea_actual) and not ("\"#" in linea_actual or "#\"" in linea_actual):
            linea = linea_actual.rstrip("\n")
            resto, caracter, comentario = linea.partition("#")
            lineas_comentarios.append(caracter + comentario)
            if resto.strip():
                lineas_codigo.append(resto.rstrip())
        elif linea_actual.strip():
            lineas_codigo.append(linea_actual.rstrip())
        linea_actual = modulo_python.readline()

    autor, ayuda = obtener_autor_ayuda(documentacion)

    datos_rutina["parametros"] = param_formales
    datos_rutina["instrucciones"] = lineas_codigo
    datos_rutina["autor"] = autor
    datos_rutina["ayuda"] = ayuda
    datos_rutina["comentarios"] = lineas_comentarios

    return datos_rutina, linea_actual

def guardar_datos(arch_programa, nombre_modulo):
    """[Autor: Javier Acho]
       [Ayuda: Devuelve una estructura de datos que contiene información de cada
        una de las funciones que se encuentran en el archivo que recibe.
        El archivo que recibe es un modulo Python, que debe estar abierto en modo
        lectura.]
    """

    # funciones ordenadas por aparición
    funciones = buscar_funciones(arch_programa)
    linea = encontrar_declaracion_funcion(arch_programa, funciones[0])
    datos_modulo = {}

    for rutina in funciones:
        datos_modulo[rutina], linea = extraer_datos_funcion(arch_programa, linea)
        datos_modulo[rutina]["modulo"] = nombre_modulo

    return datos_modulo
