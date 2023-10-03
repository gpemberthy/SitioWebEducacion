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
# Librerias para la conexión con la base de datos Mongo
from pymongo import MongoClient
# Librerias para la creación del archivo en pdf
from reportlab.pdfgen import canvas


#definicion de la ventana principal
raiz = Tk()
#definición del menu de la aplicación
VarNombres = StringVar
rb_opcion = IntVar()
residentes=[]
residente=[]
lista_pagos=[]
proyecto = 0
#Esto es temporal mientras realizo la consulta a mongo para traer el valor de las casas. 
casas = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14']

def conexion_mongo():
    """Funcion que brinda la conexion con la BD Mongo"""
    #Apertura de la conexión con la BD de Mongo
    cliente = MongoClient('mongodb://localhost:27017/')
    #La Base de Datos se llama Balcones
    db = cliente.Balcones
    return db

def generate_pdf_cuota():
    
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
    pdf_canvas.setFillColorRGB(210/255, 255/255, 210/255) 
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
    pdf_canvas.drawString(50, 450, "Casa No:")
    pdf_canvas.setFont("Times-Bold", 12)
    pdf_canvas.drawString(25, 420, "Ref          Concepto                                               Valor          Fecha")
    pdf_canvas.drawString(25, 160, "Resumen")

    pdf_canvas.setFont("Courier-Bold", 10)
    pdf_canvas.drawString(25, 140, "Pagos Recibidos")
    pdf_canvas.drawString(25, 125, "Cuotas pagadas")
    pdf_canvas.drawString(25, 110, "Cuotas atrasadas")
    pdf_canvas.drawString(25, 95, "Saldo en mora")
    pdf_canvas.drawString(25, 80, "Cargos del mes")
    pdf_canvas.drawString(25, 65, "Cuotas facturadas")
    pdf_canvas.drawString(25, 50, "Total a pagar")

    pdf_canvas.setFont("Courier-Oblique", 7.5)
    pdf_canvas.drawString(25, 30, """
            Para pagos Numero de cuenta de Ahorros Banco Davivienda:  462500020963
                          """)
    pdf_canvas.drawString(25, 20, "Este es su cuota de administración para pago en los 5 primeros dias del mes")
    
    #llenado de la informacion
    pdf_canvas.setFont("Courier-Bold", 14)
    pdf_canvas.drawString(100, 450, casa_facturacion)
    pdf_canvas.setFont("Courier-Bold", 10)
    pdf_canvas.drawString(60, 470, fecha_facturacion)
    pdf_canvas.drawString(195, 470, "Cajica")

    #parte del detalle de los movimientos.
    ejey = 400    
    for document in collection_Detalle_factura_tmp.find({'Casa': casa_facturacion}):
        valor_tmp = document['Referencia']
        pdf_canvas.drawString(25, ejey, str(valor_tmp))
        valor_tmp = document['Concepto']
        pdf_canvas.drawString(60, ejey, valor_tmp)
        valor_tmp = document['Valor']
        pdf_canvas.drawString(260, ejey, str(valor_tmp))
        pdf_canvas.drawString(325, ejey, "02/09/2023")
        ejey -= 19

    #llenado de la parte de resumen
    pdf_canvas.setFont("Courier-Bold", 10)
    resumen_total_a_pagar = resumen_saldo_cuotas_atrasadas + resumen_cargos_del_mes
    resumen_cuotas_pendientes = resumen_cuotas_atrasadas + 1 
    pdf_canvas.drawString(175, 140, str(resumen_valor_pagado))
    pdf_canvas.drawString(175, 125, str(resumen_cuotas_pagadas))
    pdf_canvas.drawString(175, 110, str(resumen_cuotas_atrasadas))
    pdf_canvas.drawString(175, 95, str(resumen_saldo_cuotas_atrasadas))
    pdf_canvas.drawString(175, 80, str(resumen_cargos_del_mes))
    pdf_canvas.drawString(175, 65, str(resumen_cuotas_pendientes))
    pdf_canvas.drawString(175, 50, str(resumen_total_a_pagar))

    # Save the PDF
    pdf_canvas.save()
    #Borramos la tabla temporal para que no vuelvan a aparecer
    collection_Detalle_factura_tmp.delete_many({})

def facturacion():
    """Metodo que me genera la facturacion mes a mes de los residentes"""
    db = conexion_mongo()
    global casa_facturacion
    global factura_valor_pago
    global numero_recibo
    global factura_fecha
    global factura_tipo
    global pago_encontrado
    global resumen_cuotas_pagadas
    global resumen_valor_pagado
    global resumen_cuotas_atrasadas
    global resumen_saldo_cuotas_atrasadas
    global resumen_cargos_del_mes
    global fecha_facturacion

    collection_pagos = db.Pagos
    collection_recibos = db.Recibos
    collection_configuracion = db.Configuracion
    collection_estados = db.Estados
    collection_detalle_facturas_tmp = db.Detalle_factura_tmp
    collection_movimientos = db.Movimientos
    
    #Tabla configuracion para saber cual es el ultimo recibo generado. 
    consulta_tabla = collection_configuracion.find_one(
        {
            'Ultimo_recibo_factura': {'$gt': 0}
            },
            {'Ultimo_recibo_factura': 1, '_id': 0}
             )
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
        resumen_cuotas_pagadas = 0
        resumen_valor_pagado = 0
        resumen_cuotas_atrasadas = 0
        resumen_saldo_cuotas_atrasadas = 0
        resumen_cargos_del_mes = 0
        pago_encontrado = False
        #valido cual es el estado de la casa
        print(f'Comienza facturacion casa - {facturacion1}')
        
        #Se valida el estado de la casa
        for estados in collection_estados.find({'Casa': facturacion1}):
            estado_casa = estados['Estado']
            print(f"Se busca el estado actual de la casa que es {estado_casa}.")
            
            ultima_factura_casa = estados['Ultima_factura']
            print(f'Ultima factura generada es la {ultima_factura_casa}')
            print(f"El valor pendiente de pago es: {estados['Deuda_pendiente']} ")
            
            facturas_pendientes_estados = estados['Facturas_pendientes']
            print(f'Facturas pendientes: {facturas_pendientes_estados}')
        
        #Si ingresa al for es que encontro un pago realizado dentro del mes
        #Este for tambien comienza a hacer el proceso de cruce de los pagos realizados contra las cuotas pendientes.
        for document in collection_pagos.find({'Casa': facturacion1, 'Estado': 'Pendiente'}):   
            pago_encontrado = True
            resumen_cuotas_pagadas += 1
            resumen_valor_pagado += document['Valor']
            print('Se encontro pago realizado en el mes.')
            
            amortizacion = document['Valor']
            factura_fecha = document['Fecha']

            #ingresare un registro en la tabla de detalle facturas para despues escribirlos en el documento
            concepto = 'Pago recibido ' + document['Tipo']
            collection_detalle_facturas_tmp.insert_one({'Casa': facturacion1,
                                                        'Referencia': document['No Recibo'],
                                                        'Concepto': concepto,
                                                        'Valor': document['Valor'],
                                                        'Fecha': document['Fecha']
                                                        })
            
            for document1 in collection_recibos.find({'Casa': facturacion1, 'Estado': 'Pendiente'}):

                #Se comienza a realizar la amortizacion del pago realizado con la deuda pendiente
                print(f'El valor de la amortizacion antes: {amortizacion}')
                amortizacion -= document1['Valor']
                print(f'El valor de la amortizacion despues: {amortizacion}')
            
                #Comienza la amortizacion del pago realizado.
                if amortizacion == 0:
                    #Al estar al dia solo debe tener un recibo pendiente de pago por el cual este es el unico que sera 
                    #actualizado
                    collection_recibos.update_one({'Casa': facturacion1,
                                                    'Estado': 'Pendiente',
                                                    'Recibo': document1['Recibo'] },
                                                {'$set': {
                                                    'Estado': 'Pagada'
                                                }})                  
                    collection_pagos.update_one({'Casa': facturacion1,
                                                'No Recibo': document['No Recibo']
                                                },
                                                {'$set': {'Estado': 'Procesada'}
                                                }
                                                )
                    collection_movimientos.insert_one({'Num_pago': document['No Recibo'],
                                                    'Valor': document['Valor'],
                                                    'Num_recibo': document1['Recibo'],
                                                    'Valor_recibo': document1['Valor'],
                                                    'Pendiente_recibo': 0,
                                                    'Saldo_a_favor': 0
                                                    })                
                    concepto = 'Cancelacion cuota ' + document1['Mes']
                    collection_detalle_facturas_tmp.insert_one({'Casa': facturacion1,
                                                        'Referencia': document1['Recibo'],
                                                        'Concepto': concepto,
                                                        'Valor': document1['Valor'],
                                                        'Fecha': document1['Fecha']
                                                        })
                    collection_estados.update_one({'Casa':facturacion1},
                                                  {'$set': {'Estado': 'Al dia',
                                                            'Deuda_pendiente': 0,
                                                            'Ultimo_pago': document['No Recibo'],
                                                            'Valor_ultimo_pago': document1['Valor'],
                                                            'Valor_ultimo_recibo': document['Valor']} }
                                                  )
                elif amortizacion < 0:
                    amortizacion = amortizacion * (-1)
                    collection_estados.update_one({'Casa':facturacion1},
                                                  {'$set': {'Estado': 'En mora',
                                                            'Deuda_pendiente': amortizacion,
                                                            'Ultimo_pago': document['No Recibo'],
                                                            'Valor_ultimo_pago': document1['Valor'],
                                                            'Valor_ultimo_recibo': document['Valor']} }
                                                    )
                    collection_recibos.update_one({'Casa': facturacion1,
                                                    'Estado': 'Pendiente',
                                                    'Recibo': document1['Recibo'] },
                                                {'$set': {
                                                    'Valor': amortizacion
                                                }})
                    collection_pagos.update_one({'Casa': facturacion1,
                                                'No Recibo': document['No Recibo']
                                                },
                                                {'$set': {'Estado': 'Procesada'}
                                                }
                                                )
                    collection_movimientos.insert_one({'Num_pago': document['No Recibo'],
                                                    'Valor': document['Valor'],
                                                    'Num_recibo': document1['Recibo'],
                                                    'Valor_recibo': document1['Valor'],
                                                    'Pendiente_recibo': amortizacion,
                                                    'Saldo_a_favor': 0
                                                    })
                    concepto = 'Amortización cuota ' + document1['Mes']
                    collection_detalle_facturas_tmp.insert_one({'Casa': facturacion1,
                                                        'Referencia': document1['Recibo'],
                                                        'Concepto': concepto,
                                                        'Valor': document1['Valor'],
                                                        'Fecha': document1['Fecha']
                                                        })
                elif amortizacion > 0:
                    collection_recibos.update_one({'Casa': facturacion1,
                                                    'Estado': 'Pendiente',
                                                    'Recibo': document1['Recibo'] },
                                                {'$set': {
                                                    'Estado': 'Pagada'
                                                }})
                    collection_movimientos.insert_one({'Num_pago': document['No Recibo'],
                                                    'Valor': document['Valor'],
                                                    'Num_recibo': document1['Recibo'],
                                                    'Valor_recibo': document1['Valor'],
                                                    'Pendiente_recibo': 0,
                                                    'Saldo_a_favor': amortizacion
                                                    })
                    collection_estados.update_one({'Casa':facturacion1},
                                                  {'$set': {'Estado': 'Saldo a favor',
                                                            'Deuda_pendiente': 0,
                                                            'Saldo_a_favor': amortizacion,
                                                            'Ultimo_pago': document['No Recibo'],
                                                            'Valor_ultimo_pago': document1['Valor'],
                                                            'Valor_ultimo_recibo': document['Valor']} }
                                                    )
                    concepto = 'Cancelación cuota ' + document1['Mes']
                    collection_detalle_facturas_tmp.insert_one({'Casa': facturacion1,
                                                        'Referencia': document1['Recibo'],
                                                        'Concepto': concepto,
                                                        'Valor': document1['Valor'],
                                                        'Fecha': document1['Fecha']
                                                        })
                    collection_pagos.update_one({'Casa': facturacion1,
                                                'No Recibo': document['No Recibo']
                                                },
                                                {'$set': {'Valor': amortizacion}
                                                }
                                                )
        
        for document in collection_recibos.find({'Casa': facturacion1, 'Estado': 'Pendiente'}):
            resumen_cuotas_atrasadas += 1
            resumen_saldo_cuotas_atrasadas += document['Valor']
            concepto = 'Cuota pendiente mes ' + document['Mes']
            collection_detalle_facturas_tmp.insert_one({'Casa': facturacion1,
                                                    'Referencia': document['Recibo'],
                                                    'Concepto': concepto,
                                                    'Valor': document['Valor'],
                                                    'Fecha': document['Fecha']
                                                    })

        #Genero el registro de la factura en la tabla de recibos
        resumen_cargos_del_mes = valor_cuota - amortizacion
        collection_recibos.insert_one({'Casa': facturacion1,
                                       'Recibo': numero_recibo,
                                       'Fecha': '2023-10-01',
                                       'Anno': anno_actual,
                                       'Valor': valor_cuota - amortizacion,
                                       'Mes': mes_actual,
                                       'Estado': 'Pendiente'
                                        })
        concepto = 'Facturación cuota ' + mes_actual
        collection_detalle_facturas_tmp.insert_one({'Casa': facturacion1,
                                                    'Referencia': numero_recibo,
                                                    'Concepto': concepto,
                                                    'Valor': valor_cuota - amortizacion,
                                                    'Fecha': fecha_facturacion
                                                    })
        generate_pdf_cuota()
        collection_detalle_facturas_tmp.delete_many({'Casa': facturacion1})

def ventana():
    """Metodo que crea la ventana principal de la aplicación"""
    global frame4
    raiz.title("Balcones de Capellania")
    raiz.geometry("850x400")
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
    menu_configuracion.add_command(label="Configuración")
    raiz.config(menu=barra_menu)
    frame4 = LabelFrame(raiz, text=" CUADRO PRINCIPAL ")
    frame4.grid(row=0, column=1, rowspan=4)
    frame4.config(width=680, height=370)
class ConexionMongo:
    """Clase que me permite realizar las conexiones a la BD de datos de mongoDB"""
    def __init__(self) -> None:
        pass
class Predio:
    """Clase que me brinda las opciones de los predios del conjunto"""
    print('Ingresa a la clase de Predio')
class Persona:
    """Clase que me brinda las opciones para crear personas dentro del conjunto"""
    def __init__(self, nombre, tipid, numid):
        self.nombre = nombre
        self.tipid =  tipid
        self.numid = numid

    print("Este es temporal")

def generate_pdf_soporte_pago():
    """Metodo que genera formato de soporte de pago"""
    # Create the canvas
    
    valor_residente = combo_residente.get()
    valor_col5 = combo_casa.get()
    valor_col6 = val_pago.get()
    valor_col7 = pago_fecha.get()
    valor_col8 = val_concepto.get()
    valor_col9 = val_numtrans.get()
    valor_col10 = val_banco.get()

    nombre_fichero = 'Recibo' + str(no_recibo) + '.pdf'
    pdf_canvas = canvas.Canvas(nombre_fichero, pagesize=(400,300))
    
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

    #Cuadrado del campo Efectivo
    pdf_canvas.setFillColorRGB(255/255, 255/255, 255/255) 
    pdf_canvas.roundRect(82, 96, 15, 15, 4, stroke=1, fill=1)

    #Cuadrado del campo Consignación
    pdf_canvas.setFillColorRGB(255/255, 255/255, 255/255) 
    pdf_canvas.roundRect(209, 96, 15, 15, 4, stroke=1, fill=1)

    #Cuadrado del campo Transferencia
    pdf_canvas.setFillColorRGB(255/255, 255/255, 255/255) 
    pdf_canvas.roundRect(342, 96, 15, 15, 4, stroke=1, fill=1)

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
    pdf_canvas.drawString(295, 160, "Casa No:")
    pdf_canvas.setFont("Times-Roman", 14)
    pdf_canvas.drawString(25, 160, "Pagado Por: ")
    pdf_canvas.setFont("Times-Roman", 12)
    pdf_canvas.drawString(25, 125, "La Suma de:")
    
    pdf_canvas.drawString(25, 100, "Efectivo                     Consignacion                     Transferencia")
    
    pdf_canvas.setFont("Helvetica-Bold", 10)
    pdf_canvas.drawString(25,  75, "Observaciones:")
    pdf_canvas.drawString(25,  50, "Transacción No:")
    pdf_canvas.drawString(195, 50, "Entidad Financiera:")
    pdf_canvas.setFont("Courier-Oblique", 7.5)
    pdf_canvas.drawString(25, 30, "Numero de cuenta de Ahorros Banco Davivienda:  462500020963")
    pdf_canvas.drawString(25, 20, "Este soporte es su comprobante del pago realizado a la administración")
    
    #llenado de la informacion
    pdf_canvas.setFont("Courier-Bold", 10)
    pdf_canvas.drawString(95, 220, str(valor_col7))
    pdf_canvas.drawString(95, 200, "Cajicá")
    pdf_canvas.setFont("Courier-Bold", 14)
    pdf_canvas.drawString(350, 160, str(valor_col5))
    pdf_canvas.setFont("Courier-Bold", 10)
    pdf_canvas.drawString(105, 160, valor_residente)
    pdf_canvas.setFont("Courier-Bold", 14)
    pdf_canvas.drawString(135, 125, str(valor_col6))
    pdf_canvas.drawString(110, 50, valor_col9)
    pdf_canvas.drawString(295, 50, valor_col10)
    if tipo == 'Efectivo':
        pdf_canvas.drawString(85, 100, 'x')
    elif tipo == 'Consignación':
        pdf_canvas.drawString(212, 100, 'x')
    else:
        pdf_canvas.drawString(345, 100, 'x')

    pdf_canvas.setFont("Courier", 8)
    pdf_canvas.drawString(105, 75, valor_col8)
    
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
    global correo_envio_residente
    valor_residente = combo_residente.get()
    
    sender_email = "german.pemberty@gmail.com"
    sender_password = "ottmedkbarfpgcfw"

    # Destinatario
    recipient_email = "german.pemberthy@outlook.com"
    #recipient_email = correo_envio_residente

    # Crear el mensaje
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "Prueba de envio"

    # Cuerpo del correo
    body = "Señor residente " + valor_residente + " la administración envia en el adjunto el comprobante del ultimo pago realizado"
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
            residente.append(document['Personas']['Nombres'] + ' ' + document['Personas']['Apellidos'])
    combo_residente["values"]=residente
    combo_residente.config(state='enabled', justify=CENTER)
    residente.clear()
    
    #Aca se buscan los recibos que estan pendientes de pago para mostrarlos en pantalla. 
    collection_recibos = db.Recibos
    for document in collection_recibos.find({'Casa': seleccion}):
        if document['Estado'] == ' Pendiente ':
            valor_col1 = document['Recibo']
            valor_col2 = document['Valor']
            valor_col3 = document['Mes']
            valor_col4 = document['Anno']
            mi_arbol.insert('', 'end', values=(valor_col1, valor_col2, valor_col3, valor_col4))

def realizar_pago():
    """Metodo para gestionar pago ingresado por el front"""
    #Este es un ejemplo de como se carga un registro en el treeview
    global tipo
    global no_recibo
    valor_pendiente_pago = 0
    valor_timestamp = datetime.now()
    valor_col1 = combo_casa.get()
    valor_col2 = val_pago.get()
    valor_pagado = int(valor_col2)
    valor_col3 = pago_fecha.get()
    valor_col4 = combo_residente.get()
    valor_col5 = val_concepto.get()
    valor_col6 = rb_opcion.get()
    #valor_col7 = val_numtrans.get()
    #valor_col8 = val_banco.get()

    db = conexion_mongo()
    collection_pagos = db.Pagos
    collection_personas = db.Personas
    collection_recibos = db.Recibos
    collection_movimientos_dinero = db.Movimientos_Dinero

    if valor_col6 == 1:
        tipo = 'Efectivo'
    elif valor_col6 == 2:
        tipo = 'Consignación'
    else:
        tipo = 'Transferencia'

#    print(f'tipo: {valor_col6}')
#    mi_arbol.insert('', 'end', values=(valor_col1, valor_col2, valor_col3))

    for document in collection_pagos.find():
        no_recibo = document['No Recibo']

    no_recibo +=1

    collection_pagos.insert_one({'No Recibo': no_recibo,
                                 'Casa': int(valor_col1), 
                                 'Fecha': valor_timestamp,
                                 'Anno': 2023,
                                 'Valor': valor_pagado,
                                 'Tipo': tipo,
                                 'Observaciones': valor_col5,
                                 'Recibi De': valor_col4,
                                 'Estado': 'Pendiente'
                                        })
    #recorro la tabla de movimientos de dinero para determinar los ultimos valores que se tienen.
    for document in collection_movimientos_dinero.find():
        valor_despues_del_movimiento = document['Valor_despues_del_movimiento']
        en_efectivo = document['En_efectivo']
        en_banco = document['En_banco']

    if tipo == 'Efectivo':
        en_efectivo = en_efectivo + valor_pagado
    else:
        en_banco = en_banco + valor_pagado

    valor_antes_del_movimiento = valor_despues_del_movimiento
    valor_despues_del_movimiento = valor_despues_del_movimiento + valor_pagado

    collection_movimientos_dinero.insert_one({
        'Tipo': 'Credito',
        'Observacion': 'Pago casa',
        'Valor': valor_pagado,
        'Valor_antes_del_movimiento': valor_antes_del_movimiento,
        'Valor_despues_del_movimiento': valor_despues_del_movimiento,
        'En_efectivo': en_efectivo,
        'En_banco': en_banco,
        'Fecha_movimiento': valor_timestamp
    })

    for document in collection_personas.find({'Casa': int(valor_col1)}):
        if document['Personas']['Nombres'] == valor_col4:
            correo_envio_residente = (document['correos']['Activo'])
            print(f'Aqui voy por el correo: {correo_envio_residente}')
    
#Aqui se llama al metodo para generar el pdf
    generate_pdf_soporte_pago()

    #Aqui se llama al metodo para enviar el correo electronico con el pdf recien generado. 
    #envio_correo()

def registrar_pagos():
    """ Metodo para gestionar los pagos """
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
    
    global rb1
    global rb2
    global rb3
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
    mi_arbol = ttk.Treeview(frame4, height=5, columns=('Col1', 'Col2', 'Col3', 'Col4'))
    mi_arbol.grid(row=6, column=0, columnspan=4, pady=10)
    mi_arbol.heading('#0', text="Id")
    mi_arbol.heading('Col1', text="Recibo")
    mi_arbol.heading('Col2', text="Valor Recibo")
    mi_arbol.heading('Col3', text="Mes")
    mi_arbol.heading('Col4', text="Año")
    mi_arbol.column('#0', width=45)
    mi_arbol.column('Col1', width=110, anchor='center')
    mi_arbol.column('Col2', width=150, anchor='center')
    mi_arbol.column('Col3', width=210, anchor='center')
    mi_arbol.column('Col4', width=110, anchor='center')

def consultar_pagos():
    """Metodo que abre una ventana emergente y me permite consultar los ultimos pagos realizados por un predio"""
    
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
    """Metodo que expone el boton para guardar un pago en la Base de datos"""
    frame = LabelFrame(raiz, text="  Modulo Pagos   ")
    frame.config(width=100, height=100)
    frame.grid(row=0, column=0, padx=15, pady=10)
    #  -- Pagos  --
    #Label(frame, text="Registrar Pagos").grid(row=1, column=0)
    boton1 = Button(frame, text="Registrar Pagos", width=15, command=registrar_pagos)
    boton1.grid(row=2, column=0, sticky= W+E, padx=5, pady=5)
    boton1.config(fg='black', bg='#158645', cursor='hand2', activebackground='yellow')

    boton2 = Button(frame,text="Consultar Pagos", command=consultar_pagos)
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

ventana()

menu_pagos()

menu_personas()

menu_proyectos()

raiz.mainloop()
""" Fin del proceso"""