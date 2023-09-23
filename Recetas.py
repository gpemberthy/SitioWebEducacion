"""Function printing python version."""
import os
from pathlib import Path
from os import system

mi_ruta = Path(Path.home(), "Documents", "12 - Proyectos", "Recetas")

def contar_recetas(ruta):
    """Function printing python version."""
    contador = 0
    for txt in Path(ruta).glob("**/*.txt"):
        contador += 1
    return contador

def inicio():
    """Function printing python version."""
    system('cls')
    print("*" * 50)
    print("*" * 4 + "  Bienvenido al administrador de recetas  " + "*" * 4)
    print("*" * 50)
    print("\n")
    print(f"Las recetas se encuentran en: {mi_ruta}")
    print(f"La cantidad de recetas es: {contar_recetas(mi_ruta)}")
    eleccion_menu = 'x'

    while not eleccion_menu.isnumeric() or int(eleccion_menu) not in range(1,7):
        print('Elige una opción: ')
        print('''
              [1] Leer receta
              [2] Crear receta nueva
              [3] Crear categoria nueva
              [4] Eliminar receta
              [5] Eliminar categoria
              [6] Salir del programa
              ''')
        eleccion_menu = input('Selección: ')
    return(int(eleccion_menu))

def mostrar_categorias(ruta):
    """Function printing python version."""
    print("Categorias: ")
    ruta_categorias = Path(ruta)
    lista_categorias = []
    contador = 1
    for carpeta in ruta_categorias.iterdir():
        carpeta_str = str(carpeta.name)
        print(f"[{contador}] - {carpeta_str}")
        lista_categorias.append(carpeta)
        contador += 1
    return lista_categorias  

def elegir_categorias(lista):
    """Function printing python version."""
    eleccion_correcta = 'x'
    while not eleccion_correcta.isnumeric() or int(eleccion_correcta) not in range(1,len(lista)+1):
        eleccion_correcta = input('\n Elije una categoria: ')
    return lista[int(eleccion_correcta)-1]

def mostrar_recetas(ruta):
    """Function printing python version."""
    print("Recetas")
    ruta_recetas = Path(ruta)
    lista_recetas = []
    contador = 1

    for receta in ruta_recetas.glob('*.txt'):
        receta_str = str(receta.name)
        print(f"[{contador}] - {receta_str}")
        lista_recetas.append(receta)
        contador += 1
    return lista_recetas

def elegir_recetas(lista):
    """Function printing python version."""
    eleccion_receta = 'x'
    while not eleccion_receta.isnumeric() or int(eleccion_receta) not in range(1,len(lista)+1):
        eleccion_receta = input("\n Elije una receta: ")
    return lista[int(eleccion_receta)-1]

def leer_receta(receta):
    """Function printing python version."""
    print(Path.read_text(receta))

def crear_receta(ruta):
    """Function printing python version."""
    existe = False

    while not existe:
        print("Escribe el nombre de tu receta: ")
        nombre_receta = input() + '.txt'
        print("Escribe tu nueva receta: ")
        contenido_receta = input()
        ruta_nueva = Path(ruta, nombre_receta)
        if not os.path.exists(ruta_nueva):
            Path.write_text(ruta_nueva, contenido_receta)
            print(f"Tu receta {nombre_receta} ha sido creada")
            existe = True
        else:
            print("Lo siento esta receta ya existe")

def crear_categoria(ruta):
    """Function printing python version."""
    existe = False

    while not existe:
        print("Escribe el nombre de la nueva categoria: ")
        nombre_categoria = input()
        ruta_nueva = Path(ruta, nombre_categoria)
        if not os.path.exists(ruta_nueva):
            Path.mkdir(ruta_nueva)
            print(f"Tu nueva categoria {nombre_categoria} ha sido creada")
            existe = True
        else:
            print("Lo siento esta categoria ya existe")

def eliminar_receta(receta):
    """Function printing python version."""
    Path(receta).unlink()
    print(f"La receta {receta.name} ha sido eliminada")

def eliminar_categoria(categoria):
    """Function printing python version."""
    Path(categoria).rmdir()
    print(f"La categoria {categoria.name} ha sido eliminada.")

def volver_inicio():
    """Function printing python version."""
    eleccion_regresar = 'x'

    while eleccion_regresar.lower() != 'v':
        eleccion_regresar = input("\nPresione V para volver al menu: ")

finalizar_programa = False

while not finalizar_programa:

    menu = inicio()

    if menu == 1:
        mis_categorias = mostrar_categorias(mi_ruta)
        mi_categoria = elegir_categorias(mis_categorias)
        mis_recetas = mostrar_recetas(mi_categoria)
        if len(mis_recetas) < 1:
            print("No hay recetas en esta categoria")
        else:
            mi_receta = elegir_recetas(mis_recetas)
            leer_receta(mi_receta)
        volver_inicio()
    elif menu == 2:
        mis_categorias = mostrar_categorias(mi_ruta)
        mi_categoria = elegir_categorias(mis_categorias)
        crear_receta(mi_categoria)
        volver_inicio()
    elif menu == 3:
        crear_categoria(mi_ruta)
        volver_inicio()
    elif menu == 4:
        mis_categorias = mostrar_categorias(mi_ruta)
        mi_categoria = elegir_categorias(mis_categorias)
        mis_recetas = mostrar_recetas(mi_categoria)
        mi_receta = elegir_recetas(mis_recetas)
        eliminar_receta(mi_receta)
        volver_inicio()
    elif menu == 5:
        mis_categorias = mostrar_categorias(mi_ruta)
        mi_categoria = elegir_categorias(mis_categorias)
        eliminar_categoria(mi_categoria)
        volver_inicio()
    elif menu == 6:
        finalizar_programa = True