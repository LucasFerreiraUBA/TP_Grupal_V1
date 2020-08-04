from extraer_datos_funciones import guardar_datos

# se va obtener los archivos fuente_unico_A.csv y comentarios_A.csv del modulo lib_matematica.py

arch_modulo = open("lib_matematica.py", "r")
datos = guardar_datos(arch_modulo, "lib_matematica")
arch_modulo.close()

def grabar_registro(archivo, linea):
    """[Autor: Javier Acho]
       [Ayuda: Graba un registro en el archivo que recibe.
        La cadena de caracteres que recibe contiene la información que se escribe
        en el archivo.
        El archivo debe estar abierto en modo escritura.]
    """

    archivo.write(f"{linea}\n")

arch_codigo = open("fuente_unico_A.csv", "w")
arch_comentarios = open("comentarios_A.csv", "w")

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