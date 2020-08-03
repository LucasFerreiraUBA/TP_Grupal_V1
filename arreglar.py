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

lista = ['int("r"istro[2])','"return regi,st,ro[,0]',',registro[1]"','valor','','hola']
lista2 =arreglar_csv(lista)
uno = lista2[0]
dos = lista2[1]
tres= lista2[2]
print(len(lista2))



