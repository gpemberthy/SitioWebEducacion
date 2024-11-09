import tkinter as tk
from tkinter import messagebox

def preguntar():
    """ Este es un metodo que muestra un mensaje en pantalla """
    resultado = messagebox.askquestion("Pregunta", "¿Quieres continuar?")
    if resultado == 'yes':
        respuesta_label.config(text="Elegiste Sí")
    else:
        respuesta_label.config(text="Elegiste No")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Ejemplo de askquestion")

# Crear un botón que al hacer clic, mostrará la pregunta
boton_pregunta = tk.Button(ventana, text="Preguntar", command=preguntar)
boton_pregunta.pack(pady=20)

# Etiqueta para mostrar la respuesta
respuesta_label = tk.Label(ventana, text="")
respuesta_label.pack()

# Iniciar el bucle principal
ventana.mainloop()
