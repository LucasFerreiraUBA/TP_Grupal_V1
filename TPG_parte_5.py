def ordenar_por_autor():
    """
    [Autor: Lucas Ferreira]
    [Ayuda: lee fuente_unico.csv y comentarios.csv, de estos dos archivos proceso los datos que necesito
     para crea un diccionario de diccionarios.
     La primera clave es el nombre del autor y el valor
     es otro diccionario que tiene como clave el nombre de la funcion y el valor la cantidad de lineas de codigo
     de esa misma funcion, agregando otra clave por autor que se llama lineas totales y tiene
     como valor la cantidad de lineas totales por autory lo retorna]
    """
    parte_5 = {}
    f = open("fuente_unico.csv")
    linea = f.readline()
    nom_funcion, resto_linea = linea.split(",", 1)
    param_form, resto_linea = resto_linea.split("),", 1)
    nom_modulo, resto_linea = resto_linea.split(",", 1)
    instrucciones= resto_linea.rstrip("\n").split("," + "    ")
    codigo = len(instrucciones)
    c = open("comentarios.csv")
    comentario = c.readline().split(",")[:2]
    parte_5[comentario[1]]={}
    autor= comentario[1]
    codigo_total=0
    parte_5[autor]["lineas_totales"]=0
    while comentario != [""]:
        if autor != comentario[1] and comentario[1] not in parte_5:
            parte_5[comentario[1]]={}
            autor= comentario[1]
            codigo_total=0
            parte_5[autor]["lineas_totales"]= codigo_total
        autor= comentario[1]
        parte_5[comentario[1]][comentario[0]]=codigo
        codigo_total = parte_5[autor]["lineas_totales"]
        codigo_total +=codigo
        parte_5[autor]["lineas_totales"]= codigo_total
        linea = f.readline()
        if linea:
            nom_funcion, resto_linea = linea.split(",", 1)
            param_form, resto_linea = resto_linea.split("),", 1)
            nom_modulo, resto_linea = resto_linea.split(",", 1)
            instrucciones= resto_linea.rstrip("\n").split("," + "    ")
            codigo = len(instrucciones)
        comentario = c.readline().split(",")[:2]
    parte_5[autor]["lineas_totales"]= codigo_total
    #ordena el diccionario agrupando las funciones por autor (y los autores en orden alfabetico)
    parte_5 = sorted(parte_5.items(),key=lambda x:x[1]["lineas_totales"], reverse=True)
    return dict(parte_5)


def crear_archivo(diccionario):
    """
    [Autor: Lucas Ferreira]
    [Ayuda: lee el diccionario generado en ordenar_por_autor() e imprime en un archivo csv nuevo llamado parte_5 que tiene
    como campos el autor, nombre de la funcion y cantidad de lineas de codigo de la misma]
    """
    parte_5 = ""
    for autor in diccionario:
        del diccionario[autor]["lineas_totales"]
        for funcion in diccionario[autor]:         
            parte_5 += "{},{},{}\n".format(autor,funcion,diccionario[autor][funcion])
    with open("parte_5.csv","w") as p:
        p.write(parte_5)
