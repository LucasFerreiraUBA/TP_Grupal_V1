from extraer_datos_funciones import guardar_datos
 
def leer_programas():
    
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
    
    linea = archivo.readline()
    
    if linea:
        devolver = linea.rstrip('\n').split(',', 1)
    else:
        devolver = "", ""
        
    return devolver

def grabar_nuevo(archivo, nombre,  demas_campos):
    
    archivo.write(nombre + ',' + demas_campos + '\n')

def mezclar_archivos(r_archivo1, r_archivo2, ruta_ar_guardado):
    
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
    
    n = 0
    dic_rutas_programas = leer_programas()
    for programa in dic_rutas_programas:
        
        n += 1
        
    return n

def mezclar_nombres(nombre_ar, cadena_modulo1, cadena_modulo2):
    #agarra el nombre por ej de comentario_modulo1 y comentario_modulo2 y genera comantario_modulo1_modulo2
    
    return nombre_ar + cadena_modulo1 + '_' + cadena_modulo2 + '.csv'

def mezcla_de_comentarios():
    """
        iteracion de los n-1 archivos
    """
    
    diccionario_programas = leer_programas()
    i = 0
    n = cantidad_lineas_programastxt()
    
    while i < (n - 1):
            
            if i == 0:
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

def mezcla_de_lineas_codigo():
    """
        iteracion de los n-1 archivos
    """
    
    diccionario_programas = leer_programas()
    i = 0
    n = cantidad_lineas_programastxt()
    
    while i < (n - 1):
            
            if i == 0:
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
                r_mezclado = mezclar_archivos(r_mezclado, "fuente_unico_"+ modulo+".csv", ruta_guardado)
                
            i += 1
