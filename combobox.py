import tkinter as tk
from tkinter import ttk

def actualizar_combobox2(event):
    # Obtén el valor seleccionado en el primer ComboBox
    seleccion = combo1.get()

    # Borra cualquier elemento anterior en el segundo ComboBox
    combo2.set("")  # Limpia la selección anterior
    combo2['values'] = []  # Borra los valores anteriores

    # Filtra y actualiza el contenido del segundo ComboBox
    if seleccion == "Opción 1":
        combo2['values'] = ["Opción 1 - Valor 1", "Opción 1 - Valor 2", "Opción 1 - Valor 3"]
    elif seleccion == "Opción 2":
        combo2['values'] = ["Opción 2 - Valor 1", "Opción 2 - Valor 2"]
    # Agrega más opciones según tus necesidades

def pagos():
    ventana_pagos = tk.Toplevel()
    ventana_pagos.title("Selección de Pagos")

    # Crear el primer ComboBox en la ventana de pagos
    global combo1
    combo1 = ttk.Combobox(ventana_pagos, values=["Opción 1", "Opción 2", "Opción 3"])
    combo1.pack()
    combo1.bind("<<ComboboxSelected>>", actualizar_combobox2)

    # Crear el segundo ComboBox en la ventana de pagos
    global combo2
    combo2 = ttk.Combobox(ventana_pagos)
    combo2.pack()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Aplicación de Pagos")

# Botón para abrir la ventana de pagos
boton_pagos = tk.Button(ventana, text="Selección de Pagos", command=pagos)
boton_pagos.pack()

ventana.mainloop()
