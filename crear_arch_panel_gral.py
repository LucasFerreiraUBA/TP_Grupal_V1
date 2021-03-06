from crear_ar_csv_merge import grabar_registro

def leer_registro(archivo, fin_arch):
    """[Autor: Javier Acho]
       [Ayuda: Devuelve una cadena que contiene un registro leído del archivo
        que recibe por parámetro.
        Cuando llega al final del archivo devuelve la cadena fin_arch.
        El archivo debe estar abierto en modo lectura.
        La cadena fin_arch, que recibe por parámetro, debe tener tres
        caracteres coma.]
    """

    linea = archivo.readline()
    return linea.rstrip("\n") if linea else fin_arch

def procesar_codigo(registro, fin_arch):
    """[Autor: Javier Acho]
       [Ayuda: Recibe un registro con el siguiente formato:
        <nombre_función>,<parámetros>,<nombre_modulo>,<instrucciones>
        y devuelve una secuencia de cuatro elemenos.
        Cada elemento contiene la información de cada uno de los campos del
        registro.]
    """

    if registro != fin_arch:
        # separo el registro por partes, de a un corte por vez
        nom_funcion, resto_registro = registro.split(",", 1)

        # el campo <parámetros> puede tener comas. Al final del campo tiene los
        # caracteres '),'
        param_form, resto_registro = resto_registro.split("),", 1)
        # el formato de param_form debe ser: (<param1>, ..., <parm_n>) o ()
        param_form += ")"

        nom_modulo, resto_registro = resto_registro.split(",", 1)

        # en esta linea, resto_registro debe tener solo líneas de codigo
        ordenes = resto_registro

    else:
        nom_funcion, param_form, nom_modulo, ordenes = fin_arch.split(",")

    return nom_funcion, param_form, nom_modulo, ordenes


def procesar_comentarios(registro, fin_arch):
    """[Autor: Javier Acho]
       [Ayuda: Recibe un registro con el siguiente formato:
        <nombre_función>,<nombre_autor>,<descripcion_funcion>,<comentarios>
        y devuelve una secuencia de cuatro elemenos.
        Cada elemento contiene la información de cada uno de los campos del
        registro.]
    """

    if registro != fin_arch:
        # el campo <nombre_funcion> y <nombre_autor> no tienen caracteres
        # coma, los otros dos campos pueden tener comas
        nom_funcion, nom_autor, resto_registro = registro.split(",", 2)
        # el campo <descripción_función> finalia con los caracteres "]," 
        descripcion, comentarios = resto_registro.split(",", 1)
        descripcion += "]"

    else:
        nom_funcion, nom_autor, descripcion, comentarios = fin_arch.split(",")

    return nom_funcion, nom_autor, descripcion, comentarios

def contar_parametros(cadena_parametros):
    """[Autor: Javier Acho]
       [Ayuda: Recibe una cadena de caracteres que contiene parámetros separados
        por coma, y devuelve la cantidad de los mismos.
        La cadena_parametros se encuentra dentro de paréntesis.]
    """

    parametros_vacios = ("()", "( )")
    if cadena_parametros in parametros_vacios:
        cantidad = 0
    else:
        cantidad = len(cadena_parametros.strip("()").split(","))

    return cantidad

def contar_sentencias(cadena_ordenes):
    """[Autor: Javier Acho]
       [Ayuda: Recibe una cadena que contiene instrucciones de una función
        separadas por coma.
        Devuelve la cantidad de líneas que contiene la cadena y la cantidad de
        apariciones de las siguientes sentencias: return, if/elif, for, while,
        break.]
    """

    # instrucciones contiene cada una de las lineas de código
    instrucciones = cadena_ordenes.rstrip("\n").split("," + "    ")

    cant_lineas = cant_retorno = cant_condicionales = cant_mientras = \
    cant_para = cant_romper = cant_salida = 0

    # las líneas de código no contienen espacios en blanco luego del último caracter de código
    for linea_codigo in instrucciones:
        linea_codigo = linea_codigo.lstrip()
        cant_lineas += 1

        if linea_codigo.endswith(":"):

            if linea_codigo.startswith("if ") or linea_codigo.startswith("elif "):
                cant_condicionales += 1
            elif linea_codigo.startswith("for "):
                cant_para += 1
            elif linea_codigo.startswith("while "):
                cant_mientras += 1

        elif linea_codigo.startswith("return ") and "if " in linea_codigo: # retorno if corto
            cant_retorno += 1
            cant_condicionales += 1

        elif linea_codigo.startswith("return "):
            cant_retorno += 1

        elif "break" in linea_codigo:
            cant_romper += 1

        elif "exit()" in linea_codigo:
            cant_salida += 1

    return cant_lineas, cant_condicionales, cant_para, cant_mientras, \
    cant_romper, cant_retorno, cant_salida

def contar_comentarios(anotaciones):
    """[Autor: Javier Acho]
       [Ayuda: Devuelve la cantidad de comentarios que se encuentran en la
        cadena que recibe por parámetro.
        Las líneas de comentarios se encuentran separadas por comas.]
    """

    if not anotaciones:
        cantidad = 0
    else:
        cantidad = len(anotaciones.rstrip("\n").split(",#"))

    return cantidad

def extraer_autor(datos_autor):
    """[Autor: Javier Acho]
       [Ayuda: Recibe una cadena que contiene el nombre del autor encerrado
        entre corchetes y con la etiqueta Autor.
        Extrae el nombre y lo devuelve.]
    """

    # formato datos_autor: [Autor: <nombre_apellido>]
    # En caso de no tener auto: [Autor: Ausente]
    residuo, nombre = datos_autor.split(":")
    return nombre.strip("] ")

def separar_datos(arch_fuente):
    """[Autor: Javier Acho]
       [Ayuda: Devuelve una secuencia de dos elementos donde el primero contiene
        una estructura con los nombres de las funciones y el segundo elemento
        una secuencia con los bloques de instrucciones de cada función en el
        archivo.
        El archivo csv que recibe debe estar abierto en modo lectura.]
    """

    datos_invoc = {}
    bloques_codigo = []
    for registro in arch_fuente:
        nomb_funcion, resto = registro.split(",", 1)
        resto, instrucciones = resto.split(",", 1)
        datos_invoc[nomb_funcion] = 0
        bloques_codigo.append(instrucciones)

    arch_fuente.seek(0)
    return datos_invoc, bloques_codigo

def contar_invocaciones(arch_datos):
    """[Autor: Javier Acho]
       [Ayuda: Devuelve una estructura de datos que contiene la cantidad de
        invocaciones de las funciones en los bloques de código del archivo que
        recibe.]
    """

    datos_invoc, bloques_instrucciones = separar_datos(arch_datos)

    for lineas_codigo in bloques_instrucciones:
        for funcion in datos_invoc:
            cant = lineas_codigo.count(funcion + "(")
            datos_invoc[funcion] += cant

    return datos_invoc

def cargar_datos(arch_codigo, arch_comentarios, arch_reporte, ultimo):
    """[Autor: Javier Acho]
       [Ayuda: Se extraen datos de arch_codigo y arch_comentarios, y se cargan
        en arch_reporte.
        Los arch_codigo y arch_comentarios tienen extension csv y están
        ordenados alfabéticamente por el primer campo. Ambos deben estar
        abiertos en modo lectura.
        El arch_reporte debe estar abierto en modo escritura y estará ordenado
        alfabéticamente por el primer campo.]
    """

    final = ultimo + ",,,"
    datos_invocaciones = contar_invocaciones(arch_codigo)

    reg_codigo = leer_registro(arch_codigo, final)
    reg_coment = leer_registro(arch_comentarios, final)

    funcion_cod, param, modulo, instruc = procesar_codigo(reg_codigo, final)
    funcion_com, autor, manual, coment = procesar_comentarios(reg_coment, final)

    nuevo_registro = "FUNCIÓN,Parámetros,Líneas,Invocaciones,Returns,If/elif,"\
                     "For,While,Break,Exit,Coment,Ayuda,Autor"

    grabar_registro(arch_reporte, nuevo_registro)

    # ambos archivos tienen los mismos nombres de funcion por linea
    while funcion_cod != ultimo and funcion_com != ultimo:
        # se utiliza los datos de arch_codigo
        funcion_rep = f"{funcion_cod}.{modulo}"
        cant_param = contar_parametros(param)
        cant_lineas, cant_if_elif, cant_for, cant_while, cant_romper, \
        cant_return, cant_exit = contar_sentencias(instruc)
        cant_invoc = datos_invocaciones[funcion_cod]
        
        # se utiliza los datos de arch_comentarios
        cant_comentarios = contar_comentarios(coment)
        nombre_autor = extraer_autor(autor)
        ayuda = "No" if "Ausente" in nombre_autor else "Si"

        nuevo_registro = f"{funcion_rep},{cant_param},{cant_lineas},{cant_invoc}"\
                         f",{cant_return},{cant_if_elif},{cant_for},{cant_while}"\
                         f",{cant_romper},{cant_exit},{cant_comentarios},{ayuda}"\
                         f",{nombre_autor}"

        grabar_registro(arch_reporte, nuevo_registro)

        reg_codigo = leer_registro(arch_codigo, final)
        reg_coment = leer_registro(arch_comentarios, final)

        funcion_cod, param, modulo, instruc = procesar_codigo(reg_codigo, final)
        funcion_com, autor, manual, coment = procesar_comentarios(reg_coment, final)
