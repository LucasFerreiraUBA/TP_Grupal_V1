import os, modulo1, generador_arbol_invocaciones, merge_total_archivos, An_Reu_Cod, TPG_parte_5, corte_control, crear_arch_datos_funciones, crear_panel_funciones, consulta_de_funciones

def generador_fuente_comentarios():
    """
    [Autor: Lucas Ferreira]
    [Ayuda: Llama a las funciones desde que lee programas txt
            hasta que las convierte en csv]
    """
    programas = modulo1.leer_programas()
    tupla_completa = modulo1.manejar_contenido(programas)
    archivos = modulo1.generar_csv(tupla_completa)
    with open('fuente_unico.csv','w') as f:
        f.write(archivos[0])
    with open('comentarios.csv','w') as c:
        c.write(archivos[1])

def main():
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
        if valor in '1,2,3,4,5,6'.split(','):
            if valor == '1':
                panel_general()
                arch_datos = open("panel_general.csv", "r")
                crear_panel_funciones.mostrar_tabla_funciones(arch_datos)
                arch_datos.close()
                valor = None
            if valor == '2':
                consulta_de_funciones.describir_funciones()
                valor = None
            if valor == '3':
                An_Reu_Cod.reutilizacion_de_codigo()
                valor = None
            if valor == '4':
                generador_arbol_invocaciones.generar_arbol_dependencias()
                valor = None
            if valor == '5':
                TPG_parte_5.ejecutar()
                corte_control.main_control()
                valor = None
            if valor == '6':
                print('''\nEsta opcion eliminara todos los archivos generados por el programa.
Luego, genera los archivos fuente_unico y comentarios que utilizan
los demas modulos. Esto permite analizar distintos programas
sin tener que eliminar los archivos correspondientes a los analisis anteriores.''')
                sn = 'a'
                while sn not in 'sSnN':
                    sn = input('Desea continuar? (S/N) ')
                if sn.lower() == 's':
                    print('\nEliminando...')
                    os.remove("{}\\fuente_unico.csv".format(os.getcwd()))
                    os.remove("{}\\comentarios.csv".format(os.getcwd()))
                    if os.path.isfile("{}\\panel_general.csv".format(os.getcwd())):
                        os.remove("{}\\panel_general.csv".format(os.getcwd()))
                    if os.path.isfile("{}\\analizador.txt".format(os.getcwd())):
                        os.remove("{}\\analizador.txt".format(os.getcwd()))
                    if os.path.isfile("{}\\participacion.txt".format(os.getcwd())):
                        os.remove("{}\\participacion.txt".format(os.getcwd()))
                    if os.path.isfile("{}\\parte_5.csv".format(os.getcwd())):
                        os.remove("{}\\parte_5.csv".format(os.getcwd()))
                    generador_fuente_comentarios()
                    merge_total_archivos.merger()
                    main()
        elif valor not in '0,1,2,3,4,5,6'.split(','):
            print('\nEl valor registrado no es un numero permitido!')
            valor = None
        else:
            print('\nDesea eliminar los archivos generados por nuestro programa? (S/N)')
            print('Esto no eliminara los archivos "fuente_unico" y "comentarios"\n')
            sn = 'a'
            while sn not in 'sSnN':
                sn = input()
            if sn.lower() == 's':
                print('\nEliminando...\n')
                if os.path.isfile("{}\\panel_general.csv".format(os.getcwd())):
                    os.remove("{}\\panel_general.csv".format(os.getcwd()))
                if os.path.isfile("{}\\analizador.txt".format(os.getcwd())):
                    os.remove("{}\\analizador.txt".format(os.getcwd()))
                if os.path.isfile("{}\\participacion.txt".format(os.getcwd())):
                    os.remove("{}\\participacion.txt".format(os.getcwd()))
                if os.path.isfile("{}\\parte_5.csv".format(os.getcwd())):
                    os.remove("{}\\parte_5.csv".format(os.getcwd()))
    
def descripcion_menu():
    """
    [Autor: Lucas M. Diana]
    [Ayuda: Esta funcion contiene las instrucciones de la utilizacion
            del menu principal.]
    """
    print('\nIndique con un numero la funcion del programa que desea ver:')
    print('1. Panel General de Funciones.')
    print('2. Consulta de Funciones.')
    print('3. Analizador de Reutilización de Código.')
    print('4. Árbol de Invocación.')
    print('5. Información por Desarrollador.')
    print('6. Reanalizar los programas.')
    print('0. Cerrar programa.\n')

def panel_general():
    """
    [Autor: Javier Acho]
    [Ayuda: Ejecuta el modulo crear_arch_datos_funciones solo
            si el archivo 'panel_general.csv' no existe]
    """
    if not os.path.isfile("{}\\panel_general.csv".format(os.getcwd())):
        f_error = "AAAAAA"
        arch_funcion_codigo = open("fuente_unico.csv", "r")
        arch_funcion_coment = open("comentarios.csv", "r")
        arch_datos_final = open("panel_general.csv", "w")

        crear_arch_datos_funciones.cargar_datos(arch_funcion_codigo, arch_funcion_coment, arch_datos_final, f_error)

        arch_funcion_codigo.close()
        arch_funcion_coment.close()
        arch_datos_final.close()
        
generador_fuente_comentarios()
merge_total_archivos.merger()
main()
