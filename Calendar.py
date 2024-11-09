import tkinter as tk
from tkcalendar import Calendar

def mostrar_fecha():
    fecha_seleccionada = cal.get_date()
    etiqueta_fecha.config(text=f"Fecha seleccionada: {fecha_seleccionada}")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Calendario")

# Crear el widget de calendario
cal = Calendar(ventana, selectmode='day', year=2024, month=2, day=3)
cal.pack(pady=20)

# Crear un botón para obtener la fecha seleccionada
boton_obtener_fecha = tk.Button(ventana, text="Obtener Fecha", command=mostrar_fecha)
boton_obtener_fecha.pack(pady=10)

# Crear una etiqueta para mostrar la fecha seleccionada
etiqueta_fecha = tk.Label(ventana, text="")
etiqueta_fecha.pack(pady=10)

# Iniciar el bucle de eventos
ventana.mainloop()
