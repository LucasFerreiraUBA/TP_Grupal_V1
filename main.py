import os, crear_ar_csv_merge, generador_arbol_invocaciones, TPG_parte_5, An_Reu_Cod, corte_control, crear_arch_panel_gral, crear_panel_funciones, consulta_de_funciones

def borrar_archivos():
    """
    [Autor: Lucas M. Diana]
    [Ayuda: Esta funcion elimina los archivos creados por el programa.]
    """
    print('\nEliminando...\n')
    if os.path.isfile("panel_general.csv"):
        os.remove("panel_general.csv")
    if os.path.isfile("analizador.txt"):
        os.remove("analizador.txt")
    if os.path.isfile("participacion.txt"):
        os.remove("participacion.txt")
    if os.path.isfile("parte_5.csv"):
        os.remove("parte_5.csv")
    if os.path.isfile("ayuda_funciones.txt"):
        os.remove("ayuda_funciones.txt")
    if os.path.isfile("ayuda_funciones.txt"):
        os.remove("ayuda_funciones.txt")

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
                TPG_parte_5.crear_archivo(TPG_parte_5.ordenar_por_autor())
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
                    borrar_archivos()
                    os.remove("fuente_unico.csv".format(os.getcwd()))
                    os.remove("comentarios.csv".format(os.getcwd()))
                    crear_ar_csv_merge.generar_par_archivos_modulo()
                    crear_ar_csv_merge.mezcla_de_lineas_codigo()
                    crear_ar_csv_merge.mezcla_de_comentarios()
                    limpieza()
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
                borrar_archivos()
    
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
    if not os.path.isfile("panel_general.csv".format(os.getcwd())):
        f_error = "AAAAAA"
        arch_funcion_codigo = open("fuente_unico.csv", "r")
        arch_funcion_coment = open("comentarios.csv", "r")
        arch_datos_final = open("panel_general.csv", "w")

        crear_arch_panel_gral.cargar_datos(arch_funcion_codigo, arch_funcion_coment, arch_datos_final, f_error)

        arch_funcion_codigo.close()
        arch_funcion_coment.close()
        arch_datos_final.close()

def limpieza():
    """
    [Autor: Lucas M. Diana]
    [Ayuda: Elimina todos los archivos intermedios utilizados para crear
            el fuente_unico y comentarios]
    """
    tipo_de_limp = ['fuente_unico_','comentarios_']
    lista_directorio = os.listdir()
    for archivo in lista_directorio:
        if archivo.startswith(tipo_de_limp[0]) or archivo.startswith(tipo_de_limp[1]):
            os.remove(archivo)

if os.path.exists('fuente_unico.csv'):
    os.remove('fuente_unico.csv')
if os.path.exists('comentarios.csv'):
    os.remove('comentarios.csv')
crear_ar_csv_merge.generar_par_archivos_modulo()
crear_ar_csv_merge.mezcla_de_lineas_codigo()
crear_ar_csv_merge.mezcla_de_comentarios()
limpieza()
main()
