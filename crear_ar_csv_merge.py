from extraer_datos_modulo import guardar_datos
import os
 
def leer_programas():
    """[Autor: Julian Uño]
       [Ayuda: Lee las lineas de las rutas de los modulos y
       devuelve un diccionario como clave el numero del programa, ej: programa0 es linea 1, programa1 es
       linea 2, etc. Y como valor la direccion de cada archivo modulo]
    """
    
    numero = 0     #se refiere al numero de posicion del programa en el diccionario
    diccionario_programas = {}
    renglon = 'z'
    
    with open('programas.txt') as p:
        while renglon:
            renglon = p.readline()
            if renglon:
                diccionario_programas['programa' + str(numero)] = renglon.strip('\n')
                numero += 1
                
    return diccionario_programas

def grabar_registro(archivo, linea):
    """[Autor: Javier Acho]
       [Ayuda: Graba un registro en el archivo que recibe.
        La cadena de caracteres que recibe contiene la información que se escribe
        en el archivo.
        El archivo debe estar abierto en modo escritura.]
    """
 
    archivo.write(f"{linea}\n")

def generar_par_archivos_modulo():
    """[Autor: Julian Uño]
       [Ayuda: Genera para cada modulo del diccionario leer_programas
       los archivos comentarios.csv y fuente.csv ordenados
       alfabeticamente por nombre de funcion. Requiere del metodo
       guardar_datos del modulo extraer_datos_modulo]
    """
    
    diccionario_programas = leer_programas()
    
    for programa in diccionario_programas:
    
        arch_modulo = open(diccionario_programas[programa], "r", encoding = 'utf-8')
        modulo = diccionario_programas[programa]
        if '/' in modulo:
            modulo = modulo.split('/')[-1][:-3]
        else:
            modulo = modulo.split('\\')[-1][:-3]
        datos = guardar_datos(arch_modulo, modulo)
        arch_modulo.close()
        if '/' in modulo:
            arch_codigo = open("fuente_unico_" + modulo.split('/')[-1].split('.')[0]+'.csv', "w")
            arch_comentarios = open("comentarios_"+ modulo.split('/')[-1].split('.')[0]+".csv", "w")
        else:            
            arch_codigo = open("fuente_unico_" + modulo.split('\\')[-1].split('.')[0]+'.csv', "w")
            arch_comentarios = open("comentarios_"+ modulo.split('\\')[-1].split('.')[0]+".csv", "w")
    
        funciones_ordenas = sorted(datos.keys())
    
        for rutina in funciones_ordenas:
        
            parametros = datos[rutina]["parametros"]
            modulo = datos[rutina]["modulo"]
            instrucciones = ",".join(datos[rutina]["instrucciones"])
            registro_codigo = f"{rutina},{parametros},{modulo},{instrucciones}"
            grabar_registro(arch_codigo, registro_codigo)
 
            autor = datos[rutina]["autor"]
            manual = datos[rutina]["ayuda"]
            comentarios = ",".join(datos[rutina]["comentarios"])
            registro_comentario = f"{rutina},{autor},{manual},{comentarios}"
            grabar_registro(arch_comentarios, registro_comentario)
 
        arch_codigo.close()
        arch_comentarios.close()
        
def leer_archivo(archivo):
    """[Autor: Julian Uño]
       [Ayuda: Lee una linea del archivo pasado por parametro y
       si no es vacio, quita el \n y devuelve una lista con dos
       valores separados por la primera coma de dicha linea. sino
       devuelve dos campos vacios.]
    """
    
    linea = archivo.readline()
    
    if linea:
        devolver = linea.rstrip('\n').split(',', 1)
    else:
        devolver = "", ""
        
    return devolver

def grabar_nuevo(archivo, nombre,  demas_campos):
    """[Autor: Julian Uño]
       [Ayuda: Guarda en el archivo pasado por parametro el nombre
       de la funcion mas el resto de la linea que habia sido 
       dividido por leer_archivo(si es que no era vacio)]
    """
    
    archivo.write(nombre + ',' + demas_campos + '\n')

def mezclar_archivos(r_archivo1, r_archivo2, ruta_ar_guardado):
    """[Autor: Julian Uño]
       [Ayuda: Recibe tres nombres de archivos, los dos primeros
       son los generados por la funcion generar_par_archivos_modulo. Ej: comentarios_mod1.csv y 
       comentarios_mod2.csv. Analizará cada linea de cada uno y comparará de 
       acuerdo a un orden lexicográfico cual es mayor igual o menor, para ir guardando en
       el tercer archivo, que se recibió el nombre como parametro ruta_ar_guardado]
    """
    
    ar1 = open(r_archivo1, 'r')
    ar2 = open(r_archivo2, 'r')
    ar_guardado = open(ruta_ar_guardado, 'w')
    
    nombre1, demas_campos1= leer_archivo(ar1)
    nombre2, demas_campos2 = leer_archivo(ar2)
    
    while(nombre1 and nombre2):
        
        if(nombre1 == nombre2):
            
            grabar_nuevo(ar_guardado,nombre1, demas_campos1)
            nombre1, demas_campos1 = leer_archivo(ar1)
            grabar_nuevo(ar_guardado, nombre2, demas_campos2)            
            nombre2, demas_campos2 = leer_archivo(ar2)
            
        elif(nombre1 < nombre2):
            grabar_nuevo(ar_guardado, nombre1, demas_campos1)
            nombre1, demas_campos1 = leer_archivo(ar1)
            
        else:    # nombre1> nombre2
            grabar_nuevo(ar_guardado, nombre2, demas_campos2)
            nombre2, demas_campos2 = leer_archivo(ar2)
            
    while nombre1:
        grabar_nuevo(ar_guardado, nombre1, demas_campos1)
        nombre1, demas_campos1 = leer_archivo(ar1)
        
    while nombre2:
        grabar_nuevo(ar_guardado, nombre2, demas_campos2)
        nombre2, demas_campos2  = leer_archivo(ar2)
        
    ar1.close()
    ar2.close()
    ar_guardado.close()
    
    return ruta_ar_guardado

def cantidad_lineas_programastxt():
    """[Autor: Julian Uño]
       [Ayuda: Cuenta la cantidad de lineas del
       archivo programas.txt y retorna ese valor]
    """
    
    n = 0
    dic_rutas_programas = leer_programas()
    for programa in dic_rutas_programas:
        
        n += 1
        
    return n

def mezclar_nombres(nombre_ar, cadena_modulo1, cadena_modulo2):
    """[Autor: Julian Uño]
       [Ayuda: Mezcla los nombres que se usará en el
       tercer parametro de la funcion mezclar_archivos]
    """
    
    #agarra el nombre por ej de comentario_modulo1 y comentario_modulo2 y genera comantario_modulo1_modulo2
    
    return nombre_ar + cadena_modulo1 + '_' + cadena_modulo2 + '.csv'

def mezcla_de_comentarios():
    """[Autor: Julian Uño]
       [Ayuda: Genera de acuerdo a la cantidad de modulos en programas.txt
       un ciclo hasta terminar de mezclar el archivo final de comentarios.
       No elimina los archivos mezclados intermedios que se utilizaron para generar
       el ultimo archivo comentarios]
    """
    
    diccionario_programas = leer_programas()
    i = 0
    n = cantidad_lineas_programastxt()
    
    while i < (n - 1):

            if n == 2:
                if '/' in diccionario_programas['programa' + str(i)]:
                    modulo1 = diccionario_programas['programa' + str(i)].split('/')[-1][:-3]
                    modulo2 = diccionario_programas['programa' + str(i+1)].split('/')[-1][:-3]
                else:
                    modulo1 = diccionario_programas['programa' + str(i)].split('\\')[-1][:-3]
                    modulo2 = diccionario_programas['programa' + str(i+1)].split('\\')[-1][:-3]
                #ruta_guardado va a ser el nombre del primer archivo de mezcla de los dos primeros modulos
                ruta_guardado = 'comentarios.csv'
                r_mezclado = mezclar_archivos("comentarios_"+ modulo1 + ".csv", "comentarios_" + modulo2 + ".csv", ruta_guardado)
            
            elif i == 0:
                if '/' in diccionario_programas['programa' + str(i)]:
                    modulo1 = diccionario_programas['programa' + str(i)].split('/')[-1][:-3]
                    modulo2 = diccionario_programas['programa' + str(i+1)].split('/')[-1][:-3]
                else:
                    modulo1 = diccionario_programas['programa' + str(i)].split('\\')[-1][:-3]
                    modulo2 = diccionario_programas['programa' + str(i+1)].split('\\')[-1][:-3]
                #ruta_guardado va a ser el nombre del primer archivo de mezcla de los dos primeros modulos
                ruta_guardado = mezclar_nombres("comentarios_", modulo1, modulo2)
                r_mezclado = mezclar_archivos("comentarios_"+ modulo1 + ".csv", "comentarios_" + modulo2 + ".csv", ruta_guardado)
                
            elif i < (n-2):
                if '/' in diccionario_programas['programa' + str(i+1)]:
                    modulo = diccionario_programas['programa' + str(i+1)].split('/')[-1][:-3]
                else:
                    modulo = diccionario_programas['programa' + str(i+1)].split('\\')[-1][:-3]
                ruta_guardado = mezclar_nombres("comentarios_", modulo, r_mezclado[14:-3])
                r_mezclado = mezclar_archivos(r_mezclado, "comentarios_" + modulo + ".csv", ruta_guardado)
                
            else:
                if '/' in diccionario_programas['programa' + str(i+1)]:
                    modulo = diccionario_programas['programa' + str(i+1)].split('/')[-1][:-3]
                else:
                    modulo = diccionario_programas['programa' + str(i+1)].split('\\')[-1][:-3]
                ruta_guardado = 'comentarios.csv'
                r_mezclado = mezclar_archivos(r_mezclado, "comentarios_"+ modulo + ".csv", ruta_guardado)
                
            i += 1

    if n== 2:
        if '/' in diccionario_programas['programa' + str(i)]:
            modulo = diccionario_programas['programa' + str(i)].split('/')[-1][:-3]
        else:
            modulo = diccionario_programas['programa' + str(i)].split('\\')[-1][:-3]
        ruta_guardado = 'comentarios.csv'
        os.rename("comentarios_"+ modulo+".csv", ruta_guardado)

def mezcla_de_lineas_codigo():
    """[Autor: Julian Uño]
       [Ayuda: Genera de acuerdo a la cantidad de modulos en programas.txt
       un ciclo hasta terminar de mezclar el archivo final de fuente_unico.
       No elimina los archivos mezclados intermedios que sirvieron para generar
       el ultimo fuente_unico]
    """
    
    diccionario_programas = leer_programas()
    i = 0
    n = cantidad_lineas_programastxt()
    
    while i < (n - 1):
        
            if n == 2:
                if '/' in diccionario_programas['programa' + str(i)]:
                    modulo1 = diccionario_programas['programa' + str(i)].split('/')[-1][:-3]
                    modulo2 = diccionario_programas['programa' + str(i+1)].split('/')[-1][:-3]
                else:                    
                    modulo1 = diccionario_programas['programa' + str(i)].split('\\')[-1][:-3]
                    modulo2 = diccionario_programas['programa' + str(i+1)].split('\\')[-1][:-3]
                ruta_guardado = 'fuente_unico.csv'
                r_mezclado = mezclar_archivos("fuente_unico_"+ modulo1+".csv", "fuente_unico_" + modulo2 + ".csv",ruta_guardado)
                
            elif i == 0:
                if '/' in diccionario_programas['programa' + str(i)]:
                    modulo1 = diccionario_programas['programa' + str(i)].split('/')[-1][:-3]
                    modulo2 = diccionario_programas['programa' + str(i+1)].split('/')[-1][:-3]
                else:                    
                    modulo1 = diccionario_programas['programa' + str(i)].split('\\')[-1][:-3]
                    modulo2 = diccionario_programas['programa' + str(i+1)].split('\\')[-1][:-3]
                ruta_guardado = mezclar_nombres("fuente_unico_", modulo1, modulo2)
                r_mezclado = mezclar_archivos("fuente_unico_"+ modulo1+".csv", "fuente_unico_" + modulo2 + ".csv",ruta_guardado)
                
            elif i < (n-2):
                if '/' in diccionario_programas['programa' + str(i+1)]:
                    modulo = diccionario_programas['programa' + str(i+1)].split('/')[-1][:-3]
                else:
                    modulo = diccionario_programas['programa' + str(i+1)].split('\\')[-1][:-3]
                ruta_guardado = mezclar_nombres("fuente_unico_", modulo, r_mezclado[14:-3])
                r_mezclado = mezclar_archivos(r_mezclado, "fuente_unico_"+ modulo+".csv", ruta_guardado)

            else:
                if '/' in diccionario_programas['programa' + str(i+1)]:
                    modulo = diccionario_programas['programa' + str(i+1)].split('/')[-1][:-3]
                else:
                    modulo = diccionario_programas['programa' + str(i+1)].split('\\')[-1][:-3]
                ruta_guardado = 'fuente_unico.csv'
                r_mezclado = mezclar_archivos(r_mezclado, "fuente_unico_"+ modulo + ".csv", ruta_guardado)
                
            i += 1

    if n == 2:
        if '/' in diccionario_programas['programa' + str(i)]:
            modulo = diccionario_programas['programa' + str(i)].split('/')[-1][:-3]
        else:
            modulo = diccionario_programas['programa' + str(i)].split('\\')[-1][:-3]
        ruta_guardado = 'fuente_unico.csv'
        os.rename("fuente_unico_"+ modulo+".csv", ruta_guardado)
