"""

[Ayuda:llama a las funciones desde que lee programas txt hasta que las convierte en csv]
[Autor: Lucas Ferreira]
"""
import modulo1
def main():
    programas = modulo1.leer_programas()
    tupla_completa = modulo1.manejar_contenido(programas)
    print(tupla_completa[0])
    archivos = modulo1.generar_csv(tupla_completa)
    with open('fuente_unico.csv','w') as f:
        f.write(archivos[0])
    with open('comentarios.csv','w') as c:
        c.write(archivos[1])
    
main()
