from tkinter import *
from tkinter import messagebox, ttk, filedialog
# Librerias para la conexión con la base de datos Mongo
from pymongo import MongoClient
# Librerias para el manejo de las fechas
from datetime import date, datetime
# Librerias para la creación del archivo en pdf
from reportlab.pdfgen import canvas
#librerias para el envio del documento pdf por correo electronico
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

#definicion de la ventana principal
raiz = Tk()
#definición del menu de la aplicación
var_nombres = StringVar
rb_opcion = IntVar()
residentes=[]
residente=[]
lista_pagos=[]
proyecto = 0
#Esto es temporal mientras realizo la consulta a mongo para traer el valor de las casas. 
casas = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14']

raiz.title("Balcones de Capellania")
raiz.geometry("850x400")
barra_menu = Menu(raiz)
menu_bancos = Menu(barra_menu, tearoff=0)
menuProyectos = Menu(barra_menu, tearoff=0)
menuConfiguracion = Menu(barra_menu, tearoff=0)
#Componentes del menu
barra_menu.add_cascade(label="Bancos", menu=menu_bancos)
barra_menu.add_cascade(label="Proyectos", menu=menuProyectos)
barra_menu.add_cascade(label="Configuracion", menu=menuConfiguracion)
menu_bancos.add_command(label="Estado Bancos")
menuProyectos.add_command(label="Crear Proyecto")
raiz.config(menu=barra_menu)
frame4 = LabelFrame(raiz, text=" CUADRO PRINCIPAL ")
frame4.grid(row=0, column=1, rowspan=3)
frame4.config(width=670, height=370)

def conexion_mongo():
    """Funcion que brinda la conexion con la BD Mongo"""
    #Apertura de la conexión con la BD de Mongo
    cliente = MongoClient('mongodb://localhost:27017/')
    #La Base de Datos se llama Balcones
    db = cliente.Balcones
    return db

def generate_pdf_soporte_pago():
    """Metodo que genera formato de soporte de pago"""
    # Create the canvas
    pdf_canvas = canvas.Canvas("example2.pdf", pagesize=(400,300))
    
    # Cuadrante superior donde esta el nombre del conjunto
    pdf_canvas.setFillColorRGB(211/255, 211/255, 211/255) 
    pdf_canvas.roundRect(10, 240, 380, 50, 4, stroke=1, fill=1)
    
    #Cuadrante central
    pdf_canvas.setFillColorRGB(210/255, 255/255, 210/255) 
    pdf_canvas.roundRect(10, 10, 380, 177, 4, stroke=1, fill=1)
    
    pdf_canvas.setFillColorRGB(210/255, 210/255, 225/255)
    pdf_canvas.roundRect(10, 192, 380, 45, 4, stroke=1, fill=1)

    #Cuadrante del numero del comprobante
    pdf_canvas.setFillColorRGB(255/255, 255/255, 255/255) 
    pdf_canvas.roundRect(255, 195, 125, 40, 4, stroke=1, fill=1)

    pdf_canvas.setDash(4,3)
    pdf_canvas.line(100,158,260,158)
    pdf_canvas.line(100,122,260,122)

    pdf_canvas.setFillColorRGB(0,0,0)
    pdf_canvas.setFont("Helvetica-Bold", 14)
    pdf_canvas.drawString(60, 265, "DUQUE OCHOA PROPIEDAD HORIZONTAL")
    pdf_canvas.setFont("Helvetica", 8)
    pdf_canvas.drawString(160, 255, "Nit: 900.740.113-3")
    pdf_canvas.drawString(150, 245, "Cra 8a # 20a-138 / 148")
    
    #pdf_canvas.setFont("Courier", 10)
    pdf_canvas.setFont("Helvetica-Bold", 10)
    pdf_canvas.drawString(270, 218, "SOPORTE DE PAGO")
    pdf_canvas.setFillColorRGB(255,0,0)
    pdf_canvas.setFont("Helvetica-Bold", 14)
    pdf_canvas.drawString(310, 200, "560")
    
    pdf_canvas.setFont("Times-Bold", 12)
    pdf_canvas.setFillColorRGB(0, 0, 0)
    pdf_canvas.drawString(45, 220   , "Fecha:     ")
    pdf_canvas.drawString(45, 200, "Ciudad:     ")
    pdf_canvas.drawString(280, 160, "Casa No:")
    pdf_canvas.setFont("Times-Roman", 14)
    pdf_canvas.drawString(25, 160, "Pagado Por: ")
    pdf_canvas.setFont("Times-Roman", 12)
    pdf_canvas.drawString(25, 125, "La Suma de:")
    
    pdf_canvas.drawString(25, 100, "Efectivo                     Consignacion                     Transferencia")
    
    pdf_canvas.setFont("Helvetica-Bold", 10)
    pdf_canvas.drawString(25, 70, "Transacción No:")
    pdf_canvas.drawString(25, 50, "Entidad Financiera:")
    pdf_canvas.setFont("Courier-Oblique", 7.5)
    pdf_canvas.drawString(25, 30, "Numero de cuenta de Ahorros Banco Davivienda:  462500020963")
    pdf_canvas.drawString(25, 20, "Este soporte es su comprobante del pago realizado a la administración")
    
    #llenado de la informacion
    pdf_canvas.setFont("Courier-Bold", 10)
    pdf_canvas.drawString(95, 220, "05/09/2023")
    pdf_canvas.drawString(95, 200, "Cajica")
    pdf_canvas.setFont("Courier-Bold", 14)
    pdf_canvas.drawString(335, 160, "14")
    pdf_canvas.setFont("Courier-Bold", 10)
    pdf_canvas.drawString(105, 160, "Luis Fernando Gonzalez")
    pdf_canvas.setFont("Courier-Bold", 14)
    pdf_canvas.drawString(135, 125, "100.000")
    pdf_canvas.drawString(130, 70, "xxxxxxxx")
    pdf_canvas.drawString(130, 50, "xxxxxxxx")
    
    # Save the PDF
    pdf_canvas.save()

def generate_pdf_recibo_administracion():
    """Metodo que genera formato de """
    # Create the canvas
    pdf_canvas = canvas.Canvas("Recibo.pdf", pagesize=(400,300))
    
    # Cuadrante superior donde esta el nombre del conjunto
    pdf_canvas.setFillColorRGB(211/255, 211/255, 211/255) 
    pdf_canvas.roundRect(10, 240, 380, 50, 4, stroke=1, fill=1)
    
    #Cuadrante central
    pdf_canvas.setFillColorRGB(210/255, 255/255, 210/255) 
    pdf_canvas.roundRect(10, 10, 380, 177, 4, stroke=1, fill=1)
    
    pdf_canvas.setFillColorRGB(210/255, 210/255, 225/255)
    pdf_canvas.roundRect(10, 192, 380, 45, 4, stroke=1, fill=1)

    #Cuadrante del numero del comprobante
    pdf_canvas.setFillColorRGB(255/255, 255/255, 255/255) 
    pdf_canvas.roundRect(255, 195, 125, 40, 4, stroke=1, fill=1)

    pdf_canvas.setDash(4,3)
    pdf_canvas.line(100,158,260,158)
    pdf_canvas.line(100,122,260,122)

    pdf_canvas.setFillColorRGB(0,0,0)
    pdf_canvas.setFont("Helvetica-Bold", 14)
    pdf_canvas.drawString(60, 265, "DUQUE OCHOA PROPIEDAD HORIZONTAL")
    pdf_canvas.setFont("Helvetica", 8)
    pdf_canvas.drawString(160, 255, "Nit: 900.740.113-3")
    pdf_canvas.drawString(150, 245, "Cra 8a # 20a-138 / 148")
    
    #pdf_canvas.setFont("Courier", 10)
    pdf_canvas.setFont("Helvetica-Bold", 10)
    pdf_canvas.drawString(270, 218, "SOPORTE DE PAGO")
    pdf_canvas.setFillColorRGB(255,0,0)
    pdf_canvas.setFont("Helvetica-Bold", 14)
    pdf_canvas.drawString(310, 200, "560")
    
    pdf_canvas.setFont("Times-Bold", 12)
    pdf_canvas.setFillColorRGB(0, 0, 0)
    pdf_canvas.drawString(45, 220   , "Fecha:     ")
    pdf_canvas.drawString(45, 200, "Ciudad:     ")
    pdf_canvas.drawString(280, 160, "Casa No:")
    pdf_canvas.setFont("Times-Roman", 14)
    pdf_canvas.drawString(25, 160, "Pagado Por: ")
    pdf_canvas.setFont("Times-Roman", 12)
    pdf_canvas.drawString(25, 125, "La Suma de:")
    
    pdf_canvas.drawString(25, 100, "Efectivo                     Consignacion                     Transferencia")
    
    pdf_canvas.setFont("Helvetica-Bold", 10)
    pdf_canvas.drawString(25, 70, "Transacción No:")
    pdf_canvas.drawString(25, 50, "Entidad Financiera:")
    pdf_canvas.setFont("Courier-Oblique", 7.5)
    pdf_canvas.drawString(25, 30, "Numero de cuenta de Ahorros Banco Davivienda:  462500020963")
    pdf_canvas.drawString(25, 20, "Este soporte es su comprobante del pago realizado a la administración")
    
    #llenado de la informacion
    pdf_canvas.setFont("Courier-Bold", 10)
    pdf_canvas.drawString(95, 220, "05/09/2023")
    pdf_canvas.drawString(95, 200, "Cajica")
    pdf_canvas.setFont("Courier-Bold", 14)
    pdf_canvas.drawString(335, 160, "14")
    pdf_canvas.setFont("Courier-Bold", 10)
    pdf_canvas.drawString(105, 160, "Luis Fernando Gonzalez")
    pdf_canvas.setFont("Courier-Bold", 14)
    pdf_canvas.drawString(135, 125, "100.000")
    pdf_canvas.drawString(130, 70, "xxxxxxxx")
    pdf_canvas.drawString(130, 50, "xxxxxxxx")
    
    # Save the PDF
    pdf_canvas.save()

def envio_correo():
    """ Metodo que envia documentos adjuntos por correo electrónico"""
    # Configuración de la cuenta de Gmail
    sender_email = "german.pemberty@gmail.com"
    sender_password = "ottmedkbarfpgcfw"

    # Destinatario
    recipient_email = "german.pemberthy@outlook.com"

    # Crear el mensaje
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "Prueba de envio"

    # Cuerpo del correo
    body = "Señor residente adjunto se encuentra el comprobante del ultimo pago realizado"
    message.attach(MIMEText(body, "plain"))

    # Adjuntar el documento
    file_path = "C:/Users/germa/Desktop/SitioWebEducacion/example2.pdf"  # Reemplaza con la ruta de tu documento
    filename = "example2.pdf"  # Nombre que tendrá el archivo adjunto en el correo
    attachment = open(file_path, "rb")

    part = MIMEBase("application", "octet-stream")
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename= {filename}")

    message.attach(part)

    # Iniciar la conexión con el servidor SMTP de Gmail
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)

        # Enviar el correo
        server.sendmail(sender_email, recipient_email, message.as_string())
        messagebox.showinfo(title = "Nuevo elemento seleccionado", message = "Correo enviado con éxito")
        print("Correo enviado con éxito")

    except Exception as envio1:
        messagebox.showinfo(title = "Nuevo elemento seleccionado", message = "Error al enviar el correo:")
        print(f"Error al enviar el correo: {str(envio1)}")

    finally:
        # Cerrar la conexión con el servidor
        server.quit()

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
            residente.append(document['Personas']['Nombres'] + document['Personas']['Apellidos'])
    combo_residente["values"]=residente
    combo_residente.config(state='enabled')
    residente.clear()
    collection_recibos = db.Recibos
    for document in collection_recibos.find({'Casa': seleccion}):
        if document['Estado'] == ' Pendiente ':
            valor_col1 = document['Recibo']
            valor_col2 = document['Valor']
            valor_col3 = document['Mes']
            valor_col4 = document['Anno']
            mi_arbol.insert('', 'end', values=(valor_col1, valor_col2, valor_col3, valor_col4))
    
def agregar_fila():
    """Metodo para agregar una fila al treeview de los pagos"""
    valor_col1 = combo_casa.get()
    valor_col2 = val_pago.get()
    valor_col3 = pago_fecha.get()
    mi_arbol.insert('', 'end', values=(valor_col1, valor_col2, valor_col3))

def pagos():
    """ Metodo para gestionar los pagos """
    for widget in frame4.winfo_children():
        widget.destroy()
    
    global combo_casa
    Label(frame4, text="Casa", anchor='center').grid(row=0, column=0)
    combo_casa = ttk.Combobox(frame4, values=casas)
    combo_casa.grid(row=1, column=0)
    combo_casa.config(width=7)
    combo_casa.bind("<<ComboboxSelected>>", lambda event: consulta_residente(event, combo_casa))

    global combo_residente
    Label(frame4, text = "Recibi de: ", anchor='e').grid(row=0, column=1)
    combo_residente = ttk.Combobox(frame4)
    combo_residente.grid(row=1, column=1)
    combo_residente.config(width=25, state='disabled')
    
    global val_pago
    Label(frame4, text="Valor pagado: ").grid(row=2,column=0)
    val_pago = Entry(frame4)
    val_pago.grid(row=3, column=0)

    global pago_fecha
    Label(frame4, text="Fecha del pago:").grid(row=2,column=1)
    pago_fecha = Entry(frame4)
    pago_fecha.grid(row=3, column=1)

    global val_concepto
    Label(frame4, text='Concepto:').grid(row=4,column=0)
    val_concepto = Entry(frame4)
    val_concepto.grid(row=4, column=1, columnspan=2)
    val_concepto.config(width=50)
    
    Label(frame4, text='Banco:').grid(row=5,column=0)
    val_banco=Entry(frame4)
    val_banco.grid(row=5,column=1)
    Label(frame4, text='Numero: ').grid(row=5,column=2)
    val_numtrans=Entry(frame4)
    val_numtrans.grid(row=5,column=3)
    rb1= Radiobutton(frame4, text="Efectivo", variable= rb_opcion, value=1 )
    rb1.grid(row=1, column=2)
    rb2= Radiobutton(frame4, text="Consignacion", variable=rb_opcion, value=2 )
    rb2.grid(row=2, column=2)
    rb3= Radiobutton(frame4, text="Transferencia", variable=rb_opcion, value=3 )
    rb3.grid(row=3, column=2)

    boton_agregar = Button(frame4, text="Pagar", command=agregar_fila)
    boton_agregar.grid(row=7, column=0, columnspan=3, sticky= W+E)

    #Tabla
    global mi_arbol
    mi_arbol = ttk.Treeview(frame4, height=5, columns=('Col1', 'Col2', 'Col3', 'Col4'))
    mi_arbol.grid(row=8, column=0, columnspan=3)
    mi_arbol.heading('#0', text="Id")
    mi_arbol.heading('Col1', text="Recibo")
    mi_arbol.heading('Col2', text="Valor Recibo")
    mi_arbol.heading('Col3', text="Mes")
    mi_arbol.heading('Col4', text="Año")
    mi_arbol.column('#0', width=45)
    mi_arbol.column('Col1', width=75, anchor='center')
    mi_arbol.column('Col2', width=100, anchor='center')
    mi_arbol.column('Col3', width=140, anchor='center')
    mi_arbol.column('Col4', width=60, anchor='center')

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

    btn_guardar = Button(ventana_emergente_pagos, text="Guardar", command=envio_correo)
    btn_guardar.grid(row=3, column=0, sticky= W+E)

    #Tabla
    miArbol = ttk.Treeview(ventana_emergente_pagos, height=10, columns=2)
    miArbol.grid(row=4, column=0)
    miArbol.heading("#0", text="Nombre")
    miArbol.heading("#1", text="Pagos")

def menu_pagos():
    """Metodo que ejecuta la pantalla principal"""
    frame = LabelFrame(raiz, text="  Modulo Pagos   ")
    frame.config(width=100, height=100)
    frame.grid(row=0, column=0, padx=15, pady=10)
    #  -- Pagos  --
    #Label(frame, text="Registrar Pagos").grid(row=1, column=0)
    boton1 = Button(frame, text="Registrar Pagos", width=15, command=pagos)
    boton1.grid(row=2, column=0, sticky= W+E, padx=5, pady=5)
    boton1.config(fg='black', bg='#158645', cursor='hand2', activebackground='yellow')

    boton2 = Button(frame,text="Consultar Pagos", command=pagos2)
    boton2.grid(row=4, columnspan=2, padx= 5, pady=5, sticky= W+E)
    boton2.config(cursor="hand2")

def guardar_persona(): 
    """Funcion que me permite guardar en la BD la persona"""
    valor_nombre = nombre_per.get()
    valor_casas =combo_casas.get()
    valor_apellido = apellidos.get()
    valor_tipoid = combo_tipoid.get()
    valor_correo = correo.get()
    valor_numid = num_id.get()
    valor_telefono = telefono.get()
    valor_tipoper = combo_tipo.get()
    valor_timestamp = datetime.now()
    print(valor_timestamp)

    db = conexion_mongo()
    collection_personas = db.Personas
    collection_personas.insert_one({'Telefono':{'Activo': valor_telefono},
                                    'Casa': valor_casas, 
                                    'Estado': 'Activo',
                                    'Tipo': valor_tipoper,
                                    'Actualizado': valor_timestamp,
                                    'Creado': valor_timestamp,
                                    'Identificacion': {
                                               'Tipo': valor_tipoid,
                                                'Numero': valor_numid
                                            },
                                    'correos': {'Activo': valor_correo},
                                    'Personas': {'Nombres': valor_nombre,
                                                 'Apellidos': valor_apellido} 
                                        })
    miArbol.insert('', 'end', 
                   values=(valor_nombre + valor_apellido, valor_tipoid, valor_numid, valor_correo, valor_telefono,valor_tipoper, 'Activo'))
    mi_boton.config(state='disabled')

def ventana_personas():
    """Funcion para gestionar las personas"""
    
    for widget in frame4.winfo_children():
        widget.destroy()
    #ventana_emergente_pagos = Toplevel()
    #ventana_emergente_pagos.title("  Ventanas Personas  ")
    
    #frameb = LabelFrame(frame4, text="  Registro de personas  ")
    #frameb.grid(row=0, column=0, pady=5)
    #frame.grid(row=0, column=0, columnspan=2, pady=5)

    global nombre_per
    Label(frame4, text="Nombres: ").grid(row=0, column=0, padx=5, pady=5)
    nombre_per = Entry(frame4)
    nombre_per.grid(row=0, column=1)
    nombre_per.focus()
    
    Label(frame4, text="Apellidos: ").grid(row=0,column=2, padx=5, pady=5)
    global apellidos
    apellidos = Entry(frame4)
    apellidos.grid(row=0, column=3)

    Label(frame4, text="Tipo Id: ").grid(row=1,column=0, padx=5, pady=5)
    global combo_tipoid
    combo_tipoid = ttk.Combobox(frame4, values=('CC', 'CE', 'TI', 'NIT'), width=5)
    combo_tipoid.grid(row=1, column=1)

    Label(frame4, text="Identificacion: ").grid(row=1,column=2, padx=5, pady=5)
    global num_id
    num_id = Entry(frame4)
    num_id.grid(row=1, column=3)

    Label(frame4, text="Telefono: ").grid(row=2,column=0, padx=5, pady=5)
    global telefono
    telefono = Entry(frame4)
    telefono.grid(row=2, column=1)

    Label(frame4, text="Correo: ").grid(row=2,column=2, padx=5, pady=5)
    global correo
    correo = Entry(frame4)
    correo.grid(row=2, column=3)
    correo.config(width=30)

    Label(frame4, text="Casa: ").grid(row=3,column=0, padx=5, pady=5)
    global combo_casas
    combo_casas = ttk.Combobox(frame4, values=casas, width=5)
    combo_casas.grid(row=3, column=1)

    Label(frame4, text="Tipo: ").grid(row=3,column=2, padx=5, pady=5)
    global combo_tipo
    combo_tipo = ttk.Combobox(frame4, values=('Propietario', 'Arrendatario'), width=15)
    combo_tipo.grid(row=3, column=3)

    global mi_boton
    mi_boton = Button(frame4, text="Guardar", command= guardar_persona)
    mi_boton.grid(row=4, column=0, sticky= W+E)
    mi_boton.config(cursor='hand2')

    #Tabla
    global miArbol
    miArbol = ttk.Treeview(frame4, height=5, 
                           columns=('Col_Nombre', 'Col_TId', 'Col_numid', 'Col_Correo', 'Col_Tel', 'Col_Tip', 'Col_Est'))
    miArbol.grid(row=6, column=0, columnspan=4)
    miArbol.heading("#0", text="Id")
    miArbol.heading('Col_Nombre', text="Nombres")
    miArbol.heading('Col_TId', text="Tipo Id")
    miArbol.heading('Col_numid', text="Num Id")
    miArbol.heading('Col_Correo', text="Correo")
    miArbol.heading('Col_Tel', text="Teléfono")
    miArbol.heading('Col_Tip', text="Tipo")
    miArbol.heading('Col_Est', text="Estado")
    miArbol.column('#0', width=10)
    miArbol.column('Col_Nombre', width=140)
    miArbol.column('Col_TId', width=50)
    miArbol.column('Col_numid', width=70)
    miArbol.column('Col_Correo', width=170)
    miArbol.column('Col_Tel', width=80)
    miArbol.column('Col_Tip', width=70)
    miArbol.column('Col_Est', width=70)

def llenar_tabla(mi_arbol):
    """Funcion que sirve para llenar la tabla en la ventana de residentes"""
    if len(residentes) > 0:
        mi_arbol.insert('', 0, text=0, values=(residentes[4], residentes[3]))

def actualizar_residente():
    """Metodo para actualizar un ressidente"""
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
    mi_boton1.config(cursor='hand2')

def menu_personas():
    """Metodo que ejecuta la pantalla de personas """
    frame2 = LabelFrame(raiz, text="   Modulo Residentes   ")
    #frame2.config(width=100, height=100, bg="blue")
    frame2.config(width=100, height=100)
    frame2.grid(row=1, column=0, padx=10, pady=5)
    #  -- Pagos  --
    #Label(frame2, text="Registrar Persona").grid(row=1, column=0)

    Button(frame2, text="Registrar Residente", width=15, 
           command=ventana_personas).grid(row=0, column=0, sticky= W+E, padx=5, pady=5)

    #Label(frame2, text="Consultar Persona").grid(row=3, column=0)
    boton1 = Button(frame2,text="Consultar Residente")
    boton1.grid(row=1, columnspan=2, padx= 5, pady=5, sticky= W+E)
    boton1.config()

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
    """Metodo para consultar los datos de un proyecto"""
    for widget in frame4.winfo_children():
        widget.destroy()
    Label(frame4, text="Registrar un proyecto").grid(row=0, column=0)
    Button(frame4, text="prueba").grid(row=0, column=1)

def registrar_proyecto():
    """Metodo para registrar un proyecto"""
    for widget in frame4.winfo_children():
        widget.destroy()
    
    Label(frame4, text="Espacio para registrar todos los movimientos de un proyecto").grid(row=0, column=0)
    Button(frame4, text="prueba").grid(row=1, column=1)

def menu_proyectos():
    """Metodo que ejecuta la pantalla principal"""
    frame3 = LabelFrame(raiz, text="  Modulo Proyectos   ")
    #frame3.config(width=100, height=100, bg="green")
    frame3.config(width=100, height=100)
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