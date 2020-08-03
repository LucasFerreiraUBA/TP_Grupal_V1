def convertir_a_simples(texto):
    """
    [Autor: Lucas Ferreira]
    [Ayuda: convierte las comillas dobles de strings a comillas simples]

    """
    while '"' in texto:
        texto = texto.replace('"',"'")
    return texto

def envolver_en_comillas(texto):
    """
    [Autor: Lucas Ferreira]
    [Ayuda:envuelve el texto entre comillas dobles, si ya tiene comillas dobles llama a una funcion para convertirlas
    en comillas simples]
    """
    if '"' in texto:
        texto = convertir_a_simples(texto)
    return '"{}"'.format(texto)
print(envolver_en_comillas('"asd"asd,a,s"f"  " "a"'))

def arreglar_csv(x):
    pos = 0
    while pos < len(x):
        if x[pos]:     
            while '"' in x[pos][0] and x[pos].count('"') == 1:
                x[pos] = (x[pos] +', ' + x[pos+1]).strip('"')
                del x[pos+1]
        else:
            del x[pos]
        pos+=1
    return x
"""
EJEMPLO
de arreglar_csv(lista)
lista = ['int("r"istro[2])','"return regi,st,ro[,0]',',registro[1]"','valor','','hola']
lista2 =arreglar_csv(lista)
uno = lista2[0]
dos = lista2[1]
tres= lista2[2]
print(lista2)
"""

