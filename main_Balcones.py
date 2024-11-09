from tkinter import *
from tkinter import messagebox, ttk
#librerias para el envio del documento pdf por correo electronico
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
# Librerias para el manejo de las fechas
from datetime import datetime

import os
#import tarfile
# Librerias para la conexión con la base de datos Mongo
from pymongo import MongoClient

# Librerias para la creación del archivo en pdf
from reportlab.pdfgen import canvas

#definicion de la ventana principal
raiz = Tk()
#definición del menu de la aplicación
VarNombres = StringVar
rb_opcion = IntVar()
numero_recibo = StringVar
residentes=[]
residente=[]
lista_pagos=[]
proyecto = 0
factura_valor_pago = 0
numero_recibo = 0
valor_cuota_extraordinaria = 100000
saldo_a_favor = False

#Esto es temporal mientras realizo la consulta a mongo para traer el valor de las casas. 
casas = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14']

def conexion_mongo():
    """Funcion que brinda la conexion con la BD Mongo"""
    #Apertura de la conexión con la BD de Mongo
    cliente = MongoClient('mongodb://localhost:27017/')
    #La Base de Datos se llama Balcones
    db = cliente.Balcones
    return db

def realizar_bkp():
    """Metodo que realiza backup de la base de datos"""

    # Conectarse a la base de datos
    db_name = 'Balcones'
    client = MongoClient("mongodb://localhost:27017")
    db = client.Balcones
    collections = db.list_collection_names()
    
    # Crear un directorio para almacenar los archivos de copia de seguridad
    backup_dir = f'backup_{db_name}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}'
    os.mkdir(backup_dir)

    for collection in collections:
        cursor = db[collection].find()
        print(f'Colección: {collection}')
        with open(f'{backup_dir}/{collection}.json', 'w') as f:
            #f.write('[')
            for document in cursor:
                print(document)
                f.write(f'{document},')
            #f.write(']')

def envio_correo_factura(email, nombre, mes):
    """ Metodo que envia documentos adjuntos por correo electrónico"""
    # Configuración de la cuenta de Gmail
    sender_email = "balconescapellania@gmail.com"
    sender_password = "mfsbwjenunfewdkn"

    # Destinatario
    print(f"El correo es: {email}")
    recipient_email = "german.pemberthy@outlook.com"
    #recipient_email = email

    # Crear el mensaje
    asunto = "Facturación mes " + mes + " Balcones de Capellania."
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = asunto

    # Cuerpo del correo
    body = "Señor residente " + nombre + " la administración envia la factura del mes de " + mes
    message.attach(MIMEText(body, "plain"))

    # Adjuntar el documento
    file_path = "C:/Users/germa/Desktop/SitioWebEducacion/" + "Administracion_Casa_" + casa_facturacion + "_" + str(numero_recibo) + '.pdf'
    # Nombre que tendrá el archivo adjunto en el correo
    filename = 'Administracion_Casa_' + casa_facturacion + "_"+ str(numero_recibo) + '.pdf'
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

def generate_pdf_cuota():
    """Metodo que genera el documento en pdf del pago de la cuota"""
    db = conexion_mongo()
    collection_detalle_factura_tmp = db.Detalle_factura_tmp
    ejey = 0
    # Create the canvas
    nombre_archivo = "Administracion_Casa_" + casa_facturacion + "_" + str(numero_recibo) + ".pdf"
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
    pdf_canvas.drawString(100, 450, casa_facturacion)
    pdf_canvas.setFont("Courier-Bold", 10)
    pdf_canvas.drawString(60, 470, fecha_facturacion)
    pdf_canvas.drawString(190, 470, "Cajica")

    #parte del detalle de los movimientos.
    ejey = 400
    for document in collection_detalle_factura_tmp.find({'Casa': casa_facturacion}):
        valor_tmp = document['Referencia']
        pdf_canvas.drawString(25, ejey, str(valor_tmp))
        valor_tmp = document['Concepto']
        pdf_canvas.drawString(60, ejey, valor_tmp)
        valor_tmp = document['Valor']
        pdf_canvas.drawString(260, ejey, str(valor_tmp))
        pdf_canvas.drawString(253, ejey, '$')
        valor_tmp = document['Fecha']
        pdf_canvas.drawString(325, ejey, str(valor_tmp))
        ejey -= 17

    #llenado de la parte de resumen
    pdf_canvas.setFont("Courier-Bold", 10)
    #resumen_total_a_pagar = resumen_saldo_cuotas_atrasadas + resumen_cargos_del_mes
    resumen_cuotas_pendientes = resumen_cuotas_atrasadas + 1
    pdf_canvas.drawString(138, 140, '$')
    pdf_canvas.drawString(145, 140, str(resumen_valor_pagado))
    pdf_canvas.drawString(145, 125, str(resumen_cuotas_pagadas))
    pdf_canvas.drawString(145, 110, str(resumen_cuotas_atrasadas))
    pdf_canvas.drawString(138, 95, '$')
    pdf_canvas.drawString(145, 95, str(resumen_saldo_cuotas_atrasadas))
    pdf_canvas.drawString(138, 80, '$')
    pdf_canvas.drawString(145, 80, str(resumen_cargos_del_mes))
    pdf_canvas.drawString(145, 65, str(resumen_cuotas_pendientes))
    pdf_canvas.drawString(138, 50, '$')
    pdf_canvas.drawString(145, 50, str(resumen_total_a_pagar))

    # Save the PDF
    pdf_canvas.save()

def novedades():
    """Modulo que gestiona las novedades que se generan con la facturación"""
    print("Ingresa a novedades")

def facturacion():
    """Metodo que me genera la facturacion mes a mes de los residentes"""
    db = conexion_mongo()
    global cruce_notificacion_pago
    global casa_facturacion
    global factura_valor_pago
    global numero_recibo
    global factura_tipo
    global pago_encontrado
    global resumen_cuotas_pagadas
    global resumen_valor_pagado
    global resumen_cuotas_atrasadas
    global resumen_saldo_cuotas_atrasadas
    global resumen_cargos_del_mes
    global resumen_total_a_pagar
    global fecha_facturacion

    collection_pagos = db.Pagos
    collection_recibos = db.Recibos
    collection_configuracion = db.Configuracion
    collection_estados = db.Estados
    collection_detalle_facturas_tmp = db.Detalle_factura_tmp
    collection_movimientos = db.Movimientos
    collection_notificaciones = db.Notificaciones
    collection_personas = db.Personas

#Tabla configuracion para saber cual es el ultimo recibo generado.
    consulta_recibo = collection_configuracion.find_one({
            'Recibo_factura': 'Activo'},
            {'Ultimo_recibo_factura': 1, '_id': 0})
    numero_recibo = consulta_recibo['Ultimo_recibo_factura']

    consulta_mes = collection_configuracion.find_one({
            'Estado_mes': 'Activo'
            },
            {'Mes': 1, 'Numero_mes': 1, '_id': 0})
    mes_actual = consulta_mes['Mes']
    numero_mes_actual = consulta_mes['Numero_mes']

    consulta_anno = collection_configuracion.find_one({
            'Estado_anno_actual': 'Activo'
            },
            {'Anno_actual': 1, '_id': 0})
    anno_actual = consulta_anno['Anno_actual']
    fecha_facturacion = '01-'+ str(numero_mes_actual) + '-'+ anno_actual

    consulta_val_cuota = collection_configuracion.find_one(
        {
            'Estado_valor_cuota': 'Activo'},
            {'Valor_cuota_administracion': 1, '_id': 0})
    valor_cuota = consulta_val_cuota['Valor_cuota_administracion']

    #Punto principal del proceso de facturacion
    for facturacion1 in casas:
        casa_facturacion = facturacion1
        numero_recibo +=1
        #Se inician los valores de las facturas por cada ciclo que se realiza.
        cruce_notificacion_pago = 0
        cruce_facturas_pendientes = 0
        pago_amortizar = 0
        factura_valor_pago = 0
        resumen_cuotas_pagadas = 0
        resumen_valor_pagado = 0
        resumen_cuotas_atrasadas = 0
        resumen_saldo_cuotas_atrasadas = 0
        resumen_cargos_del_mes = 0
        resumen_total_a_pagar = 0
        pago_encontrado = False
        saldo_a_favor = False
        cuota_extraordinaria = False
        arreglos_zc = False
        lista_pagos = []
        #valido cual es el estado de la casa
        print(f'Comienza facturacion casa - {facturacion1}')
#se consulta la informacion de las personas
        for persona in collection_personas.find({"Casa": facturacion1}):
            email = persona['correos']['Activo']
            nombre = persona['Personas']['Nombres']
            print(f"Esta es la persona: {nombre}")
        #Se valida el estado de la casa
        for estados in collection_estados.find({'Casa': facturacion1}):
            estado_casa = estados['Estado']
            print(f"Se busca el estado actual de la casa que es {estado_casa}.")

            ultima_factura_casa = estados['Ultima_factura']
            print(f'Ultima factura generada es la {ultima_factura_casa}')
            print(f"El valor pendiente de pago es: {estados['Deuda_pendiente']} ")

            facturas_pendientes_estados = estados['Facturas_pendientes']
            print(f'Facturas pendientes: {facturas_pendientes_estados}')

        for notificacion in collection_notificaciones.find({'Casa': facturacion1,
                                                            'Estado': 'Pendiente'}):
            if notificacion['Tipo_Notificacion'] == 'Pago':
                pago_encontrado = True
                print('Notificación encontrada de pago realizado')
                cruce_notificacion_pago += 1
            elif notificacion['Tipo_Notificacion'] == 'Factura':
                factura_encontrada = True
                cruce_facturas_pendientes += 1
            elif notificacion['Tipo_Notificacion'] == 'Cuota Extraordinaria':
                cuota_extraordinaria = True
                valor_cuota_extraordinaria = notificacion['Valor']
                print('Notificación encontrada de cuota extraordinaria')
            elif notificacion['Tipo_Notificacion'] == 'Arreglos':
                #multa por daño bien ajeno
                arreglos_zc = True
                valor_arreglos_zonas = notificacion['Valor']
                print('Notificación encontrada de arreglos por daño encontrado')

 #Comienza a hacer el proceso de cruce de los pagos realizados contra las cuotas pendientes.
        if pago_encontrado:
        #Se busca el pago en la tabla de pagos.
            for pagos in collection_pagos.find({'Casa': facturacion1, 'Estado': 'Pendiente'}):
                resumen_valor_pagado += pagos['Valor']
                print(f'Se encontro pago realizado en el mes. Recibo {pagos["No Recibo"]}')
                pago_amortizar = pagos['Valor']
                fecha_pago = str(pagos['Fecha'])
                fecha_objeto = datetime.strptime(fecha_pago[:10], "%Y-%m-%d")
                fecha_pago_formato = fecha_objeto.strftime("%d-%m-%Y")
#ingresare registro en tabla detalle facturas para despues escribirlos en el documento
                concepto = 'Pago recibido ' + pagos['Tipo']
                collection_detalle_facturas_tmp.insert_one({'Casa': facturacion1,
                                                            'Referencia': pagos['No Recibo'],
                                                            'Concepto': concepto,
                                                            'Valor': pagos['Valor'],
                                                            'Fecha': fecha_pago_formato})

                for recibos in collection_recibos.find({'Casa': facturacion1, 'Estado': 'Pendiente'}):
#Se comienza a realizar la amortizacion del pago realizado con la deuda pendiente
                    cruce_notificacion_pago -=1
                    print(f'El valor de la amortizacion antes: {pago_amortizar}')
                    pago_amortizar -= recibos['Valor']
                    print(f'El valor de la amortizacion despues: {pago_amortizar}')
#Comienza la amortizacion del pago realizado.
                    if pago_amortizar == 0:
                        resumen_cuotas_pagadas += 1
                        estado_casa = 'Al Dia'
#Al ser el valor pagado igual al pendiente del recibo, la casa queda al dia.
# Actualizacion de la notificacion de la factura.
                        collection_notificaciones.update_one({
                            'Casa': facturacion1,
                            'Tipo_Notificacion': "Factura",
                            'Estado': 'Pendiente', 
                            'Recibo': recibos['Recibo']},
                            {'$set': {'Estado': 'Procesada'}})
#se actualiza el recibo cambiando estado y el valor a cero.
                        collection_recibos.update_one({
                            'Casa': facturacion1,
                            'Estado': 'Pendiente',
                            'Recibo': recibos['Recibo'] },
                             {'$set': {'Estado': 'Pagada', 
                                        'Valor': 0}})
#Se actualiza el pago
                        collection_pagos.update_one({
                            'Casa': facturacion1,
                            'No Recibo': pagos['No Recibo']},
                            {'$set': {'Estado': 'Procesada',
                                      'Valor': 0}})
#Se actualiza la notificacion de pago realizado
                        collection_notificaciones.update_one({
                            'Casa': facturacion1,
                            'Tipo_Notificacion': "Pago",
                            'Estado': 'Pendiente', 
                            'Recibo': pagos['No Recibo']},
                            {'$set': {'Estado': 'Procesada'}})
#Se ingresa el registro del movimiento realizado
                        collection_movimientos.insert_one({
                            'Num_pago': pagos['No Recibo'],
                            'Valor': pagos['Valor'],
                            'Num_recibo': recibos['Recibo'],
                            'Valor_recibo': recibos['Valor'],
                            'Pendiente_recibo': 0,
                            'Saldo_a_favor': 0 })
                        concepto = 'Cancelacion cuota ' + recibos['Mes']
                        collection_detalle_facturas_tmp.insert_one({
                            'Casa': facturacion1,
                            'Referencia': recibos['Recibo'],
                            'Concepto': concepto,
                            'Valor': recibos['Valor'],
                            'Fecha': fecha_pago_formato})
                        collection_estados.update_one({
                            'Casa':facturacion1},
                            {'$set': {
                                       'Estado': estado_casa,
                                       'Deuda_pendiente': 0,
                                       'Ultimo_pago': pagos['No Recibo'],
                                       'Facturas_pendientes': lista_pagos,
                                       'Valor_ultimo_pago': pagos['Valor'],
                                       'Valor_ultimo_recibo': recibos['Valor']}})
                    elif pago_amortizar < 0:
#Si amortizacion es negativa significa que el pago no alcanzo a cubrir total del recibo pendiente.
                        pago_amortizar = pago_amortizar * (-1)
                        estado_casa = 'En Mora'
                        lista_pagos.append(recibos['Recibo'])
                        collection_estados.update_one({'Casa':facturacion1},
                                                {'$set': {'Estado': estado_casa,
                                                        'Deuda_pendiente': pago_amortizar,
                                                        'Facturas_pendientes': lista_pagos,
                                                        'Saldo_a_favor': 0,
                                                        'Ultimo_pago': pagos['No Recibo'],
                                                        'Valor_ultimo_pago': pagos['Valor'],
                                                        'Valor_ultimo_recibo': recibos['Valor']}})
#El recibo queda con el valor pendiente de pagar.
                        collection_recibos.update_one({'Casa': facturacion1,
                                                        'Estado': 'Pendiente',
                                                        'Recibo': recibos['Recibo'] },
                                                    {'$set': {'Valor': pago_amortizar,}})
#El pago queda en cero totalmente procesado.                         
                        collection_pagos.update_one({'Casa': facturacion1,
                                                    'No Recibo': pagos['No Recibo']},
                                                    {'$set': {'Estado': 'Procesada',
                                                              'Valor': 0}})
#Se actualiza la notificacion de pago realizado
                        collection_notificaciones.update_one({'Casa': facturacion1,
                                                              'Tipo_Notificacion': "Pago",
                                                              'Estado': 'Pendiente', 
                                                              'Recibo': pagos['No Recibo']},
                                                             {'$set': {'Estado': 'Procesada'}})
                        collection_movimientos.insert_one({'Num_pago': pagos['No Recibo'],
                                                        'Valor': pagos['Valor'],
                                                        'Num_recibo': recibos['Recibo'],
                                                        'Valor_recibo': recibos['Valor'],
                                                        'Pendiente_recibo': pago_amortizar,
                                                        'Saldo_a_favor': 0})
                        concepto = 'Amortización cuota ' + recibos['Mes']
                        collection_detalle_facturas_tmp.insert_one({'Casa': facturacion1,
                                                            'Referencia': recibos['Recibo'],
                                                            'Concepto': concepto,
                                                            'Valor': pagos['Valor'],
                                                            'Fecha': fecha_pago_formato})
                    elif pago_amortizar > 0:
#Si amortizacion es mayor a cero, significa pago mas valor del recibo que se esta cruzando
#Queda con saldo a favor, sino tiene mas recibos pendientes de cruzar.
                        saldo_a_favor = True
                        estado_casa = 'Saldo A Favor'
                        resumen_cuotas_pagadas += 1
                        lista_pagos = []
#Se actualiza el recibo a pagado en su totalidad
                        collection_recibos.update_one({'Casa': facturacion1,
                                                        'Estado': 'Pendiente',
                                                        'Recibo': recibos['Recibo'] },
                                                    {'$set': {'Estado': 'Pagada',
                                                              'Valor': 0}})
# Actualizacion de la notificacion de la factura a procesado.
                        collection_notificaciones.update_one({'Casa': facturacion1,
                                                              'Tipo_Notificacion': "Factura",
                                                              'Estado': 'Pendiente', 
                                                              'Recibo': recibos['Recibo']},
                                                             {'$set': {'Estado': 'Procesada'}})
#Se actualiza el pago
                        collection_pagos.update_one({'Casa': facturacion1,
                                                    'No Recibo': pagos['No Recibo']},
                                                    {'$set': {'Valor': pago_amortizar}})
                        collection_notificaciones.update_one({'Casa': facturacion1,
                                                              'Tipo_Notificacion': "Pago",
                                                              'Recibo': pagos['No Recibo']},
                                                              {'$set': {
                                                            'Observaciones': 'Notificación con saldo a favor'}})
#Se ingresa el movimiento
                        collection_movimientos.insert_one({'Num_pago': pagos['No Recibo'],
                                                        'Casa': facturacion1,
                                                        'Valor': pagos['Valor'],
                                                        'Num_recibo': recibos['Recibo'],
                                                        'Valor_recibo': recibos['Valor'],
                                                        'Pendiente_recibo': 0,
                                                        'Saldo_a_favor': pago_amortizar})
                        collection_estados.update_one({'Casa':facturacion1},
                                                    {'$set': {'Estado': estado_casa,
                                                            'Deuda_pendiente': 0,
                                                            'Facturas_pendientes': lista_pagos,
                                                            'Saldo_a_favor': pago_amortizar,
                                                            'Ultimo_pago': pagos['No Recibo'],
                                                            'Valor_ultimo_pago': pagos['Valor'],
                                                            'Valor_ultimo_recibo': recibos['Valor']}})
                        concepto = 'Cancelación cuota ' + recibos['Mes']
                        collection_detalle_facturas_tmp.insert_one({'Casa': facturacion1,
                                                            'Referencia': recibos['Recibo'],
                                                            'Concepto': concepto,
                                                            'Valor': recibos['Valor'],
                                                            'Fecha': fecha_pago_formato})
                if cruce_notificacion_pago > 0:
#Si cruce_notificacion_pago es mayor a cero significa que realizaron mas de un pago en el mes
#y los recibos pendientes ya estan pagos.
                    saldo_a_favor = True
                    print("La casa realizo mas de un pago en el mes no teniendo recibos contra que cruzar, dejando casa con saldo a favor")
                    print(f"Amortización: {pago_amortizar}")
        else:
#Como no se encontraron pagos se recorre la tabla de recibos para generar la respectiva factura
            estado_casa = 'En Mora'
            for recibos in collection_recibos.find({'Casa': facturacion1, 'Estado': 'Pendiente'}):
                resumen_cuotas_atrasadas += 1
                recibo = recibos['Recibo']
                valor_recibo = recibos['Valor']
                lista_pagos.append(recibos['Recibo'])
                resumen_saldo_cuotas_atrasadas += recibos['Valor']
                concepto = 'Cuota pendiente mes ' + recibos['Mes']
                collection_detalle_facturas_tmp.insert_one({'Casa': facturacion1,
                                                        'Referencia': recibo,
                                                        'Concepto': concepto,
                                                        'Valor': valor_recibo,
                                                        'Fecha': recibos['Fecha']})
#se ingresa el registro en la tabla de estados
            collection_estados.update_one(
                {'Casa':facturacion1},
                {'$set': {'Estado': estado_casa,
                          'Ultima_factura': numero_recibo,
                          'Deuda_pendiente': resumen_saldo_cuotas_atrasadas,
                          'Facturas_pendientes': lista_pagos,
                          'Saldo_a_favor': 0} })

#Conceptos facturables
        if cuota_extraordinaria:
            concepto="Cuota Extraordinaria"
            collection_detalle_facturas_tmp.insert_one({'Casa': casa_facturacion,
                                                    'Referencia': numero_recibo,
                                                    'Concepto': concepto,
                                                    'Valor': valor_cuota_extraordinaria,
                                                    'Fecha': fecha_facturacion})
            resumen_cargos_del_mes += valor_cuota_extraordinaria
        else:
            resumen_cargos_del_mes = valor_cuota
        if arreglos_zc:
            concepto = 'Arreglo daño zonas comunes'
            collection_detalle_facturas_tmp.insert_one({'Casa': casa_facturacion,
                                                    'Referencia': numero_recibo,
                                                    'Concepto': concepto,
                                                    'Valor': valor_arreglos_zonas,
                                                    'Fecha': fecha_facturacion})
            resumen_cargos_del_mes += valor_arreglos_zonas
#Genero el registro de la factura en la tabla de recibos
        concepto = 'Facturación cuota ' + mes_actual
        collection_detalle_facturas_tmp.insert_one({'Casa': facturacion1,
                                                    'Referencia': numero_recibo,
                                                    'Concepto': concepto,
                                                    'Valor': valor_cuota,
                                                    'Fecha': fecha_facturacion})
#Se ingresa el registro en la tabla de recibos
        collection_recibos.insert_one({'Casa': facturacion1,
                                       'Recibo': numero_recibo,
                                       'Fecha': fecha_facturacion,
                                       'Anno': anno_actual,
                                       'Valor': resumen_cargos_del_mes,
                                       'Mes': mes_actual,
                                       'Estado': 'Pendiente'})
#Genero el registro de facturacion en la tabla de notificaciones tipo Factura
        observaciones = "Factura generada para el mes de " + mes_actual
        collection_notificaciones.insert_one({"Casa": casa_facturacion,
                                              "Tipo_Notificacion": "Factura",
                                              'Fecha': fecha_facturacion,
                                              'Estado': 'Pendiente',
                                              "Observaciones": observaciones,
                                              'Valor': resumen_cargos_del_mes,
                                              "Recibo": numero_recibo})
#Deducciones del valor
        if saldo_a_favor:
            print("La casa no cuenta con saldo a Favor")
            resumen_total_a_pagar = resumen_cargos_del_mes - pago_amortizar
        else:
            resumen_total_a_pagar = resumen_cargos_del_mes + pago_amortizar + resumen_saldo_cuotas_atrasadas
#Se genera el documento en pdf para despues ser enviado por correo.
        generate_pdf_cuota()

        #Se borra la tabla temporal para no guardar cosas que no se necesitan.
        collection_detalle_facturas_tmp.delete_many({'Casa': facturacion1})

        #Se envia por correo el documento generado.
        messagebox.showinfo(title = "Mensaje", message = "Validar facturación")
        envio_correo_factura(email, nombre, mes_actual)
        #collection_configuracion.update_one({'_id': '6515bca231889efb2c584c42'},
        #                                    {'$set': {"Ultimo_recibo_factura": numero_recibo}} )
        collection_configuracion.update_one({"Recibo_factura": 'Activo'},
                                            {'$set': {"Ultimo_recibo_factura": numero_recibo}})
        print(f"Ultimo numero de recibo: {numero_recibo}")
    # Enviar el documento por correo.

def generate_pdf_soporte_pago():
    """Metodo que genera formato de soporte de pago"""
    # Create the canvas

    valor_residente = combo_residente.get()
    valor_col5 = combo_casa.get()
    valor_col6 = val_pago.get()
    fecha_pago = pago_fecha.get()
    valor_col8 = val_concepto.get()
    valor_col9 = val_numtrans.get()
    valor_col10 = val_banco.get()

    nombre_fichero = 'Recibo_' + str(numero_recibo) + '.pdf'
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
    pdf_canvas.drawString(310, 200, str(numero_recibo))

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
    pdf_canvas.drawString(95, 220, str(fecha_pago))
    pdf_canvas.drawString(95, 200, "Cajicá")
    pdf_canvas.setFont("Courier-Bold", 14)
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

def envio_correo_pago():
    """ Metodo que envia documentos adjuntos por correo electrónico"""
    # Configuración de la cuenta de Gmail
    global correo_envio_residente
    valor_residente = combo_residente.get()

    sender_email = "balconescapellania@gmail.com"
    sender_password = "mfsbwjenunfewdkn"

    # Destinatario
    recipient_email = "german.pemberthy@outlook.com"
    #recipient_email = correo_envio_residente

    # Crear el mensaje
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "Prueba de envio"

    # Cuerpo del correo
    body = "Señor/a residente " + valor_residente + " la administración envia en el adjunto el comprobante del ultimo pago realizado"
    message.attach(MIMEText(body, "plain"))

    # Adjuntar el documento
    # Reemplaza con la ruta de tu documento
    file_path = "C:/Users/germa/Desktop/SitioWebEducacion/"+'Recibo_' + str(numero_recibo) + '.pdf'
    #Nombre que tendrá el archivo adjunto en correo
    filename = 'Recibo_' + str(numero_recibo) + '.pdf'
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
        messagebox.showinfo(title = "Mensaje", 
                            message = "Pago realizado con exito \n Correo enviado con éxito")
        print("Correo enviado con éxito")

    except Exception as envio1:
        messagebox.showinfo(title = "Mensaje de error", message = "Error al enviar el correo:")
        print(f"Error al enviar el correo: {str(envio1)}")

    finally:
        # Cerrar la conexión con el servidor
        server.quit()

def consulta_residente(event, combo_casa):
    """Funcion para la consulta de residentes"""

    for i in mi_arbol.get_children():
        mi_arbol.delete(i)

    seleccion = combo_casa.get()
    db = conexion_mongo()

    collection_recibos = db.Recibos
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
            residente.append(document['Personas']['Nombres']+' '+document['Personas']['Apellidos'])
    combo_residente["values"]=residente
    combo_residente.config(state='enabled', justify=CENTER)
    residente.clear()

    #Aca se buscan los recibos que estan pendientes de pago para mostrarlos en pantalla.

    for document in collection_recibos.find({'Casa': seleccion, 'Estado': 'Pendiente'}):
        valor_col1 = document['Recibo']
        valor_col2 = 'Recibo'
        valor_col3 = 'Pendiente'
        valor_col4 = document['Valor']
        valor_col5 = document['Mes']
        valor_col6 = document['Anno']
        mi_arbol.insert('', 'end', values=(valor_col1, valor_col2, valor_col3, valor_col4, valor_col5, valor_col6))

def realizar_pago():
    """Metodo para gestionar pago ingresado por el front"""

    global tipo
    global numero_recibo
    valor_pendiente_pago = 0
    valor_timestamp = datetime.now()
    valor_col1 = combo_casa.get()
    valor_col2 = val_pago.get()
    valor_pagado = int(valor_col2)
    valor_col3 = pago_fecha.get()
    valor_col4 = combo_residente.get()
    valor_col5 = val_concepto.get()
    valor_col6 = rb_opcion.get()
    numtrans = val_numtrans.get()
    valor_col8 = val_banco.get()

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
        numero_recibo_actual = document['No Recibo']

    numero_recibo = numero_recibo_actual + 1
    fecha_pago = str(valor_timestamp)
    fecha_objeto = datetime.strptime(fecha_pago[:10], "%Y-%m-%d")
    fecha_pago_formato = fecha_objeto.strftime("%d-%m-%Y")
    collection_pagos.insert_one({'No Recibo': numero_recibo,
                                 'Casa': valor_col1, 
                                 'Fecha': valor_timestamp,
                                 'Anno': int(anno_actual),
                                 'Valor': valor_pagado,
                                 'Tipo': tipo,
                                 'Observaciones': valor_col5,
                                 'Recibi De': valor_col4,
                                 'Numero_transaccion': numtrans,
                                 'Banco': valor_col8,
                                 'Estado': 'Pendiente'})

    mi_arbol.insert('', 'end', values=(numero_recibo, 'Pago', 'Pendiente', valor_pagado, valor_col3, anno_actual))

    collection_configuracion.update_one({'Ultimo_recibo_pago': numero_recibo_actual},
                                        {'$set': {'Ultimo_recibo_pago': numero_recibo }})

    collection_eventos.update_one({'Identificador': 4},{'$set': {'Valor': numero_recibo}})

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
        'Fecha_movimiento': valor_timestamp})

    collection_notificaciones.insert_one({'Casa': valor_col1,
                                          'Tipo_Notificacion': 'Pago',
                                          'Fecha': fecha_pago_formato,
                                          'Estado': 'Pendiente',
                                          'Valor': valor_pagado,
                                          'Observaciones': 'Ninguna',
                                          'Recibo':numero_recibo})

    for document in collection_personas.find({'Casa': valor_col1}):
        if document['Personas']['Nombres'] == valor_col4:
            correo_envio_residente = document['correos']['Activo']
            print(f'Aqui voy por el correo: {correo_envio_residente}')

    #Aqui se llama al metodo para generar el pdf
    generate_pdf_soporte_pago()

    #Aqui se llama al metodo para enviar el correo electronico con el pdf recien generado.
    envio_correo_pago()

def registrar_pagos():
    """ Ventana para registrar en la base de datos los pagos realizados """
    #Se limpia los widgets que se encuentren en el frame previemante.
    for widget in frame4.winfo_children():
        widget.destroy()

    global combo_casa
    Label(frame4, text="Casa", anchor='center').grid(row=0, column=0)
    combo_casa = ttk.Combobox(frame4, values=casas)
    combo_casa.grid(row=1, column=0, padx=20, pady=10)
    combo_casa.config(width=15, justify=CENTER)
    combo_casa.bind("<<ComboboxSelected>>", lambda event: consulta_residente(event, combo_casa))

    global combo_residente
    Label(frame4, text = "Recibi de: ", anchor='e').grid(row=0, column=1)
    combo_residente = ttk.Combobox(frame4)
    combo_residente.grid(row=1, column=1, padx=5, pady=10)
    combo_residente.config(width=35, state='disabled')

    global val_pago
    Label(frame4, text="Valor pagado: ").grid(row=0,column=2)
    val_pago = Entry(frame4)
    val_pago.config(width=20, justify=CENTER)
    val_pago.grid(row=1, column=2, padx=8, pady=10)

    global pago_fecha
    Label(frame4, text="Fecha del pago:").grid(row=0,column=3)
    pago_fecha = Entry(frame4)
    pago_fecha.grid(row=1, column=3, padx=10, pady=10)
    pago_fecha.config(justify=CENTER)

    global val_concepto
    Label(frame4, text='Observaciones:').grid(row=2,column=0)
    val_concepto = Entry(frame4)
    val_concepto.maxlimit = 10
    val_concepto.grid(row=2, column=1, columnspan=3, padx=5, pady=10)
    val_concepto.config(width=82)

    global val_banco
    Label(frame4, text='Banco:').grid(row=3,column=0)
    val_banco=Entry(frame4)
    val_banco.config(width=35)
    val_banco.grid(row=3,column=1, padx=3, pady=10)

    global val_numtrans
    Label(frame4, text='Numero: ').grid(row=3,column=2)
    val_numtrans=Entry(frame4)
    val_numtrans.config(width=20)
    val_numtrans.grid(row=3,column=3, padx=5,pady=10)

    global rb1, rb2, rb3
    rb1= Radiobutton(frame4, text="Efectivo", variable= rb_opcion, value=1 )
    rb1.grid(row=4, column=0, pady=10)
    rb2= Radiobutton(frame4, text="Consignacion", variable=rb_opcion, value=2 )
    rb2.grid(row=4, column=1, pady=10)
    rb3= Radiobutton(frame4, text="Transferencia", variable=rb_opcion, value=3 )
    rb3.grid(row=4, column=2, pady=10)
    rb_opcion.set(1)

    boton_agregar = Button(frame4, text="Pagar", command=realizar_pago)
    boton_agregar.grid(row=5, column=0, columnspan=4, sticky= W+E,pady=10)
    boton_agregar.config(fg='black', bg='#158645', cursor='hand2', activebackground='yellow')

    #Tabla
    global mi_arbol
    mi_arbol = ttk.Treeview(frame4, height=5, columns=('Col1', 'Col2', 'Col3', 'Col4', 'Col5', 'Col6'))
    mi_arbol.grid(row=6, column=0, columnspan=4, pady=10)
    mi_arbol.heading('#0', text="Id")
    mi_arbol.heading('Col1', text="Recibo")
    mi_arbol.heading('Col2', text="Tipo")
    mi_arbol.heading('Col3', text="Estado")
    mi_arbol.heading('Col4', text="Valor Recibo")
    mi_arbol.heading('Col5', text="Mes")
    mi_arbol.heading('Col6', text="Año")
    mi_arbol.column('#0', width=45)
    mi_arbol.column('Col1', width=70, anchor='center')
    mi_arbol.column('Col2', width=110, anchor='center')
    mi_arbol.column('Col3', width=130, anchor='center')
    mi_arbol.column('Col4', width=110, anchor='center')
    mi_arbol.column('Col5', width=90, anchor='center')
    mi_arbol.column('Col6', width=90, anchor='center')

def consultar_movimientos():
    """Metodo que abre ventana emergente, permite consultar los ultimos pagos realizados"""
    for widget in frame4.winfo_children():
        widget.destroy()

    #ventana_emergente_pagos = Toplevel()
    #ventana_emergente_pagos.title("  Ventana Pagos  ")
    global combo_casa
    Label(frame4, text="Casa", anchor='center').grid(row=0, column=0)
    combo_casa = ttk.Combobox(frame4, values=casas)
    combo_casa.grid(row=1, column=0, padx=20, pady=10)
    combo_casa.config(width=15, justify=CENTER)
    combo_casa.bind("<<ComboboxSelected>>", lambda event: consulta_residente(event, combo_casa))

    global mi_arbol
    mi_arbol = ttk.Treeview(frame4, height=5, columns=('Col1', 'Col2', 'Col3', 'Col4', 'Col5'))
    mi_arbol.grid(row=6, column=0, columnspan=4, pady=10)
    mi_arbol.heading('#0', text="Id")
    mi_arbol.heading('Col1', text="Recibo")
    mi_arbol.heading('Col2', text="Estado")
    mi_arbol.heading('Col3', text="Valor Recibo")
    mi_arbol.heading('Col4', text="Mes")
    mi_arbol.heading('Col5', text="Año")
    mi_arbol.column('#0', width=45)
    mi_arbol.column('Col1', width=90, anchor='center')
    mi_arbol.column('Col2', width=130, anchor='center')
    mi_arbol.column('Col3', width=180, anchor='center')
    mi_arbol.column('Col4', width=90, anchor='center')
    mi_arbol.column('Col5', width=110, anchor='center')

def menu_pagos():
    """Metodo que expone el boton para guardar un pago en la Base de datos"""
    frame = LabelFrame(raiz, text="  Modulo Pagos   ")
    frame.config(width=100, height=100)
    frame.grid(row=0, column=0, padx=15, pady=10)
    #  -- Pagos  --
    #Label(frame, text="Registrar Pagos").grid(row=1, column=0)
    boton1 = Button(frame, text="Registrar Pagos", width=15, command=registrar_pagos)
    boton1.grid(row=2, column=0, sticky= W+E, padx=5, pady=5)
    boton1.config(fg='black', bg='#158645', cursor='hand2', activebackground='yellow')

    boton2 = Button(frame,text="Consultar Movimientos", command=consultar_movimientos)
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

    Label(frame4,
          text="Espacio para registrar todos los movimientos de un proyecto").grid(row=0, column=0)
    Button(frame4, text="prueba").grid(row=1, column=1)

def menu_proyectos():
    """Metodo que ejecuta la pantalla principal"""
    frame3 = LabelFrame(raiz, text="  Modulo Proyectos   ")
    #frame3.config(width=100, height=100, bg="green")
    frame3.config(width=130, height=100)
    frame3.grid(row=2, column=0, padx=10, pady=10)
    #  -- Proyectos  --

    Button(frame3, text="Crear Proyecto", width=15,
           command=crear_proyecto).grid(row=0, column=0, sticky= W+E, padx=5, pady=5)

    Button(frame3, text="Registrar Movimientos", width=18,
           command=registrar_proyecto).grid(row=1, column=0, sticky= W+E, padx=5, pady=5)

    Button(frame3,text="Consultar Proyecto",
           command=consultar_proyecto).grid(row=4, columnspan=2, padx= 5, pady=5, sticky= W+E)

    Button(frame3,text="Cuenta de Cobro",
           command=consultar_proyecto).grid(row=5, columnspan=2, padx= 5, pady=5, sticky= W+E)

def ventana():
    """Metodo que crea la ventana principal de la aplicación"""
    global frame4
    raiz.title("Balcones de Capellania")
    raiz.geometry("880x440")
    barra_menu = Menu(raiz)
    menu_bancos = Menu(barra_menu, tearoff=0)
    menu_facturacion = Menu(barra_menu, tearoff=0)
    menu_configuracion = Menu(barra_menu, tearoff=0)
    #Componentes del menu
    barra_menu.add_cascade(label="Bancos", menu=menu_bancos)
    barra_menu.add_cascade(label="Facturación", menu=menu_facturacion)
    barra_menu.add_cascade(label="Configuracion", menu=menu_configuracion)

    menu_bancos.add_command(label="Estado Bancos")

    menu_facturacion.add_command(label="Generar facturación", command=facturacion)
    menu_facturacion.add_command(label="Ingresar Novedad", command=novedades)

    menu_configuracion.add_command(label="Backup Completo", command=realizar_bkp)

    raiz.config(menu=barra_menu)
    
    frame4 = LabelFrame(raiz, text=" CUADRO PRINCIPAL ")
    frame4.grid(row=0, column=1, rowspan=4)
    frame4.config(width=680, height=400)

ventana()

menu_pagos()

menu_personas()

menu_proyectos()

raiz.mainloop()
""" Fin del proceso"""