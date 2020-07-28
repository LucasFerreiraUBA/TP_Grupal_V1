def arreglar_csv(x):
    pos = 0
    while pos < len(x):
        while '"' in x[pos][0] and x[pos].count('"') == 1:
            x[pos] = (x[pos] +', ' + x[pos+1]).strip('"')
            del x[pos+1]
        pos+=1
    return x
