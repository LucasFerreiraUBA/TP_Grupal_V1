import arreglar
def ordenar_por_autor():
    """
    [Autor: Lucas Ferreira]
    [Ayuda: lee programas.txt, crea un diccionario y lo retorna]
    """
    parte_5 = {}
    f = open('fuente_unico.csv')
    codigo = f.readline().rstrip(',\n').split(',')[3:]
    codigo = len(arreglar.arreglar_csv(codigo))
    c = open('comentarios.csv')
    comentario = c.readline().split(',')[:2]
    parte_5[comentario[1]]={}
    autor= comentario[1]
    codigo_total=0
    parte_5[autor]['lineas_totales']=0
    while comentario != ['']:
        if autor != comentario[1] and comentario[1] not in parte_5:
            parte_5[comentario[1]]={}
            autor= comentario[1]
            codigo_total=0
            parte_5[autor]['lineas_totales']= codigo_total
        autor= comentario[1]
        parte_5[comentario[1]][comentario[0]]=codigo
        codigo_total = parte_5[autor]['lineas_totales']
        codigo_total +=codigo
        parte_5[autor]['lineas_totales']= codigo_total
        codigo = len(arreglar.arreglar_csv(f.readline().rstrip(',\n').split(',')[3:]))
        comentario = c.readline().split(',')[:2]
    parte_5[autor]['lineas_totales']= codigo_total
    #ordena el diccionario agrupando las funciones por autor (y los autores en orden alfabetico)
    parte_5 = sorted(parte_5.items(),key=lambda x:x[1]['lineas_totales'], reverse=True)
    return dict(parte_5)


def crear_archivo(diccionario):
    """
    [Autor: Lucas Ferreira]
    [Ayuda: lee programas.txt, crea un diccionario y lo retorna]
    """
    parte_5 = ''
    for autor in diccionario:
        del diccionario[autor]['lineas_totales']
        for funcion in diccionario[autor]:         
            parte_5 += '{},{},{}\n'.format(autor,funcion,diccionario[autor][funcion])
    with open('parte_5.csv','w') as p:
        p.write(parte_5)


def ejecutar():
    crear_archivo(ordenar_por_autor())
