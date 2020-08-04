import os

def merger():
    programas = []
    programa_num = 0
    with open('programas.txt', encoding='utf-8') as p:
        renglon = None
        while renglon != '':
            renglon = p.readline()
            if renglon != '':
                if '/' in renglon:
                    programas.append(renglon.strip('\n').split('/')[-1])
                else:
                    programas.append(renglon.strip('\n').split('\\')[-1])
            programa_num += 1
    posicion = 0
    fuente_unico = open('fuente_unico.csv','w')
    comentario_unico = open('comentarios.csv','w')
    for prog in programas:
        nombre_modulo = programas[posicion].split('.')[0]
        fuente = open(nombre_modulo+'_fuente_unico.csv','r')
        comentario = open(nombre_modulo+'_comentario.csv','r')
        renglon_fuente = None
        while renglon_fuente != '':
            renglon_fuente = fuente.readline()
            fuente_unico.write(renglon_fuente)
        renglon_comentario = None
        while renglon_comentario != '':
            renglon_comentario = comentario.readline()
            comentario_unico.write(renglon_comentario)
        fuente.close()
        comentario.close()
        os.remove("{}_fuente_unico.csv".format(nombre_modulo))
        os.remove("{}_comentario.csv".format(nombre_modulo))
        posicion += 1
    fuente_unico.close()
    comentario_unico.close()
