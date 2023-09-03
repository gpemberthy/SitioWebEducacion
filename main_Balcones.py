from tkinter import *
from tkinter import messagebox, ttk, filedialog
from pymongo import MongoClient

#definicion de la ventana principal
raiz = Tk()
#definición del menu de la aplicación
var_nombres = StringVar
residentes=[]
proyecto = 0
#Esto es temporal mientras realizo la consulta a mongo para traer el valor de las casas. 
casas = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14']

raiz.title("Balcones de Capellania")
raiz.geometry("650x400")
barra_menu = Menu(raiz)
menuPersonas = Menu(barra_menu, tearoff=0)
menuProyectos = Menu(barra_menu, tearoff=0)
menuConfiguracion = Menu(barra_menu, tearoff=0)
#Componentes del menu
barra_menu.add_cascade(label="Personas", menu=menuPersonas)
barra_menu.add_cascade(label="Proyectos", menu=menuProyectos)
barra_menu.add_cascade(label="Configuracion", menu=menuConfiguracion)
menuProyectos.add_command(label="Crear Proyecto")
raiz.config(menu=barra_menu)
frame4 = LabelFrame(raiz, text=" CUADRO PRINCIPAL ")
frame4.grid(row=0, column=1, rowspan=3)
frame4.config(width=340, height=370)

def conexion_mongo():
    """Funcion que brinda la conexion con la BD Mongo"""
    #Apertura de la conexión con la BD de Mongo
    cliente = MongoClient('mongodb://localhost:27017/')
    #La Base de Datos se llama Balcones
    db = cliente.Balcones
    return db

def pagos():
    """Funcion para gestionar los pagos"""
    ventana_emergente_pagos = Toplevel()
    ventana_emergente_pagos.title("  Ventana Pagos  ")
    
    frameb = LabelFrame(ventana_emergente_pagos, text="Registro de pagos Balcones")
    frameb.grid(row=0, column=0, pady=5)
    #frame.grid(row=0, column=0, columnspan=2, pady=5)

    Label(frameb, text="Nombres").grid(row=1, column=0)
    nombre = Entry(frameb)
    nombre.grid(row=1, column=1)
    nombre.focus()
    
    Label(frameb, text="Apellidos").grid(row=2,column=0)
    apellidos = Entry(frameb)
    apellidos.grid(row=2, column=1)

    Button(ventana_emergente_pagos, text="Guardar").grid(row=3, column=0, sticky= W+E)

    #Tabla
    miArbol = ttk.Treeview(ventana_emergente_pagos, height=10, columns=2)
    miArbol.grid(row=4, column=0)
    miArbol.heading("#0", text="Nombre")
    miArbol.heading("#1", text="Pagos")

def pagos2():
    """Funcion para gestionar los pagos"""
    ventana_emergente_pagos = Toplevel()
    ventana_emergente_pagos.title("  Ventana Pagos  ")
    
    frameb = LabelFrame(ventana_emergente_pagos, text="Registro de pagos Balcones")
    frameb.grid(row=0, column=0, pady=5)
    #frame.grid(row=0, column=0, columnspan=2, pady=5)

    Label(frameb, text="Nombres").grid(row=1, column=0)
    nombre = Entry(frameb)
    nombre.grid(row=1, column=1)
    nombre.focus()
    
    Label(frameb, text="Apellidos").grid(row=2,column=0)
    apellidos = Entry(frameb)
    apellidos.grid(row=2, column=1)

    Button(ventana_emergente_pagos, text="Guardar").grid(row=3, column=0, sticky= W+E)

    #Tabla
    miArbol = ttk.Treeview(ventana_emergente_pagos, height=10, columns=2)
    miArbol.grid(row=4, column=0)
    miArbol.heading("#0", text="Nombre")
    miArbol.heading("#1", text="Pagos")

def menu_pagos():
    """Metodo que ejecuta la pantalla principal"""
    frame = LabelFrame(raiz, text="  Modulo Pagos   ")
    frame.config(width=100, height=100, bg="red")
    frame.grid(row=0, column=0, padx=15, pady=10)
    #  -- Pagos  --
    #Label(frame, text="Registrar Pagos").grid(row=1, column=0)
    boton1 = Button(frame, text="Registrar Pagos", 
           width=15, command=pagos)
    boton1.grid(row=2, column=0, sticky= W+E, padx=5, pady=5)
    boton1.config(fg='black', bg='#158645', cursor='hand2', activebackground='yellow')

    #Label(frame, text="Consultar Pagos").grid(row=3, column=0)
    Button(frame,text="Consultar Pagos", command=pagos2).grid(row=4, columnspan=2, padx= 5, pady=5, sticky= W+E)

def guardar_persona(combo_casas, nombre, apellido): 
    """Funcion que me permite guardar en la BD la persona"""
    val=combo_casas.get()
    print(nombre)
    db = conexion_mongo()
    collection_personas = db.Personas
    collection_personas.insert_one({'Telefono':{'Activo': '3013025888'},
                                    'Casa': val, 
                                    'Estado': 'Activo',
                                    'Tipo': 'Propietario',
                                    'Identificacion': {
                                               'Tipo': "CC",
                                                'Numero': 10236589
                                            },
                                    'correos': {'Activo': "perro@loquesea.net"},
                                    'Personas': {'Nombres': nombre,
                                                 'Apellidos': apellido} 
                                        })
  
def ventana_personas():
    """Funcion para gestionar las personas"""
    
    ventana_emergente_pagos = Toplevel()
    ventana_emergente_pagos.title("  Ventanas Personas  ")
    
    frameb = LabelFrame(ventana_emergente_pagos, text="  Registro de personas  ")
    frameb.grid(row=0, column=0, pady=5)
    #frame.grid(row=0, column=0, columnspan=2, pady=5)

    Label(frameb, text="Nombres").grid(row=1, column=0, padx=5, pady=5)
    nombre = Entry(frameb)
    nombre.grid(row=1, column=1)
    nombre.focus()
    minombre = nombre.get()
    
    Label(frameb, text="Apellidos").grid(row=2,column=0, padx=5, pady=5)
    apellidos = Entry(frameb)
    apellidos.grid(row=2, column=1)

    Label(frameb, text="Casa: ").grid(row=3,column=0, padx=5, pady=5)
    combo_casas = ttk.Combobox(frameb, values=casas, width=5)
    combo_casas.grid(row=3, column=1)

    Button(ventana_emergente_pagos, text="Guardar", 
           command= lambda: guardar_persona(combo_casas, nombre.get(), apellidos.get())).grid(row=4, column=0, sticky= W+E)

    #Tabla
    miArbol = ttk.Treeview(ventana_emergente_pagos, height=10, columns=2)
    miArbol.grid(row=6, column=0)
    miArbol.heading("#0", text="Nombre")
    miArbol.heading("#1", text="Pagos")

def consulta_residente(event, combo_casa):
    """Funcion para la consulta de residentes"""
    seleccion = combo_casa.get()
    db = conexion_mongo()
    collection_personas = db.Personas
    for document in collection_personas.find({'Casa': seleccion}):
        if document['Estado'] == 'Activo':
            residentes.append(document['Tipo'])
            residentes.append(document['Estado'])
            residentes.append(document['Telefono']['Activo'])
            residentes.append(document['Personas']['Nombres'])
            residentes.append(document['Personas']['Apellidos'])
            residentes.append(document['Identificacion']['Tipo'])
            residentes.append(document['Identificacion']['Numero'])

def llenar_tabla(miArbol):
    print("in llenar_tabla")
    print(residentes)
    if len(residentes) > 0:
        miArbol.insert('', 0, text=0, values=(residentes[4], residentes[3]))
    print("out llenar_tabla")

def actualizar_residente():
    for widget in frame4.winfo_children():
        widget.destroy()
    
    Label(frame4, text="Casa: ").grid(row=0, column=0)
    combo_casa = ttk.Combobox(frame4, values=casas)
    combo_casa.grid(row=0, column=1)
    combo_casa.config(width=7)
    combo_casa.bind("<<ComboboxSelected>>", lambda event: consulta_residente(event, combo_casa))

    #Tabla
    miArbol = ttk.Treeview(frame4, height=10, columns=3)
    miArbol.grid(row=3, column=0, columnspan=3)
    miArbol.heading("#0", text="Nombre")
    miArbol.heading("#1", text="Apellidos")
    miArbol.heading("#2", text="identificacion")
    if len(residentes) > 0:
        llenar_tabla(miArbol)

    mi_boton1 = Button(frame4, text="Consultar", command= lambda: llenar_tabla(miArbol))
    mi_boton1.grid(row=0, column=2)

def menu_personas():
    """Metodo que ejecuta la pantalla de personas """
    frame2 = LabelFrame(raiz, text="   * Modulo Residentes *   ")
    frame2.config(width=100, height=100, bg="blue")
    frame2.grid(row=1, column=0, padx=10, pady=5)
    #  -- Pagos  --
    #Label(frame2, text="Registrar Persona").grid(row=1, column=0)

    Button(frame2, text="Registrar Residente", width=15, 
           command=ventana_personas).grid(row=0, column=0, sticky= W+E, padx=5, pady=5)

    #Label(frame2, text="Consultar Persona").grid(row=3, column=0)
    Button(frame2,text="Consultar Residente").grid(row=1, columnspan=2, padx= 5, pady=5, sticky= W+E)

    Button(frame2,text="Actualizar Residente", command=actualizar_residente).grid(row=2, columnspan=2, padx= 5, pady=5, sticky= W+E)

def crear_proyecto():
    """Funcion para crear proyectos"""
    for widget in frame4.winfo_children():
        widget.destroy()
    #for child in raiz.winfo_children():
    #    print(child)

    Label(frame4, text="Crear un proyecto").grid(row=0, column=0)
    Button(frame4, text="prueba").grid(row=0, column=1)

def consultar_proyecto():
    for widget in frame4.winfo_children():
        widget.destroy()
    Label(frame4, text="Registrar un proyecto").grid(row=0, column=0)
    Button(frame4, text="prueba").grid(row=0, column=1)

def registrar_proyecto():
    for widget in frame4.winfo_children():
        widget.destroy()
    
    Label(frame4, text="Espacio para registrar todos los movimientos de un proyecto").grid(row=0, column=0)
    Button(frame4, text="prueba").grid(row=1, column=1)

def menu_proyectos():
    """Metodo que ejecuta la pantalla principal"""
    frame3 = LabelFrame(raiz, text="  Modulo Proyectos   ")
    frame3.config(width=100, height=100, bg="green")
    frame3.grid(row=2, column=0, padx=10, pady=10)
    #  -- Proyectos  --

    Button(frame3, text="Crear Proyecto", width=15, 
           command=crear_proyecto).grid(row=0, column=0, sticky= W+E, padx=5, pady=5)
    
    Button(frame3, text="Registrar Proyecto", width=15, 
           command=registrar_proyecto).grid(row=1, column=0, sticky= W+E, padx=5, pady=5)
    
    Button(frame3,text="Consultar Proyecto", 
           command=consultar_proyecto).grid(row=4, columnspan=2, padx= 5, pady=5, sticky= W+E)
    
menu_pagos()

menu_personas()

menu_proyectos()

raiz.mainloop()