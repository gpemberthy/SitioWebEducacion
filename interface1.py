import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from pymongo import MongoClient

#Apertura de la conexión con la BD de Mongo
cliente = MongoClient('mongodb://localhost:27017/')
#La Base de Datos se llama Balcones
db = cliente.Balcones
collection_Personas = db.Personas
#Esto es temporal mientras realizo la consulta a mongo para traer el valor de las casas. 
casas = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14']


def acercade():
    """Función para devolver el mensaje en acerca de."""
    messagebox.showinfo(
        title = "Nuevo elemento seleccionado",
        message = "Programa realizado por German"
    )

def salirde():
    """Función para salir de la aplicación"""
    salir = messagebox.askquestion("Salir", "Desea salir de la aplicación")

    if salir == "yes":
        raiz.destroy()

def guardar_persona(Casa, Numid, Tipoid):
    """Funcion que me permite crear una nueva persona"""
    collection_Personas = db.Personas
    collection_Personas.insert_one({'Telefono':{'Activo': '3013025888',
                                                'Activo': '3105987456'},
                                    'Casa': Casa, 
                                    'Estado': 'Activo',
                                    'Tipo': 'Propietario',
                                    'Identificacion': {
                                            'Tipo': Tipoid,
                                            'Numero': Numid
                                        },
                                    
                                   })

def crear_persona():
    """Funcion para crear una persona en la BD de Mongo"""
    ventana_emergente = tk.Toplevel()
    ventana_emergente.title("Ventana emergente")
    ventana_emergente.geometry("350x250")
    
    etk_LblPer1 = ttk.Label(ventana_emergente, text="Nombres: ")
    etk_LblPer1.grid(row=0, column=0, padx=5, pady=5)
    etk_EntPer1 = ttk.Entry(ventana_emergente)
    etk_EntPer1.grid(row=0, column=1, padx=5,pady=5)
    
    etk_LblPer2 = ttk.Label(ventana_emergente, text="Apellidos: ")
    etk_LblPer2.grid(row=1, column=0, padx=5, pady=5)
    etk_EntPer2 = ttk.Entry(ventana_emergente)
    etk_EntPer2.grid(row=1, column=1, padx=5,pady=5)

    etk_LblTDoc = ttk.Label(ventana_emergente, text="Tipo de Documento: ")
    etk_LblTDoc.grid(row=2, column=0, padx=5, pady=5)
    etk_CmbbTDoc = ttk.Combobox(ventana_emergente, values=["CC", "CE", "TI", "RC"])
    etk_CmbbTDoc.grid(row=2, column=1, padx=5, pady=5)
    Tipoid = etk_CmbbTDoc.get()

    etk_LblDocumento = ttk.Label(ventana_emergente, text="Numero de Documento")
    etk_LblDocumento.grid(row=3, column=0, padx=5, pady=5)
    etk_EntDocumento = ttk.Entry(ventana_emergente)
    etk_EntDocumento.grid(row=3, column=1, padx=5, pady=5)
    Numid = etk_EntDocumento.get()

    etk_RdBtnPer1 = ttk.Radiobutton(ventana_emergente, text="Propietario", variable=varOpcion, value=1 )
    etk_RdBtnPer1.grid(row=4, column=0, padx=5, pady=5)
    etk_RdBtn2Per1=ttk.Radiobutton(ventana_emergente, text="Arrendatario", variable=varOpcion, value=2 )
    etk_RdBtn2Per1.grid(row=4, column=1, padx=5, pady=5)

    etk_LblCorreo = ttk.Label(ventana_emergente, text="Correo Eléctronico: ")
    etk_LblCorreo.grid(row=5, column=0, padx=5, pady=5)
    etk_EntCorreo = ttk.Entry(ventana_emergente)
    etk_EntCorreo.grid(row=5, column=1, padx=5, pady=5)

    etk_LblCasas = ttk.Label(ventana_emergente, text="Casas: ")
    etk_LblCasas.grid(row=6, column=0, padx=5, pady=5)
    etk_CmbbCasas = ttk.Combobox(ventana_emergente, values=casas)
    etk_CmbbCasas.grid(row=6, column=1, padx=5, pady=5)
    Casa = etk_CmbbCasas.get()
    
    btn_Per1 = ttk.Button(ventana_emergente, text="Guardar", command=guardar_persona(Casa,Numid, Tipoid))
    btn_Per1.grid(row=7, column=1)

#definicion de la ventana principal
raiz = tk.Tk()

#definición del menu de la aplicación
barra_menu= tk.Menu(raiz)

#Definición del menu personas de la aplicación donde se realizaran todas las acciones
#pertinentes como creación, consulta y actualización. 
menu_personas = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Personas", menu=menu_personas)
menu_personas.add_command(label="Consulta")
menu_personas.add_separator()
menu_personas.add_command(label="Creación", command=crear_persona)
menu_personas.add_command(label="Modificación")
menu_personas.add_command(label="Paz y Salvo")
menu_personas.add_separator()
menu_personas.add_command(label="Salir", command=salirde)

#Menu relacionado con los pagos de la aplicación 
menu_pagos = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Pagos", menu=menu_pagos)
menu_pagos.add_command(label="Ingresar Pago")
menu_pagos.add_command(label="Consultar Pago")
menu_pagos.add_command(label="Estado de Cuenta")

#menu relacionado con los movimientos de facturar mes a mes las cuotas
#Adicional esta el tema de registrar los pagos de las personas.
#Tambien se debe registrar los egresos de dinero que se generan 
menu_movimientos = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Movimientos", menu=menu_movimientos)
menu_movimientos.add_command(label="Facturar")
menu_movimientos.add_command(label="Egresos-Gastos")
menu_movimientos.add_command(label="Ingresos")
menu_movimientos.add_command(label="Cuentas x Pagar")

#En este menu se registraran todos los proyectos realizados año por año. 
menu_proyectos = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Proyectos", menu=menu_proyectos)
menu_proyectos.add_command(label="Crear Proyecto")
menu_proyectos.add_command(label="Consulta Proyecto")
menu_proyectos.add_command(label="Ingresar Avance")

#Menu de ayuda de la aplicación
menu_ayuda = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)
menu_ayuda.add_command(label="Acerca de ...", command=acercade)

raiz.config(menu=barra_menu)

raiz.title("Balcones de Capellania")
raiz.geometry("350x250")
#Creacion de los diferentes frames que se utilizaran dentro de la ventana de la aplicación
miFrame = ttk.Frame(raiz)
miFrame.pack()
miFrame2 = ttk.Frame(raiz)
miFrame2.pack()

#Comando para ubicar en un pack segun lo que necesite. 
#entry.pack(side=tk.LEFT)
#entry.pack(side=tk.LEFT)
#self.label = ttk.Label(self, text="...desde Tkinter!")
#self.label.pack(before=self.entry)

milabelpantalla = tk.StringVar()
varOpcion = tk.IntVar()
valores=[]


def fnguardar():
    """Funcion temporal para mostrar en un label la info de una variable"""
    #T1 = Label1Texto.get()
    T3 = cuadroTexto3.get()
    eleccion = combo.get()
    if T3.isnumeric():
        print(f"prueba exitosa el valor ingresado es: {T3}")
    else:
        print("Valor no valido")
    var1 = 'prueba'
    print(f"la casa seleccionada es {eleccion}")
    milabelpantalla.set("Texto1")
    return var1

def selection_changed(event):
    """Funcion que me devuelve el valor de las personas por casa"""
    selection = combo.get()

    for document in collection_Personas.find({'Casa': selection}):
        nombresito = document['Personas']['Nombres'] + document['Personas']['Apellidos']
        valores.append(nombresito)
        
    combo2["values"] = valores
    valores.clear()



#para un cuadro de contraseña se utiliza el siguiente comando
#cuadroTexto.config(show="*")

miLabel1=ttk.Label(miFrame, text="Casa: ")
miLabel1.grid(row=0, column=0, sticky="e", padx=5, pady=5)
combo = ttk.Combobox(miFrame, values=casas)
combo.set('01')
combo.grid(row=0, column=1)
combo.config(justify="center", width=30)
combo.bind("<<ComboboxSelected>>", selection_changed)

#comienzo a ubicar los elementos que quiero mostrar en la ventana
print(valores)
miLabel2=ttk.Label(miFrame, text="Recibi de: ")
miLabel2.grid(row=1, column=0, sticky="e", padx=5, pady=5)
combo2 = ttk.Combobox(miFrame, values=valores)
combo2.grid(row=1,column=1,  padx=5, pady=5)
combo2.config(justify="center", width=30)


miLabel3=ttk.Label(miFrame, text="La suma de: ")
miLabel3.grid(row=2, column=0, sticky="e", padx=5, pady=5)
cuadroTexto3=ttk.Entry(miFrame)
cuadroTexto3.grid(row=2,column=1)
cuadroTexto3.config(justify="center", width=33)

miLabel4=ttk.Label(miFrame, text="Por Concepto de: ")
miLabel4.grid(row=3, column=0, sticky="e", padx=5, pady=5)
cuadroTexto4=ttk.Entry(miFrame)
cuadroTexto4.grid(row=3,column=1)
cuadroTexto4.config(justify="center", width=33)

rb=ttk.Radiobutton(miFrame, text="Efectivo", variable=varOpcion, value=1 )
rb.grid(row=4, column=0)
rb2=ttk.Radiobutton(miFrame, text="Consignacion", variable=varOpcion, value=2 )
rb2.grid(row=4, column=1)

cb=ttk.Checkbutton(miFrame, text="Efectivo")
cb.grid(row=5,column=0)


botonEnvio=ttk.Button(miFrame, text="Guardar", command=fnguardar)
botonEnvio.grid(row=6, column=1, columnspan=2)


miLabel5=ttk.Label(miFrame, textvariable=milabelpantalla)
miLabel5.grid(row=7, column=0, sticky="e", padx=5, pady=5)

raiz.mainloop()
#Ejemplo de como borrar los widgets en un frame
"""
import tkinter as tk

def eliminar_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()

root = tk.Tk()

frame = tk.Frame(root)
frame.pack()

label = tk.Label(frame, text="Hola")
label.pack()

button = tk.Button(frame, text="Eliminar widgets", command=lambda: eliminar_widgets(frame))
button.pack()

root.mainloop()


"""
