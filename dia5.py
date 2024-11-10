from tkinter import *
from tkinter import messagebox, ttk
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Librerias para el manejo de las fechas
from datetime import datetime
# Librerias para la conexión con la base de datos Mongo
from pymongo import MongoClient
# Librerias para la creación del archivo en pdf
from reportlab.pdfgen import canvas

valor_residente = 'Diego Andres Sabogal Donoso'
valor_col5 = '09'
valor_col6 = '100000'
valor_col7 = '2023-10-16'
valor_col8 = 'Administracion'
valor_col9 = '10726587351'
valor_col10 = 'Banco de bogota'
no_recibo = 599
#tipo = 'Consignaci2'
casas = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14']
casa_facturacion = StringVar
numero_recibo = 720
fecha_facturacion = '2023-10-16'
resum_saldo = 100000
resumen_cargos_del_mes = 100000
resum_ctas_facturadas = 1
resum_pagos_recibidos = 0
resum_cuotas_pagadas = 0
resumen_total_a_pagar = 0
resum_cuotas_pend= 0
saldo_a_favor = False
cuota_extraordinaria = False
valor_cuota_extraordinaria = 100000
factura_valor_pago = 0
numero_recibo = 0

def conexion_mongo():
    """Funcion que brinda la conexion con la BD Mongo"""
    #Apertura de la conexión con la BD de Mongo
    cliente = MongoClient('mongodb://localhost:27017/')
    #La Base de Datos se llama Balcones
    db = cliente.Balcones_Desarrollo
    return db

def generate_pdf_soporte_pago():
    """Metodo que genera formato de soporte de pago"""
    # Create the canvas

    nombre_fichero = 'Recibo' + str(no_recibo) + '.pdf'
    pdf_canvas = canvas.Canvas(nombre_fichero, pagesize=(400,300))

    # Cuadrante superior donde esta el nombre del conjunto
    pdf_canvas.setFillColorRGB(211/255, 211/255, 211/255) 
    pdf_canvas.roundRect(10, 240, 380, 50, 4, stroke=1, fill=1)

    #Cuadrante central
    pdf_canvas.setFillColorRGB(235/255, 255/255, 255/255) 
    pdf_canvas.roundRect(10, 10, 380, 177, 4, stroke=1, fill=1)

    pdf_canvas.setFillColorRGB(210/255, 210/255, 225/255)
    pdf_canvas.roundRect(10, 192, 380, 45, 4, stroke=1, fill=1)

    #Cuadrante del numero del comprobante
    pdf_canvas.setFillColorRGB(255/255, 255/255, 255/255) 
    pdf_canvas.roundRect(255, 195, 125, 40, 4, stroke=1, fill=1)

    #Cuadrado del campo Efectivo
    pdf_canvas.setFillColorRGB(255/255, 255/255, 255/255) 
    pdf_canvas.roundRect(72, 96, 15, 15, 4, stroke=1, fill=1)

    #Cuadrado del campo Consignación
    pdf_canvas.setFillColorRGB(255/255, 255/255, 255/255) 
    pdf_canvas.roundRect(200, 96, 15, 15, 4, stroke=1, fill=1)

    #Cuadrado del campo Transferencia
    pdf_canvas.setFillColorRGB(255/255, 255/255, 255/255) 
    pdf_canvas.roundRect(327, 96, 15, 15, 4, stroke=1, fill=1)

    pdf_canvas.setDash(4,3)
    pdf_canvas.line(100,158,280,158)
    pdf_canvas.line(100,122,280,122)

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
    pdf_canvas.drawString(310, 200, str(no_recibo))

    pdf_canvas.setFont("Times-Bold", 12)
    pdf_canvas.setFillColorRGB(0, 0, 0)
    pdf_canvas.drawString(45, 220   , "Fecha:     ")
    pdf_canvas.drawString(45, 200, "Ciudad:     ")
    pdf_canvas.setFont("Times-Roman", 14)
    pdf_canvas.drawString(295, 160, "Casa No:")
    pdf_canvas.drawString(25, 160, "Pagado Por: ")
    pdf_canvas.setFont("Times-Roman", 12)
    pdf_canvas.drawString(25, 125, "La Suma de:")

    pdf_canvas.drawString(25, 100, "Efectivo                     Consignación                     Transferencia")

    pdf_canvas.setFont("Helvetica-Bold", 10)
    pdf_canvas.drawString(25,  75, "Observaciones:")
    pdf_canvas.setFont("Helvetica-Bold", 9)
    pdf_canvas.drawString(25,  50, "Transacción No:")
    pdf_canvas.drawString(195, 50, "Entidad Financiera:")
    pdf_canvas.setFont("Courier-Oblique", 7.5)
    pdf_canvas.drawString(25, 30, "Numero de cuenta de Ahorros Banco Davivienda:  462500020963")
    pdf_canvas.drawString(25, 20, "Este soporte es su comprobante del pago realizado a la administración")

    #llenado de la informacion
    pdf_canvas.setFont("Helvetica-Bold", 10)
    pdf_canvas.drawString(95, 220, str(valor_col7))
    pdf_canvas.drawString(95, 200, "Cajicá")
    pdf_canvas.setFont("Courier-Bold", 12)
    pdf_canvas.drawString(350, 160, str(valor_col5))
 
    pdf_canvas.setFont("Courier-Bold", 10)
    if len(valor_residente) > 28:
        pdf_canvas.drawString(98, 160, valor_residente)
    elif len(valor_residente) > 20:
        pdf_canvas.drawString(112, 160, valor_residente)
    else:
        pdf_canvas.drawString(120, 160, valor_residente)

    pdf_canvas.setFont("Courier-Bold", 14)
    pdf_canvas.drawString(135, 125, str(valor_col6))
    pdf_canvas.setFont("Courier-Bold", 10)
    pdf_canvas.drawString(100, 50, valor_col9)
    pdf_canvas.drawString(283, 50, valor_col10)
    if tipo == 'Efectivo':
        pdf_canvas.drawString(76, 100, 'x')
    elif tipo == 'Consignación':
        pdf_canvas.drawString(204, 100, 'x')
    else:
        pdf_canvas.drawString(332, 100, 'x')

    pdf_canvas.setFont("Courier", 8)
    pdf_canvas.drawString(105, 75, valor_col8)

    # Save the PDF
    pdf_canvas.save()

def generate_pdf_cuota():
    """Metodo que genera el documento en pdf del pago de la cuota"""
    db = conexion_mongo()
    collection_Detalle_factura_tmp = db.Detalle_factura_tmp
    ejey = 0
    # Create the canvas
    nombre_archivo = "Cuota_Casa_" + casa_facturacion + "_" + str(numero_recibo) + ".pdf"
    pdf_canvas = canvas.Canvas(nombre_archivo, pagesize=(400,550))

    # Cuadrante superior donde esta el nombre del conjunto
    pdf_canvas.setFillColorRGB(211/255, 211/255, 211/255) 
    pdf_canvas.roundRect(10, 490, 380, 50, 4, stroke=1, fill=1)
    
    #Segundo cuadrante
    pdf_canvas.setFillColorRGB(210/255, 210/255, 225/255)
    pdf_canvas.roundRect(10, 442, 380, 45, 4, stroke=1, fill=1)

    #Cuadrante central
    pdf_canvas.setFillColorRGB(240/255, 255/255, 240/255) 
    pdf_canvas.roundRect(10, 10, 380, 428, 4, stroke=1, fill=1)

    #Cuandrante del numero del comprobante
    pdf_canvas.setFillColorRGB(255/255, 255/255, 255/255) 
    pdf_canvas.roundRect(250, 445, 135, 40, 4, stroke=1, fill=1)

    pdf_canvas.line(10,156,390,156)
    pdf_canvas.line(10,416,390,416)
    #pdf_canvas.setDash(4,3)
    #pdf_canvas.line(100,158,260,158)

    pdf_canvas.setFillColorRGB(0,0,0)
    pdf_canvas.setFont("Helvetica-Bold", 14)
    pdf_canvas.drawString(60, 515, "DUQUE OCHOA PROPIEDAD HORIZONTAL")
    pdf_canvas.setFont("Helvetica", 8)
    pdf_canvas.drawString(160, 505, "Nit: 900.740.113-3")
    pdf_canvas.drawString(150, 495, "Cra 8a # 20a-138 / 148")

    #pdf_canvas.setFont("Courier", 10)
    pdf_canvas.setFont("Helvetica-Bold", 10)
    pdf_canvas.drawString(255, 468, "CUOTA ADMINISTRACIÓN")
    pdf_canvas.setFillColorRGB(255,0,0)
    pdf_canvas.setFont("Helvetica-Bold", 14)
    pdf_canvas.drawString(310, 450, str(numero_recibo))

    pdf_canvas.setFont("Times-Bold", 10)
    pdf_canvas.setFillColorRGB(0, 0, 0)
    pdf_canvas.drawString(25, 470   , "Fecha:     ")
    pdf_canvas.drawString(145, 470, "Ciudad:     ")
    pdf_canvas.drawString(25, 450, "Casa No:")
    pdf_canvas.setFont("Times-Bold", 12)
    pdf_canvas.drawString(25, 420, "Ref          Concepto                                               Valor          Fecha")
    pdf_canvas.drawString(25, 160, "Resumen")

    pdf_canvas.setFont("Helvetica-Bold", 9)
    pdf_canvas.drawString(25, 140, "Pagos Recibidos")
    pdf_canvas.drawString(25, 125, "Cuotas pagadas")
    pdf_canvas.drawString(25, 110, "Cuotas pendientes")
    if saldo_a_favor:
        pdf_canvas.drawString(25, 95, "Saldo a favor")
    else:
        pdf_canvas.drawString(25, 95, "Saldo en mora")
    pdf_canvas.drawString(25, 80, "Cargos del mes")
    pdf_canvas.drawString(25, 65, "Cuotas facturadas")
    pdf_canvas.drawString(25, 50, "Total a pagar")

    pdf_canvas.setFont("Courier-Oblique", 7.5)
    pdf_canvas.drawString(25, 30, "Para pagos Numero de cuenta de Ahorros Banco Davivienda:  462500020963")
    pdf_canvas.drawString(25, 20, "Este es su cuota de administración para pago en los 5 primeros dias del mes")
    
    #llenado de la informacion
    pdf_canvas.setFont("Times-Bold", 10)
    pdf_canvas.drawString(70, 450, casa_facturacion)
    pdf_canvas.setFont("Courier-Bold", 10)
    pdf_canvas.drawString(60, 470, fecha_facturacion)
    pdf_canvas.drawString(190, 470, "Cajica")

    #parte del detalle de los movimientos.
    ejey = 400
    for document in collection_Detalle_factura_tmp.find({'Casa': casa_facturacion}):
        valor_tmp = document['Referencia']
        pdf_canvas.drawString(25, ejey, str(valor_tmp))
        valor_tmp = document['Concepto']
        pdf_canvas.drawString(60, ejey, valor_tmp)
        valor_tmp = document['Valor']
        pdf_canvas.drawString(260, ejey, str(valor_tmp))
        pdf_canvas.drawString(253, ejey, '$')
        pdf_canvas.drawString(325, ejey, "2023-10-16")
        ejey -= 17

    #llenado de la parte de resumen
    pdf_canvas.setFont("Courier-Bold", 10)
    resumen_total_a_pagar = resum_saldo + resumen_cargos_del_mes
    pdf_canvas.drawString(138, 140, '$')
    pdf_canvas.drawString(145, 140, str(resum_pagos_recibidos))
    pdf_canvas.drawString(145, 125, str(resum_cuotas_pagadas))
    pdf_canvas.drawString(145, 110, str(resum_cuotas_pend))
    pdf_canvas.drawString(138, 95, '$')
    pdf_canvas.drawString(145, 95, str(resum_saldo))
    pdf_canvas.drawString(138, 80, '$')
    pdf_canvas.drawString(145, 80, str(resumen_cargos_del_mes))
    pdf_canvas.drawString(145, 65, str(resum_ctas_facturadas))
    pdf_canvas.drawString(138, 50, '$')
    pdf_canvas.drawString(145, 50, str(resumen_total_a_pagar))

    # Save the PDF
    pdf_canvas.save()

def envio_correo_pago():
    """ Metodo que envia documentos adjuntos por correo electrónico"""
    # Configuración de la cuenta de Gmail
    global correo_envio_residente
    valor_residente = "German Pemberthy"

    sender_email = "balconescapellania@gmail.com"
    sender_password = "mfsbwjenunfewdkn"

    # Destinatario
    recipient_email = "german.pemberthy@outlook.com"
    #recipient_email = correo_envio_residente

    # Crear el mensaje
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "Soporte de pago"

    # Cuerpo del correo
    body = "Señor/a " + valor_residente + " la administración envia en el adjunto el comprobante del ultimo pago realizado"
    message.attach(MIMEText(body, "plain"))

    # Adjuntar el documento
    file_path = "C:/Users/germa/Desktop/SitioWebEducacion/" + 'Recibo' + str(no_recibo) + '.pdf'  # Reemplaza con la ruta de tu documento
    filename = 'Recibo' + str(no_recibo) + '.pdf'  # Nombre que tendrá el archivo adjunto en el correo
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
        messagebox.showinfo(title = "Mensaje", message = "Pago realizado con exito \n Correo enviado con éxito")
       
        print("Correo enviado con éxito")

    except Exception as envio1:
        messagebox.showinfo(title = "Nuevo elemento seleccionado", message = "Error al enviar el correo:")
        print(f"Error al enviar el correo: {str(envio1)}")

    finally:
        # Cerrar la conexión con el servidor
        server.quit()

def envio_correo_factura():
    """ Metodo que envia documentos adjuntos por correo electrónico"""
    # Configuración de la cuenta de Gmail
    global correo_envio_residente
    valor_residente = "German Pemberthy"
    
    sender_email = "balconescapellania@gmail.com"
    sender_password = "mfsbwjenunfewdkn"

    # Destinatario
    recipient_email = "german.pemberthy@outlook.com"
    #recipient_email = correo_envio_residente

    # Crear el mensaje
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "Facturación mes XXXX Balcones de Capellania."

    # Cuerpo del correo
    body = "Señor residente " + valor_residente + " la administración envia la factura del mes"
    message.attach(MIMEText(body, "plain"))

    # Adjuntar el documento
    file_path = "C:/Users/germa/Desktop/SitioWebEducacion/" + 'Recibo' + str(no_recibo) + '.pdf'  # Reemplaza con la ruta de tu documento
    filename = 'Recibo' + str(no_recibo) + '.pdf'  # Nombre que tendrá el archivo adjunto en el correo
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
        messagebox.showinfo(title = "Mensaje", message = "Correo enviado con éxito")
        print("Correo enviado con éxito")

    except Exception as envio1:
        messagebox.showinfo(title = "Nuevo elemento seleccionado", message = "Error al enviar el correo:")
        print(f"Error al enviar el correo: {str(envio1)}")

    finally:
        # Cerrar la conexión con el servidor
        server.quit()

def realizar_pago():
    """Metodo para gestionar pago ingresado por el front"""
  
    global tipo
    global no_recibo
    valor_pendiente_pago = 0
    valor_timestamp = datetime.now()
    valor_col1 = '01'
    valor_col2 = '100000'
    valor_pagado = int(valor_col2)
    valor_col3 = '2023-10-16'
    valor_col4 = 'Juan Alberto Rojas'
    valor_col5 = 'Pago recibido'
    valor_col6 = 2
    valor_col7 = 600
    valor_col8 = 'Davivienda'

    db = conexion_mongo()
    collection_pagos = db.Pagos
    collection_personas = db.Personas
    collection_configuracion = db.Configuracion
    collection_eventos = db.Eventos
    collection_movimientos_dinero = db.Movimientos_Dinero
    collection_notificaciones = db.Notificaciones

    if valor_col6 == 1:
        tipo = 'Efectivo'
    elif valor_col6 == 2:
        tipo = 'Consignación'
    else:
        tipo = 'Transferencia'

    for document in collection_configuracion.find({'Estado_anno_actual': 'Activo'}):
        anno_actual = document['Anno_actual']

    for document in collection_pagos.find():
        no_recibo_actual = document['No Recibo']

    no_recibo = no_recibo_actual + 1

    collection_pagos.insert_one({'No Recibo': no_recibo,
                                 'Casa': valor_col1, 
                                 'Fecha': valor_timestamp,
                                 'Anno': int(anno_actual),
                                 'Valor': valor_pagado,
                                 'Tipo': tipo,
                                 'Observaciones': valor_col5,
                                 'Recibi De': valor_col4,
                                 'Numero_transaccion': valor_col7,
                                 'Banco': valor_col8,
                                 'Estado': 'Pendiente'
                                        })

    #mi_arbol.insert('', 'end', values=(no_recibo, 'Pago', 'Pendiente', valor_pagado, valor_col3, anno_actual ))

    collection_configuracion.update_one({'Ultimo_recibo_pago': no_recibo_actual},
                                        {'$set': {'Ultimo_recibo_pago': no_recibo }})
    
    collection_eventos.update_one({'Identificador': 4},{'$set': {'Valor': no_recibo}})

    #recorro la tabla de movimientos de dinero para determinar los ultimos valores que se tienen.
    for document in collection_movimientos_dinero.find():
        valor_despues_del_movimiento = document['Valor_despues_del_movimiento']
        en_efectivo = document['En_efectivo']
        en_banco = document['En_banco']

    #Si el pago fue en efectivo se aumenta dicho monto en la tabla de movimientos de dinero
    if tipo == 'Efectivo':
        en_efectivo = en_efectivo + valor_pagado
    else:
        en_banco = en_banco + valor_pagado

    valor_antes_del_movimiento = valor_despues_del_movimiento
    valor_despues_del_movimiento = valor_despues_del_movimiento + valor_pagado
    observacion = 'Pago casa ' + valor_col1
    
    collection_movimientos_dinero.insert_one({
        'Tipo': 'Credito',
        'Observacion': observacion,
        'Valor': valor_pagado,
        'Valor_antes_del_movimiento': valor_antes_del_movimiento,
        'Valor_despues_del_movimiento': valor_despues_del_movimiento,
        'En_efectivo': en_efectivo,
        'En_banco': en_banco,
        'Fecha_movimiento': valor_timestamp
    })

    collection_notificaciones.insert_one({'Casa': valor_col1,
                                          'Tipo_Notificacion': 'Pago',
                                          'Fecha': '10/10/2023',
                                          'Estado': 'Pendiente',
                                          'Observaciones': 'Ninguna',
                                          'Recibo':no_recibo})

    for document in collection_personas.find({'Casa': valor_col1}):
        if document['Personas']['Nombres'] == valor_col4:
            correo_envio_residente = (document['correos']['Activo'])
            print(f'Aqui voy por el correo: {correo_envio_residente}')

    #Aqui se llama al metodo para generar el pdf
    generate_pdf_soporte_pago()

    #Aqui se llama al metodo para enviar el correo electronico con el pdf recien generado. 
    envio_correo_pago()

def facturacion():
    """Metodo que me genera la facturacion mes a mes de los residentes"""
    db = conexion_mongo()
    #global casa_facturacion
    global factura_valor_pago
    global numero_recibo
    global factura_fecha
    global factura_tipo
    global pago_encontrado
    global resum_cuotas_pagadas
    global resum_pagos_recibidos
    global resum_ctas_facturadas
    global resum_saldo
    global resumen_cargos_del_mes
    global fecha_facturacion
    global resum_cuotas_pend

    collection_pagos = db.Pagos
    collection_recibos = db.Recibos
    collection_configuracion = db.Configuracion
    collection_estados = db.Estados
    collection_detalle_facturas_tmp = db.Detalle_factura_tmp
    collection_movimientos = db.Movimientos
    collection_notificaciones = db.Notificaciones

    #Tabla configuracion para saber cual es el ultimo recibo generado. 
    consulta_tabla = collection_configuracion.find_one(
        {
            'Ultimo_recibo_factura': {'$gt': 0}
            },
            {'Ultimo_recibo_factura': 1, '_id': 0}             )
    numero_recibo = consulta_tabla['Ultimo_recibo_factura']

    consulta_mes = collection_configuracion.find_one(
        {
            'Estado_mes': 'Activo'
            },
            {'Mes': 1, 'Numero_mes': 1, '_id': 0}
             )
    mes_actual = consulta_mes['Mes']
    numero_mes_actual = consulta_mes['Numero_mes']

    consulta_anno = collection_configuracion.find_one(
        {
            'Estado_anno_actual': 'Activo'
            },
            {'Anno_actual': 1, '_id': 0}
             )
    anno_actual = consulta_anno['Anno_actual']
    fecha_facturacion = '01/'+ str(numero_mes_actual) +'/'+anno_actual

    consulta_val_cuota = collection_configuracion.find_one(
        {
            'Estado_valor_cuota': 'Activo'
            },
            {'Valor_cuota_administracion': 1, '_id': 0}
             )
    valor_cuota = consulta_val_cuota['Valor_cuota_administracion']

    #Punto principal del proceso de facturacion
    for facturacion1 in casas:
        casa_facturacion = facturacion1
        numero_recibo +=1
        #Se inician los valores de las facturas por cada ciclo que se realiza.
        amortizacion = 0
        factura_valor_pago = 0
        resum_cuotas_pagadas = 0
        resum_pagos_recibidos = 0
        resum_ctas_facturadas = 0
        resum_saldo = 0
        resumen_cargos_del_mes = 0
        pago_encontrado = False
        arreglos_zc = False
        cruce_notificaciones = 0
        #valido cual es el estado de la casa
        print(f'Comienza facturacion casa - {casa_facturacion}')

        #Se valida el estado de la casa
        for estados in collection_estados.find({'Casa': casa_facturacion}):
            estado_casa = estados['Estado']
            print(f"Se busca el estado actual de la casa que es {estado_casa}.")

            ultima_factura_casa = estados['Ultima_factura']
            print(f'Ultima factura generada es la {ultima_factura_casa}')
            print(f"El valor pendiente de pago es: {estados['Deuda_pendiente']} ")

            facturas_pendientes_estados = estados['Facturas_pendientes']
            print(f'Facturas pendientes: {facturas_pendientes_estados}')

        for notificacion in collection_notificaciones.find({'Casa': casa_facturacion, 'Estado': 'Pendiente'}):
            if notificacion['Tipo_Notificacion'] == 'Pago':
                pago_encontrado = True
            elif notificacion['Tipo_Notificacion'] == 'Cuota Extraordinaria':
                cuota_extraordinaria = True
            elif notificacion['Tipo_Notificacion'] == 'Arreglos':
                #multa por daño bien ajeno
                arreglos_zc = True

            cruce_notificaciones += 1
            print('Notificación encontrada de pago realizado')

#Comienza a hacer el proceso de cruce de los pagos realizados contra las cuotas pendientes.
        if pago_encontrado:
            #Se busca el pago en la tabla de pagos. 
            for pagos in collection_pagos.find({'Casa': casa_facturacion, 'Estado': 'Pendiente'}):   
    
                resum_pagos_recibidos += pagos['Valor']
                print(f'Se encontro pago realizado en el mes. Recibo {pagos["No Recibo"]}')

                amortizacion = pagos['Valor']
                factura_fecha = pagos['Fecha']

        #ingresare un registro en la tabla de detalle facturas para despues escribirlos en el documento
                concepto = 'Pago recibido ' + pagos['Tipo']
                collection_detalle_facturas_tmp.insert_one({'Casa': casa_facturacion,
                                                            'Referencia': pagos['No Recibo'],
                                                            'Concepto': concepto,
                                                            'Valor': pagos['Valor'],
                                                            'Fecha': pagos['Fecha']
                                                            })
                
                for recibos in collection_recibos.find({'Casa': casa_facturacion, 'Estado': 'Pendiente'}):
        #Se comienza a realizar la amortizacion del pago realizado con la deuda pendiente
                    cruce_notificaciones -=1
                    print(f'El valor de la amortizacion antes: {amortizacion}')
                    amortizacion -= recibos['Valor']
                    print(f'El valor de la amortizacion despues: {amortizacion}')

                    #Comienza la amortizacion del pago realizado.
                    if amortizacion == 0:
                        #Al ser el valor pagado igual al pendiente del recibo, la casa queda al dia.
                        # por el cual este es el unico que sera actualizado
                        #se actualiza la notificación para que no se vuelva a procesar.
                        resum_cuotas_pagadas += 1
                        collection_notificaciones.update_one({  'Casa': casa_facturacion,
                                                                'Estado': 'Pendiente', 
                                                                'Recibo': pagos['No Recibo']},
                                                                {'$set': {'Estado': 'Procesada'}})

                        #se actualiza el estado del recibo.
                        collection_recibos.update_one({'Casa': casa_facturacion,
                                                        'Estado': 'Pendiente',
                                                        'Recibo': recibos['Recibo'] },
                                                    {'$set': {'Estado': 'Pagada'}})                

                        collection_pagos.update_one({'Casa': casa_facturacion,
                                                    'No Recibo': pagos['No Recibo']},
                                                    {'$set': {'Estado': 'Procesada'}})

                        collection_movimientos.insert_one({'Num_pago': pagos['No Recibo'],
                                                        'Valor': pagos['Valor'],
                                                        'Num_recibo': recibos['Recibo'],
                                                        'Valor_recibo': recibos['Valor'],
                                                        'Pendiente_recibo': 0,
                                                        'Saldo_a_favor': 0
                                                        })
                        concepto = 'Cancelacion cuota ' + recibos['Mes']
                        collection_detalle_facturas_tmp.insert_one({'Casa': casa_facturacion,
                                                            'Referencia': recibos['Recibo'],
                                                            'Concepto': concepto,
                                                            'Valor': recibos['Valor'],
                                                            'Fecha': recibos['Fecha']
                                                            })
                        collection_estados.update_one({'Casa':casa_facturacion},
                                                    {'$set': {
                                                        'Estado': 'Al dia',
                                                        'Deuda_pendiente': 0,
                                                        'Ultimo_pago': pagos['No Recibo'],
                                                        'Valor_ultimo_pago': recibos['Valor'],
                                                        'Valor_ultimo_recibo': pagos['Valor']} })
                    elif amortizacion < 0:
#Si amortizacion es negativa significa que el pago no alcanzo a cubrir total del recibo pendiente.
                        amortizacion = amortizacion * (-1)
                        collection_estados.update_one({'Casa':casa_facturacion},
                                                    {'$set': {'Estado': 'En mora',
                                                                'Deuda_pendiente': amortizacion,
                                                                'Ultimo_pago': pagos['No Recibo'],
                                                                'Valor_ultimo_pago': recibos['Valor'],
                                                                'Valor_ultimo_recibo': pagos['Valor']} })
                        collection_recibos.update_one({'Casa': casa_facturacion,
                                                        'Estado': 'Pendiente',
                                                        'Recibo': recibos['Recibo'] },
                                                    {'$set': {
                                                        'Valor': amortizacion
                                                    }})
                        collection_pagos.update_one({'Casa': casa_facturacion,
                                                    'No Recibo': pagos['No Recibo']
                                                    },
                                                    {'$set': {'Estado': 'Procesada'}
                                                    }
                                                    )
                        collection_movimientos.insert_one({'Num_pago': pagos['No Recibo'],
                                                        'Valor': pagos['Valor'],
                                                        'Num_recibo': recibos['Recibo'],
                                                        'Valor_recibo': recibos['Valor'],
                                                        'Pendiente_recibo': amortizacion,
                                                        'Saldo_a_favor': 0
                                                        })
                        concepto = 'Amortización cuota ' + recibos['Mes']
                        collection_detalle_facturas_tmp.insert_one({'Casa': casa_facturacion,
                                                            'Referencia': recibos['Recibo'],
                                                            'Concepto': concepto,
                                                            'Valor': recibos['Valor'],
                                                            'Fecha': recibos['Fecha']
                                                            })
                    elif amortizacion > 0:
#Si amortizacion es mayor que cero, significa que la casa pago mas del valor pendiente
                        #Queda con saldo a favor.
                        resum_cuotas_pagadas += 1
                        collection_recibos.update_one({'Casa': casa_facturacion,
                                                        'Estado': 'Pendiente',
                                                        'Recibo': recibos['Recibo'] },
                                                    {'$set': {
                                                        'Estado': 'Pagada'
                                                    }})
                        collection_movimientos.insert_one({'Num_pago': pagos['No Recibo'],
                                                        'Casa': casa_facturacion,
                                                        'Valor': pagos['Valor'],
                                                        'Num_recibo': recibos['Recibo'],
                                                        'Valor_recibo': recibos['Valor'],
                                                        'Pendiente_recibo': 0,
                                                        'Saldo_a_favor': amortizacion
                                                        })
                        collection_estados.update_one({'Casa':casa_facturacion},
                                                    {'$set': {'Estado': 'Saldo a favor',
                                                                'Deuda_pendiente': 0,
                                                                'Saldo_a_favor': amortizacion,
                                                                'Ultimo_pago': pagos['No Recibo'],
                                                                'Valor_ultimo_pago': recibos['Valor'],
                                                                'Valor_ultimo_recibo': pagos['Valor']} }
                                                        )
                        concepto = 'Cancelación cuota ' + recibos['Mes']
                        collection_detalle_facturas_tmp.insert_one({'Casa': casa_facturacion,
                                                            'Referencia': recibos['Recibo'],
                                                            'Concepto': concepto,
                                                            'Valor': recibos['Valor'],
                                                            'Fecha': recibos['Fecha']
                                                            })
                        collection_pagos.update_one({'Casa': casa_facturacion,
                                                    'No Recibo': pagos['No Recibo']
                                                    },
                                                    {'$set': {'Valor': amortizacion}
                                                    }
                                                    )
                        collection_notificaciones.update_one({'Casa': casa_facturacion, 
                                                              'Recibo': pagos['No Recibo']},
                                                              {'$set': {'Observaciones': 'Por pago mas del pendiente, se creara una nueva notificacion para el mismo pago con el valor pendiente de compensacion',
                                                                        'Estado': 'Procesada'}})
                if cruce_notificaciones > 0:
        #Si cruce_notificaciones es mayor a cero es que hay mas pagos los recibos ya estan pagos.
                    saldo_a_favor = True
                    print("La casa realizo mas de un pago en el mes dejando la casa con saldo a favor")
                    print(f"Amortización: {amortizacion}")
        else:
#Se recorre tabla  recibos para determinar que quedo pendiente para validar el resumen en recibo de pago
            for recibos_pendientes in collection_recibos.find({'Casa': casa_facturacion, 
                                                               'Estado': 'Pendiente'}):
                resum_cuotas_pend += 1
                resum_saldo += recibos_pendientes['Valor']
                concepto = 'Cuota pendiente mes ' + recibos_pendientes['Mes']
                collection_detalle_facturas_tmp.insert_one({'Casa': casa_facturacion,
                                                        'Referencia': recibos_pendientes['Recibo'],
                                                        'Concepto': concepto,
                                                        'Valor': recibos_pendientes['Valor'],
                                                        'Fecha': recibos_pendientes['Fecha']
                                                        })
#ojo - pendiente validar los valores correctos de este
            collection_estados.update_one({'Casa':casa_facturacion},
                                          {'$set': {'Estado': 'En mora',
                                                    'Deuda_pendiente': amortizacion,
                                                    'Ultimo_pago': recibos_pendientes['No Recibo'],
                                                    'Valor_ultimo_pago': recibos['Valor'],
                                                    'Valor_ultimo_recibo': recibos_pendientes['Valor']} })

#Genero el registro de facturacion en la tabla de notificaciones
#toda actividad debe quedar registrada en esa tabla.
        collection_notificaciones.insert_one({"Casa": casa_facturacion,
                                              "Tipo_Notificacion": "Factura",
                                              'Fecha': '2023-10-01',
                                              'Estado': 'Pendiente',
                                              "Observaciones": "Factura generada para el mes",
                                              "Recibo": numero_recibo})

#Validar tabla de notificaciones si existe registro difererente a pago que amerite cargos en el mes

        resumen_cargos_del_mes = valor_cuota
        if saldo_a_favor:
            resum_saldo = amortizacion
        else:
            valor_cuota = valor_cuota - amortizacion

        if cuota_extraordinaria:
            valor_cuota = valor_cuota + valor_cuota_extraordinaria
            concepto="Cuota Extraordinaria"
            collection_detalle_facturas_tmp.insert_one({'Casa': casa_facturacion,
                                                    'Referencia': numero_recibo,
                                                    'Concepto': concepto,
                                                    'Valor': valor_cuota,
                                                    'Fecha': fecha_facturacion
                                                    })

        resum_ctas_facturadas += 1
        concepto = 'Facturación cuota ' + mes_actual
        collection_detalle_facturas_tmp.insert_one({'Casa': casa_facturacion,
                                                    'Referencia': numero_recibo,
                                                    'Concepto': concepto,
                                                    'Valor': valor_cuota,
                                                    'Fecha': fecha_facturacion
                                                    })

        collection_recibos.insert_one({'Casa': casa_facturacion,
                                       'Recibo': numero_recibo,
                                       'Fecha': '2023-10-01',
                                       'Anno': anno_actual,
                                       'Valor': valor_cuota,
                                       'Mes': mes_actual,
                                       'Estado': 'Pendiente'
                                           })
# ojo - Se tiene que actualizar el valor de la ultima cuota en la tabla de configuracion
        #Se genera el documento en pdf para despues ser enviado por correo.
        generate_pdf_cuota()

        #Se borra la tabla temporal para no guardar cosas que no se necesitan.
        collection_detalle_facturas_tmp.delete_many({'Casa': facturacion1})

        #Se envia por correo el documento generado.
        envio_correo_factura()
    # Enviar el documento por correo.

facturacion()
#realizar_pago()
#generate_pdf_cuota()
#generate_pdf_soporte_pago()