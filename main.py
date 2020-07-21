"""

[Ayuda:llama a las funciones desde que lee programas txt hasta que las convierte en csv]
[Autor: Lucas Ferreira]
"""
import modulo1, An_Reu_Cod

def main():
    programas = modulo1.leer_programas()
    tupla_completa = modulo1.manejar_contenido(programas)
    print(tupla_completa[0])
    archivos = modulo1.generar_csv(tupla_completa)
    with open('fuente_unico.csv','w') as f:
        f.write(archivos[0])
    with open('comentarios.csv','w') as c:
        c.write(archivos[1])

def menu():
    """
    [Autor: Lucas M. Diana]
    [Ayuda: Muestra un menu y espera a la instruccion del usuario.
            La instruccion enviara al usuario al modulo del programa
            que solicite.
            En caso de elegir cerrar el programa, este finalizara.]
    """
    valor = None
    while valor == None:
        descripcion_menu()
        valor = input()
        if valor in '1,2,3,4,5'.split(','):
            """if valor == '1':
                modulo 1
                valor = None
            if valor == '2':
                modulo 2
                valor = None"""
            if valor == '3':
                An_Reu_Cod.reutilizacion_de_codigo()
                valor = None
            """if valor == '4':
                modulo 4
                valor = None
            if valor == '5':
                modulo 5
                valor = None"""
        elif valor not in '0,1,2,3,4,5'.split(','):
            print('\nEl valor registrado no es un numero!')
            valor = None
    
def descripcion_menu():
    """
    [Autor: Lucas M. Diana]
    [Ayuda: Esta funcion contiene las instrucciones de la utilizacion
            del menu principal.]
    """
    print('\nIndique con un numero la funcion del programa que desea ver:')
    print('1. Panel General de Funciones')
    print('2. Consulta de Funciones')
    print('3. Analizador de Reutilización de Código')
    print('4. Árbol de Invocación')
    print('5. Información por Desarrollador')
    print('0. Cerrar programa')

main()
menu()
