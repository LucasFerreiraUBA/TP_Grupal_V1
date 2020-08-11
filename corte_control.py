# constantes 
MAX_AUTOR = "[Autor: zzzzz]"
MAX_LINEA = MAX_AUTOR + ",xxx,999"
ARCHIVO = "parte_5.csv"
# funciones ====================================================
def escribir(leyenda, dato,archivo_nuevo, separador = False,contador_funciones="",porcentaje="",simbolo_porcentaje=""):
    """
    [Autor: Lucas Ferreira]
    [Ayuda: escribe en participacion.txt]
    """
    if len(contador_funciones)==2:      
        archivo_nuevo.write("{0} {1:^38} {2:^5} {3} {4} {5}".format(contador_funciones,leyenda, dato,porcentaje,simbolo_porcentaje,"\n"))
    elif len(contador_funciones)==1:
        archivo_nuevo.write("{0} {1:^39} {2:^5} {3} {4} {5}".format(contador_funciones,leyenda, dato,porcentaje,simbolo_porcentaje,"\n"))
    else:
        archivo_nuevo.write("{0} {1:^40} {2:^5} {3} {4} {5}".format(contador_funciones,leyenda, dato,porcentaje,simbolo_porcentaje,"\n"))
    if (separador):
        guion = "=" * 55
        archivo_nuevo.write("{} {}".format(guion,"\n\n"))
        
#---------------------------------------------------------------------
def imprimir(leyenda, dato, separador = False,contador_funciones="",porcentaje="",simbolo_porcentaje=""):
    """
    [Autor: Lucas Ferreira]
    [Ayuda: imprime por pantalla]
    """
    if len(contador_funciones) == 2:       
        print("{0} {1:^38} {2:^5} {3} {4}".format(contador_funciones,leyenda, dato, porcentaje,simbolo_porcentaje))
    elif len(contador_funciones) ==1:
        print("{0} {1:^39} {2:^5} {3} {4}".format(contador_funciones,leyenda, dato, porcentaje,simbolo_porcentaje))
    else:
        print("{0} {1:^40} {2:^5} {3} {4}".format(contador_funciones,leyenda, dato, porcentaje,simbolo_porcentaje))
    if (separador):
        guion = "=" * 55
        print (guion,"\n")
        
#---------------------------------------------------------------------
def total_funcion(registro, archivo):
    """
    [Autor: Lucas Ferreira]
    [Ayuda: lee programas.txt, crea un diccionario y lo retorna]
    """
    autor, funcion, valor= autor_funcion_valor(registro)
    registro= leer(archivo)    
    return valor, funcion, registro

#---------------------------------------------------------------------
def autor_funcion_valor(registro):
    """
    [Autor: Lucas Ferreira]
    [Ayuda: lee una linea de parte_5.csv y separa los campos segun autor, funcion y valor]
    """
    valor = int(registro[2])
    return registro[0], registro[1], valor
#---------------------------------------------------------------------
def total_autor(registro, archivo,archivo_nuevo):
    """
    [Autor: Lucas Ferreira]
    [Ayuda: --------------]
    """
    autor, funcion, valor = autor_funcion_valor(registro)
    autor_actual = autor
    funcion_actual = funcion
    acumulado_autor   = 0
    contador_funciones=0
    print("{0:^40}{1:^6}".format("Funciones","lineas"))
    archivo_nuevo.write("{0:^40}{1:^6} {2}".format("Funciones","lineas","\n"))
    while (autor == autor_actual and autor < MAX_AUTOR):
        acumulado_funcion, funcion_procesado, registro = total_funcion(registro, archivo)
        leyenda = "  " + funcion_procesado + " - "
        imprimir(leyenda, acumulado_funcion)
        escribir(leyenda, acumulado_funcion,archivo_nuevo) 
        acumulado_autor  += acumulado_funcion
        contador_funciones+=1
        autor = registro[0]
        
    return acumulado_autor, registro, contador_funciones

#---------------------------------------------------------------------

def leer(archivo):
    """
    [Autor: Lucas Ferreira]
    [Ayuda: lee programas.txt, crea un diccionario y lo retorna]
    """
    linea = archivo.readline()
    if (not(linea)):
        linea = MAX_LINEA
    linea = linea.rstrip()
    return linea.split(",")
#---------------------------------------------------------------------
def corte_control(archivo,archivo_nuevo):
    """
    [Autor: Lucas Ferreira]
    [Ayuda: --------------]
    """
    # Leo cada una de las lineas
    registro = leer(archivo)
    acumulado_total = 0

    while (registro[0] < MAX_AUTOR):
        print(registro[0]+"\n")
        archivo_nuevo.write(registro[0]+"\n\n")
        acumulado_autor, registro , contador_funciones= total_autor(registro, archivo,archivo_nuevo)
        acumulado_total += acumulado_autor
        imprimir("Funciones - lineas: ", acumulado_autor,True,str(contador_funciones),str(round(acumulado_autor/contar_total()*100,2)),"%")
        escribir("Funciones - lineas: ", acumulado_autor,archivo_nuevo, True,str(contador_funciones),str(round(acumulado_autor/contar_total()*100,2)),"%")
        

    imprimir("\n Funciones - lineas: ", acumulado_total)
    escribir("\n Funciones - lineas: ", acumulado_total,archivo_nuevo)

#### =================================================

def contar_total():
    """
    [Autor: Lucas Ferreira]
    [Ayuda: --------------]
    """
    with open(ARCHIVO,"r") as a:
        cantidad = 0
        linea = a.readline().split(",")[2]
        while linea:
            cantidad += int(linea)
            try:
                linea = a.readline().split(",")[2]
            except IndexError:
                linea = ""
    return cantidad

### =================================================

def main_control():
    """
    [Autor: Lucas Ferreira]
    [Ayuda: --------------]
    """
    # Abro archivo para lectura
    archivo = open(ARCHIVO,"r")
    archivo_nuevo = open("participacion.txt","w")
    contar_total()
    corte_control(archivo,archivo_nuevo)
    archivo.close()
    archivo_nuevo.close()
