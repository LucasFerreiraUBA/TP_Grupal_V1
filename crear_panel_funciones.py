def mostrar_tabla_funciones(arch_datos_funciones):
	"""[Autor: Javier Acho]
	   [Ayuda: Recibe un archivo con extensión csv y muestra por pantalla una
	    tabla con información de cada funcion que se encuentra dentro del
	    archivo.
	    El archivo que recibe debe estar abierto en modo lectura.]
	"""

	for linea in arch_datos_funciones:
		c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13 = \
		linea.rstrip("\n").split(",")

		cadena = "{0:<50s} {1:<11s} {2:<7s} {3:<13s}".format(c1, c2, c3, c4) +\
		         "{0:<8s} {1:<8s} {2:<4s} {3:<6s}".format(c5, c6, c7, c8) +\
		         "{0:<6s}{1:<5s} {2:<7s} {3:<6}".format(c9, c10, c11, c12) +\
		         " {0:<20s}".format(c13)

		print(cadena)

#------------------------------------------------------------------------------
