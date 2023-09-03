import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x200")

# Crear una lista de opciones
opciones = ["Opción 1", "Opción 2", "Opción 3"]

# Crear un objeto Combobox
combo = ttk.Combobox(root, values=opciones)

# Colocar el objeto Combobox en la ventana
combo.pack()

root.mainloop()